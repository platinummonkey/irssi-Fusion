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
	private Cipher ecipher;
	private Cipher dcipher;
	Socket testSocket = null;
	//DataOutputStream out = null;
	//DataInputStream in = null;
	PrintWriter out = null;
	BufferedReader in = null;
	String masterkey = "mysecretpassword";
   	
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
    
    public void setupCrypto(byte[] iv, String key) {
	    // setup AES CBC encryption
	    // 	convert IV and key to byte array for crypto
	    try {
			 System.out.println("Setting up Crypto...");
		 	 //byte[] ivb = iv.getBytes("UTF8");
		 	 byte[] keyb = key.getBytes("UTF8");
			 AlgorithmParameterSpec paramSpec = new IvParameterSpec(iv);
			 SecretKeySpec skey = new SecretKeySpec(keyb, "AES");
			 ecipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
			 dcipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
			 ecipher.init(Cipher.ENCRYPT_MODE, skey, paramSpec);
			 dcipher.init(Cipher.DECRYPT_MODE, skey, paramSpec);
		} catch (Exception e) {
			System.err.println("Error:" + e);
		}
    }
    
    public void startServer() {
		// starts server
		try {
			System.out.println("Connecting to Server");
			testSocket = new Socket("localhost", 5555);
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
    
    public static byte[] hexStringToByteArray(String s) {
		int len = s.length();
		byte[] data = new byte[len / 2];
		for (int i = 0; i < len; i += 2) {
			data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
								+ Character.digit(s.charAt(i+1), 16));
		}
		return data;
	}

    /*
	 * df
	 */
	 
	 public void androidClientHandler() {
		 // actual communication
		 if (testSocket != null && out != null && in != null) {
			 try {
			 	 System.out.println("Waiting for IV..");
				 String iv;
				 iv = in.readLine();
				 byte [] ivb = hexStringToByteArray(iv);
				 System.out.println("Got IV..." + iv);
				 // Setup ciphers
				 //setupCrypto(masterkey, iv);
				 // convert IV to byte array for crypto
				 //byte[] ivb = iv.getBytes("UTF8");
				 //AlgorithmParameterSpec paramSpec = new IvParameterSpec(ivb);
				 //SecretKeySpec skey = new SecretKeySpec(masterkey.getBytes("UTF8"), "AES");
				 //ecipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
				 //dcipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
				 //ecipher.init(Cipher.ENCRYPT_MODE, skey, paramSpec);
				 //dcipher.init(Cipher.DECRYPT_MODE, skey, paramSpec);
				 // ciphers are setup
				 setupCrypto(ivb, masterkey);
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
	 
	 public void javaIsGay() {
		 // java is fucking gay
		 startServer();
		 androidClientHandler();
	 }
	 
	 public static void main(String[] args) {
		 clientHandler c = new clientHandler();
		 c.javaIsGay();
	 }
}
