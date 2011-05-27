package com.platinummonkey.irssifusion;

import android.app.Activity;
import android.os.Bundle;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException; 
import android.widget.TextView;
import android.util.Log;

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
    
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        TextView replytexttv = (TextView) this.findViewById(R.id.replytext);
        TextView statustexttv = (TextView) this.findViewById(R.id.statustext);
    
    try {
    	    statustexttv.setText("Connecting......");
            Socket s = new Socket("64.85.168.188",5555);
            statustexttv.setText("Connected");
            //outgoing stream redirect to socket
            OutputStream out = s.getOutputStream();
            statustexttv.setText("Output stream created");
            PrintWriter output = new PrintWriter(out);
            statustexttv.setText("printwriter created");
            output.println("Hello Android!");
            statustexttv.setText("sent");
            BufferedReader input = new BufferedReader(new InputStreamReader(s.getInputStream()));
            statustexttv.setText("buffer created");
            //read line(s)
            String st = input.readLine();
            statustexttv.setText("read data");
            replytexttv.setText(st);
            statustexttv.setText("set text");
            //Close connection
            s.close();
            statustexttv.setText("Closed connection");
           
           
    } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
    } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            replytexttv.setText("socket error");
    }

	}
}