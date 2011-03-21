package com.platinummonkey.irssifusion;

import org.json.JSONArray;
import org.json.JSONObject;

import android.app.Activity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class channel extends Activity {
//  /** Called when the activity is first created. */
//  @Override
//  public void onCreate(Bundle savedInstanceState) {
//      super.onCreate(savedInstanceState);
//      setContentView(R.layout.main);
//  }
//}
//
//public class ClientActivity extends Activity {

  //private String serverIpAddress = "64.85.168.188";
  
  //private boolean connected = false;
  
	TextView txtServerChannel;
	TextView txtChannelTopic;
	ListView listMessages; 
  
  @Override
  protected void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      setContentView(R.layout.channel);
      
      txtServerChannel = (TextView) findViewById(R.id.serverchannel);
      txtChannelTopic = (TextView) findViewById(R.id.channeltopic);
      listMessages = (ListView) findViewById(R.id.ListView01);
      /*btnChannel = (Button) findViewById(R.id.btnChannel);
      btnChannel.setOnClickListener(new Button.OnClickListener() {
      	public void onClick(View v) {
      		examineXMLFile();
      	}
      });
      
      btnQuery = (Button) findViewById(R.id.btnQuery);
      btnQuery.setOnClickListener(new Button.OnClickListener() {
      	public void onClick(View v) {
      		examineJSONFile();
      	}
      });
   */
    channelTest();  
  }

  void channelTest() {
  	try {
  		String jString = "{\"server\": \"freenode\",  \"channel\": \"#testchannel\", \"messages\": [ {\"time\": \"timestamp\", \"nick\": \"testNick\", \"message\": \"message 1 this is the message\", \"address\": \"somenick@someplace.com\"}, {\"time\": \"timestamp\", \"nick\": \"otherNick\", \"message\": \"message 2 this is the message\", \"address\": \"othernick@someplace.com\"} ] }";
  		JSONObject jObject = new JSONObject(jString);
  		String serverChannelString = jObject.getString("server") + " | " + jObject.getString("channel");
  		txtServerChannel.setText(serverChannelString);
  		JSONArray messagesArray = jObject.getJSONArray("messages");
  		txtChannelTopic.setText("There are " + messagesArray.length() + "messages");
  		String [] messages_arr = new String[messagesArray.length()];
  		int i;
  		for (i=0;i<messagesArray.length();i++) {
  			JSONObject privmsg = messagesArray.getJSONObject(i);
  			String msgNick = privmsg.getString("nick").toString();
  			String msgMessage = privmsg.getString("message").toString();
  			String msgTimestamp = privmsg.getString("time").toString();
  			String msgAddress = privmsg.getString("address").toString();
  			messages_arr[i] = "[" + msgTimestamp + "] " + msgNick + " | " + msgMessage;
  		}
  		listMessages.setAdapter(new ArrayAdapter<String>(this, R.layout.channel_list_item, messages_arr));
  	} catch (Exception je) {
  		txtChannelTopic.setText("failure" + je);
  	}
  }
}
