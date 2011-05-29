# socket_remote.pl -- send commands to Irssi through a UNIX Socket
#
#  Cody Lee "platinummonkey" (aka "pltmnky") <platinummonkey@archlinux.us>
#
#  
#
# connect to the socket and send any normal irssi command to irssi. do not
# precede with '/'
#
# SETTINGS
#
# socket_remote_file (default is `socket-remote')
#      Use absolute paths only.
#
# TODO
#  1. Clean up after irssi quits.
#  2. Add 
#
# CHANELOG
#  2011-02-18 - v0.1 - created

our $VERSION = '0.1';
our %IRSSI = (
    authors     => 'Cody Lee',
    contact     => 'platinummonkey\@archlinux.us',
    name        => 'socket_remote',
    description => 'Irssi remote control for a connecting socket server ' .
                   'run all commands written to the socket.',
    license     => 'GPLv2',
    url         => 'http://www.irssi.org/scripts/',
    changed	=> '2011-02-18',
); 
use strict;
use IO::Socket;     # provides socket connections
use Irssi;          # provides irssi functions
use Fcntl;          # provides `O_NONBLOCK' and `O_RDONLY' constants
use Time::Format qw(%strftime);
use JSON;			# json encoding

# NOTES
# Irssi::channels() - irssi list all channels
#
# trigger types with a message and a channel
#my @allchanmsg_types = qw(publics pubactions pubnotices parts quits kicks topics);
## trigger types with a message
#my @allmsg_types = (@allchanmsg_types, qw(privmsgs privactions privnotices));
## trigger types with a channel
#my @allchan_types = (@allchanmsg_types, qw(mode_channel mode_nick joins invites));


my $server = "";   # server handle
my $socket = ""; # socket handle expanded from Irssi config
my $server_log = ""; # log server handle
my $socket_log = ""; # socket handle expanded from Irssi config

#TODO make this an irssi setting
# Irssi settings
my $defaultsock = $ENV{"HOME"} . "/.irssi/socket-remote";
Irssi::settings_add_str($IRSSI{name},   # default socket_remote
	'socket_remote_file', $defaultsock);
my $defaultsocklog = $ENV{"HOME"} . "/.irssi/socket-log";
Irssi::settings_add_str($IRSSI{name},   # default socket_log
	'socket_log_file', $defaultsocklog);

# We don't want this to be a blocking socket otherwise irssi will hang
sub setNonBlock
{
  my ($fd) = @_;
  my $flags = fcntl($fd, F_GETFL, 0);
  fcntl($fd, F_SETFL, $flags | O_NONBLOCK);
}

## check socket for data, then act.
#sub check_sock
#{
  #my $msg;
  #if (my $client = $server->accept()) {
    #$client->recv($msg, 1024);
    #print "Got message: $msg" if $msg;

	#if ($msg) {
	  #Irssi::active_win->command($msg);
	#}
  #}
#} 

sub check_sock
{
  use vars qw($server);
  my $msg;
  $server->recv($msg, 1024);
  print "Got message to forward: $msg" if $msg;

  if ($msg) {
	Irssi::active_win->command($msg);
  }
} 

sub send_log_sock
{
	my $msg = @_;
	$server->send($msg);
}

# clean up on unload (/script unload)
Irssi::signal_add_first
	'command script unload', sub {
		my ($script) = @_;
		return unless $script =~
			/(?:^|\s) $IRSSI{name}
			 (?:\.[^. ]*)? (?:\s|$) /x;
		close($socket); # close socket
		close($socket_log); # close log socket
		#$server->shutdown();
		#$server_log->shutdown();
		Irssi::print("%B>>%n $IRSSI{name} $VERSION unloaded", MSGLEVEL_CLIENTCRAP);
	};

sub try (&$) {
	my($try, $catch) = @_;
	eval {$try };
	if ($@) {
		local $_ = $@;
		&$catch;
	}
}
sub catch (&) { $_[0] }

#try {
	## attempt to connect to ircTalk Server UNIX sockets:
	my $new_socket = Irssi::settings_get_str
			'socket_remote_file';
	#unlink $new_socket; # destroy old socket if there
	$socket = $new_socket; # set handle
	$server = IO::Socket::UNIX->new(Peer	=> $socket ) or die $@;
									#Local   => $socket,
									#Type    => SOCK_STREAM,
									#Listen  => 5) or die $@;
	setNonBlock($server);
	
	my $new_log_socket = Irssi::settings_get_str
			'socket_log_file';
	#unlink $new_log_socket; # we aren't handling this socket the server is
	$socket_log = $new_log_socket; # set handle
	$server_log = IO::Socket::UNIX->new(Peer	=> $socket_log ) or die $@;
	setNonBlock($server_log);
#}
#catch {
#	# Couldn't connect to one of the sockets. error out and display on CLIENTCRAP
#	print CLIENTCRAP "Is the ircTalk server running? This must be run prior to loading this script!\n";
#	die "ERROR connecting to server";
#};

