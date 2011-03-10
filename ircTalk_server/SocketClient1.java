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
   Socket testSocket = null;
   //DataOutputStream out = null;
   //DataInputStream in = null;
   PrintWriter out = null;
   BufferedReader in = null;
   Cipher ecipher;
   Cipher dcipher;
   String masterkey = "mysecretpassword";
   // convert masterkey to byte array for crypto
   //byte[] ivb = iv.getBytes("UTF8");
   //AlgorithmParameterSpec paramSpec = new IvParameterSpec(ivb);   

   //SecretKeySpec skey = new SecretKeySpec(masterkey, "AES");
   //Cipher ecipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
   //Cipher dcipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
   //ecipher.init(Cipher.ENCRYPT_MODE, secret, paramSpec);
   //dcipher.init(Cipher.DECRYPT_MODE, secret, paramSpec);
   //// encrypt text
   //// byte [] ciphertext = ecipher.doFinal("Hello".getBytes("UTF8"));
   //// decrypt text
   //// String plaintext = new String(dcipher.doFinal(ciphertext), "UTF-8");


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
     if (testSocket != null && out != null && in != null) {
       try {
         System.out.println("Sending \"test\" to server");
         //out.writeBytes("test\n");
         out.println("test");
         System.out.println("Waiting for Server to reply");
         String responseLine;
         responseLine = in.readLine();
         System.out.println("Recieved from Server: " + responseLine);
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
}

