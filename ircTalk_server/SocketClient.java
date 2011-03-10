import java.io.*;
import java.net.*;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
//import javax.crypto.CipherInputStream;
//import javax.crypto.CipherOutputStream;

import java.security.spec.AlgorithmParameterSpec;
import javax.crypto.spec.SecretKeySpec;

class socketClient {
   
   public void setupCrypto(String key, String iv) {
	   // convert IV to byte array for crypto
	   byte[] ivb = iv.getBytes("UTF8");
	   AlgorithmParameterSpec paramSpec = new IvParameterSpec(ivb);
	   SecretKeySpec skey = new SecretKeySpec(key.getBytes("UTF8"), "AES");
	   Cipher ecipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
	   Cipher dcipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
	   ecipher.init(Cipher.ENCRYPT_MODE, skey, paramSpec);
	   dcipher.init(Cipher.DECRYPT_MODE, skey, paramSpec);
   }
   
   public String encrypt(String plaintext) {
	   // encrypt string
	   try {
		   //byte[] cipherbyte = ecipher.doFinal(plaintext.getBytes("UTF8")); 
		   //new String(ecipher.doFinal(plaintext.getBytes("UTF8")));
		   String ciphertext = new String(ecipher.doFinal(plaintext.getBytes("UTF8")));
		   return ciphertext;
	   } catch (Exception e){
		   e.printStackTrace();
		   return null;
	   }
   }
   
   public String decrypt(String ciphertext) {
	   // decrypt string
	   try {
		   String plaintext = new String(dcipher.doFinal(ciphertext.getBytes("UTF8")), "UTF-8");
		   return plaintext;
	   } catch (Exception e) {
		   e.printStackTrace();
		   return null;
	   }
   }
   public void main(String[] args){
	 Socket testSocket = null;
	 //DataOutputStream out = null;
	 //DataInputStream in = null;
	 PrintWriter out = null;
	 BufferedReader in = null;
	 String masterkey = "mysecretpassword";
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
    	     System.out.println("Waiting for IV..");
    	     String iv;
    	     iv = in.readLine();
    	     setupCrypto(masterkey, iv);
    	     String ciphertext;
    	     String plaintext;
    	     System.out.println("Sending \"test\" to server");
    	     //out.writeBytes("test\n");
    	     ciphertext = encrypt("test");
    	     out.println(ciphertext);
    	     System.out.println("Waiting for Server to reply");
    	     String responseLine;
    	     responseLine = in.readLine();
    	     plaintext = decrypt(responseLine);
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
}

