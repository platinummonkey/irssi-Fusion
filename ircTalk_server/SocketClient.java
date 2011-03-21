import java.io.*;
import java.util.*;
import java.net.*;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
//import javax.crypto.CipherInputStream;
//import javax.crypto.CipherOutputStream;

import java.security.spec.AlgorithmParameterSpec;
import javax.crypto.spec.SecretKeySpec;

class clientHandler {
	/*
	 *  This class sets up AES CBC encryption for the socket, 
	 *  new instance for every connection since the IV changes
	 */
	
	// Declare variables
	Socket testSocket = null;
	//DataOutputStream out = null;
	//DataInputStream in = null;
	PrintWriter out = null;
	BufferedReader in = null;
	String masterkey = "mysecretpassword";
    
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
	 
	 public void androidClientHandler() {
		 // actual communication
		 if (testSocket != null && out != null && in != null) {
			 try {
				 System.out.println("Sending \"test\" to server");
				 System.out.println("Sent: test");
				 out.println("test");
				 System.out.println("Waiting for Server to reply");
				 String responseLine;
				 //responseLine = in.readLine(); //.replaceAll("\\\\n", "");
				 responseLine = in.readLine();
				 System.out.println("Recieved from Server: " + responseLine + " - length: " + responseLine.length());
				 //System.out.println("\nEscaped: "+ responseLine.replaceAll("\\", "\\\\"));
				 plaintext = responseLine;
				 System.out.println("Recieved from Server: " + plaintext);
				 System.out.println("Closing Connection");
				 out.close();
				 in.close();
				 testSocket.close();
			 } catch (UnknownHostException e) {
				 System.err.println("Trying to connect to unknown host:" + e);
			 } catch (IOException e) {
				 System.err.println("IOException: " + e);
			 }
		 }
	 }
	 
	 public void javaIsGay() {
		 // java is fucking gay
		 startServer();
		 androidClientHandler();
	 }
	 
	 public static void main(String[] args) {
		 System.setProperty("file.encoding", "UTF-8");
		 clientHandler c = new clientHandler();
		 c.javaIsGay();
	 }
}