# forwards all privmsgs to ther server
sub sig_privmsg {
	my ($server, $data, $nick, $address) = @_;
	my ($target, $msg) = split(/ :/, $data,2);
	my %privmsgHash = {};
	my $serverName = $server->{'tag'};
	my $yournick = $server->{'nick'};
	my $targetType;
	if ($target =~ m/^#+/) {
		$targetType = "CHANNEL";
	} else {
		$targetType = "QUERY";
	}
	# assign values to hash
	$privmsgHash{$target}{"type"} = $targetType;
	$privmsgHash{$target}{"server"} = $serverName;
	$privmsgHash{$target}{"nick"} = $nick;
	$privmsgHash{$target}{"message"} = $msg;
	$privmsgHash{$target}{"address"} = $address;
	#print CLIENTCRAP "server: $serverName | msg: $msg | nick: $nick | address: $address | target: $target";
	# compile json
	my $json->{"privmsg"} = \%privmsgHash;
	my $json_text = to_json($json);
	# forward to server socket
}

sub sig_nick {
   my ($server, $newnick, $nick, $address) = @_;
   $newnick = substr ($newnick, 1) if ($newnick =~ /^:/);
   my $serverName = $server->{'tag'};
   my $yournick = $server->{'nick'};
   my %nickHash = {};
   # assign values to hash
   $nickHash{$serverName}{"nick"} = $nick;
   $nickHash{$serverName}{"newnick"} = $newnick;
   $nickHash{$serverName}{"yournick"} = $yournick;
   $nickHash{$serverName}{"address"} = $address;
   print CLIENTCRAP "server: $server | nick: $nick | newnick: $newnick | address: $address";
   # compile json
   my $json->{"nickchange"} = \%nickHash;
   my $json_text = to_json($json);
   # forward to server socket
 }

sub sig_get_windows {
	# Grabs all the current open windows then sends them to the server
	# on all user channel joins/parts/kicks
	my $channels = &get_windows();
	# send to remote server
}

sub get_windows {
	# Irrsi is a bit ambiguous... I want names not reference numbers
	#    as Irssi:windows would only supply unless you iterate over each
	#    window item, make it active, then you can get the name.
	#
	#  There are 3 window types: CHANNEL, QUERY and EXEC.
	#       EXEC is not supported yet.
	# channels:
	my %channelHash = {};
	for my $win (Irssi::channels()) {
		$channelHash{$win->{"name"}}{"type"} = "CHANNEL";
		$channelHash{$win->{"name"}}{"topic"} = $win->{"topic"};
		$channelHash{$win->{"name"}}{"server"} = $win->{"server"}{"tag"};
		$channelHash{$win->{"name"}}{"nick"} = $win->{"server"}{"nick"};
		my @nicklist;
		for my $n ($win->nicks()) {
			push(@nicklist, $n->{"nick"})
		}
		$channelHash{$win->{"name"}}{"nicklist"} = "@nicklist"; # "them them them you them..."
	}
	# queries:
	for my $win (Irssi::queries()) {
		$channelHash{$win->{"name"}}{"type"} = "QUERY";
		$channelHash{$win->{"name"}}{"topic"} = ""; # queries have no channel topic
		$channelHash{$win->{"name"}}{"server"} = $win->{"server"}{"tag"};
		$channelHash{$win->{"name"}}{"nick"} = $win->{"server"}{"nick"};
		$channelHash{$win->{"name"}}{"nicklist"} = $win->{"name"}." ".$win->{"server"}{"nick"}; # "them you"
	}
	# compile json
	my $json->{"channels"} = \%channelHash;
	my $json_text = to_json($json);
	return($json_text);
}

### Signals
Irssi::signal_add("event privmsg", \&sig_privmsg);
Irssi::signal_add_last('channel created', \&sig_get_windows);
Irssi::signal_add_last('channel destroyed', \&sig_get_windows);
Irssi::signal_add_last('query created', \&sig_get_windows);
Irssi::signal_add_last('query destroyed', \&sig_get_windows);
# TODO:
#Irssi::signal_add("event notice", \&forward);
#Irssi::signal_add("event join", \&forward);
#Irssi::signal_add("event part", \&forward);
#Irssi::signal_add("event quit", \&forward);
#Irssi::signal_add("event ctcp", \&forward);
#Irssi::signal_add("event crap", \&forward);
#Irssi::signal_add("event action", \&forward);
#Irssi::signal_add("event topic", \&forward);
#Irssi::signal_add("event kick", \&forward);
#Irssi::signal_add("event mode", \&forward);

#Irssi::signal_add('setup changed', \&setup);
print CLIENTCRAP "%B>>%n $IRSSI{name} $VERSION (by $IRSSI{authors}) loaded";
print CLIENTCRAP "    (socket: $socket) - (log_socket: $socket_log)";
my $channels = &get_windows();
#print CLIENTCRAP "json channels: $channels";
#print $server_log $channels;
my $timer == Irssi::timeout_add(250, \&check_sock, []);
#my $timer2 == Irssi::timeout_add(250, \&sock, []);
