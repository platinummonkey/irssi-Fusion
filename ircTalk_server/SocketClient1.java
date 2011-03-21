import java.io.*;
import java.net.*;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.CipherInputStream;
import javax.crypto.CipherOutputStream;

import java.security.spec.AlgorithmParameterSpec;
import javax.crypto.spec.SecretKeySpec;

class socketClient {

   public static void main(String[] args){
   Socket androidSocket = null;
   //DataOutputStream out = null;
   //DataInputStream in = null;
   PrintWriter out = null;
   BufferedReader in = null;


     try {
       System.out.println("Connecting to Server");
       androidSocket = new Socket("localhost", 5555);
       out = new PrintWriter(androidSocket.getOutputStream(), true);
       in = new BufferedReader(new InputStreamReader(androidSocket.getInputStream()));
     } catch (UnknownHostException e) {
       System.err.println("Uknown Host");
     } catch (IOException e) {
       System.err.println("Couldn't get I/O for the connection");
     }
     if (androidSocket != null && out != null && in != null) {
       try {
         System.out.println("Sending \"test\" to server");
         out.println("test");
         System.out.println("Waiting for Server to reply");
         String responseLine;
         //responseLine = in.readLine();
         responseLine = in.readLine().replaceAll("\\\\n", "");
         System.out.println("Recieved from Server: " + responseLine);
         System.out.println("Closing Connection");
         out.close();
         in.close();
         androidSocket.close();
     } catch (UnknownHostException e) {
       System.err.println("Trying to connect to unknown host:" + e);
     } catch (IOException e) {
       System.err.println("IOException: " + e);
     }
   }
 }
}

