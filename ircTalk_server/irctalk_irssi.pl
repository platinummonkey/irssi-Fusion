# socket_remote.pl -- send commands to Irssi through a UNIX Socket
#
# DESCRIPTION
#
# fifo_remote.pl creates a named pipe (a.k.a. fifo). Everything written to the
# fifo will be passed on to Irssi and run as a command. (You need not precede
# you commands with `/', or whatever you've set you `cmdchars' to -- this also
# means that if you want to send a message, you must use the explicit `say'
# command.)
#
# SETTINGS
#
# fifo_remote_file (default is `remote-control')
#
#       This is the file name of the named pipe. Any leading `~[USER]' part is
#       expanded before use. If the name does not begin with `/' it is taken to
#       be relative to Irssi's current configuration dir (usually `~/.irssi').
#
#       The default value thus normally means `~/.irssi/remote-control'.
#
# NOTES
#
# This script may have limited use to you, since it cannot bring back *any*
# return values from Irssi. It can only run Irssi commands from the outside. --
# I use it to trigger my online/away messages from any shell, and that's about
# it.
#
# CAVEATS
#
# Due to the way named pipes (or fifos) works one must take extra care when
# writing to one of these beasts -- if not, the writing program may well hang
# forever. This is because the writing process will not terminate until the
# fifo has been read from the other end (see also fifo(4)).
#
# To avoid this problem, I usually use something akin to the below shell
# function to write to the Irssi fifo remote. It simply kills off the writing
# process if it's still around after a certain timeout (e.g. the fifo could be
# present but Irssi not running -- and thus the pipe would never be read). The
# entire process is done in the background, so the caller of the function does
# not have to wait.
#
#     FILE="$HOME/.irssi/remote-control"
#     irssi_command() {
#          if [ -p "$FILE" ]; then
#              (   echo "$*" > "$FILE" &
#                  sleep 5
#                  kill $! 2>/dev/null   )&
#          fi
#      }
#
# TODO
#
# o Clean up fifo file when Irssi quits -- right now this is not done, so extra
#   precautions are required inside your shell scripts to make sure they do not
#   hang indefinately when trying to write to the remote control fifo. (See
#   above example.)
#
# HISTORY
#
# [2004-08-12, 22.16-00.58] v0.1a - began implementing it
#
# [2004-08-13, 09.52-10-19] v0.2a - began implementing fifo_read
#
# [2004-08-14, 01.12-04.27] v0.3a
#
# [2004-08-14, 14.09-18.13] v0.4a - seems to be fully functional, except for
# the fact that commands aren't run in the proper window/server environment
#
# [2004-08-15, 18.17-19.26] v0.5a - command comming through pipe is now run in
# the active window; removed bug which crashed Irssi, bug was caused by several
# input_add()s being called without having been removed in between
#
# [2004-08-26, 21.46-22.30] v0.5 - wrote above docs
#

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

our ($server,   # server handle
     $socket ); # socket handle expanded from Irssi config

#TODO make this an irssi setting
# Irssi settings
Irssi::settings_add_str($IRSSI{name},   # default socket_remote
	'socket_remote_file', 'socket-remote');

# We don't want this to be a blocking socket otherwise irssi will hang
sub setNonBlock
{
  my ($fd) = @_;
  my $flags = fcntl($fd, F_GETFL, 0);
  fcntl($fd, F_SETFL, $flags | O_NONBLOCK);
}

# check socket for data, then act.
sub check_sock
{
  my $msg;
  if (my $client = $server->accept()) {
    $client->recv($msg, 1024);
    print "Got message: $msg" if $msg;

  if ($msg) {
    Irssi::active_win->command($msg);
  }
} 

# clean up on unload (/script unload)
Irssi::signal_add_first
	'command script unload', sub {
		my ($script) = @_;
		return unless $script =~
			/(?:^|\s) $IRSSI{name}
			 (?:\.[^. ]*)? (?:\s|$) /x;
		close($socket);
		Irssi::print("%B>>%n $IRSSI{name} $VERSION unloaded", MSGLEVEL_CLIENTCRAP);
	};

sub createSocket() {
  my $server = IO::Socket::UNIX->new(Local   => $socket,
                                     Type    => SOCK_STREAM,
                                     Listen  => 5) or die $@;
  setNonBlock($server);
}

sub setup() {
  my $new_socket = Irssi::settings_get_str
			'socket_remote_file';
  unlink $socket; # destroy old socket if there
  $socket = $new_socket; # set handle
  createSocket();
}  

setup();
Irssi::signal_add('setup changed', \&setup);
print CLIENTCRAP "%B>>%n $IRSSI{name} $VERSION (by $IRSSI{authors}) loaded";
print CLIENTCRAP "    (socket: $socket)";
my $timer == Irssi::timeout_add(250, \&check_sock, []);
