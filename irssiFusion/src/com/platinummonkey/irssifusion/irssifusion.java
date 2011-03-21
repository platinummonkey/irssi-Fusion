package com.platinummonkey.irssifusion;

import android.app.Activity;
import android.os.Bundle;
import java.io.*;
import java.net.*;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.widget.ListView;
//import android.util.Log;

public class irssifusion extends Activity {
//    /** Called when the activity is first created. */
//    @Override
//    public void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.main);
//    }
//}
//
//public class ClientActivity extends Activity {

    //private String serverIpAddress = "64.85.168.188";
    
    //private boolean connected = false;
    
	TextView txtServerChannel;
	TextView txtChannelTopic;
	ListView listMessages; 
    
	Socket testSocket = null;
	//DataOutputStream out = null;
	//DataInputStream in = null;
	PrintWriter out = null;
	BufferedReader in = null;
	String plaintext;
	
	
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
      startServer();
      channelTest();  
    }

    public void startServer() {
		// starts server
		try {
			System.out.println("Connecting to Server");
			testSocket = new Socket("platinummonkey.com", 5555);
			//out = new DataOutputStream(testSocket.getOutputStream());
			//in = new DataInputStream(testSocket.getInputStream());
			out = new PrintWriter(testSocket.getOutputStream(), true);
         	in = new BufferedReader(new InputStreamReader(testSocket.getInputStream()));
		} catch (UnknownHostException e) {
			System.err.println("Uknown Host");
		} catch (IOException e) {
			System.err.println("Couldn't get I/O for the connection");
		}
	}
    
    public void channelTest() {
    	try {
    		// test server stuff
    		if (testSocket != null && out != null && in != null) {
   			 	try {
   			 		//System.out.println("Sending \"test\" to server");
   			 		//System.out.println("Sent: test");
   			 		out.println("test");
   			 		//System.out.println("Waiting for Server to reply");
   			 		String responseLine;
   			 		//responseLine = in.readLine(); //.replaceAll("\\\\n", "");
   			 		responseLine = in.readLine();
   			 		//System.out.println("Recieved from Server: " + responseLine + " - length: " + responseLine.length());
   			 		//System.out.println("\nEscaped: "+ responseLine.replaceAll("\\", "\\\\"));
   			 		plaintext = responseLine;
   			 		//System.out.println("Recieved from Server: " + plaintext);
   			 		//System.out.println("Closing Connection");
   			 		out.close();
   			 		in.close();
   			 		testSocket.close();
   			 	} catch (UnknownHostException e) {
   			 		//System.err.println("Trying to connect to unknown host:" + e);
   			 		plaintext = "failure" + e;
   			 	} catch (IOException e) {
   			 		//System.err.println("IOException: " + e);
   			 		plaintext = "failure" + e;
   			 	}
   		 	}
    		// end test server stuff
    		String jString = plaintext;
    		//String jString = "{\"server\": \"freenode\",  \"channel\": \"#testchannel\", \"messages\": [ {\"time\": \"timestamp\", \"nick\": \"testNick\", \"message\": \"message 1 this is the message\", \"address\": \"somenick@someplace.com\"}, {\"time\": \"timestamp\", \"nick\": \"otherNick\", \"message\": \"message 2 this is the message\", \"address\": \"othernick@someplace.com\"} ] }";
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