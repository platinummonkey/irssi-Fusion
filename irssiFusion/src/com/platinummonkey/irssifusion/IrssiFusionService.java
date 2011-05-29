package com.platinummonkey.irssifusion;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
//import android.widget.Toast;

public class IrssiFusionService extends Service {
	private static final String LOG_TAG = "IrssiFusionService";
	//MediaPlayer player;
	
	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}
	
	@Override
	public void onCreate() {
		//Toast.makeText(this, "My Service Created", Toast.LENGTH_LONG).show();
		Log.d(LOG_TAG, "onCreate");
		
		//player = MediaPlayer.create(this, R.raw.braincandy);
		//player.setLooping(false); // Set looping
	}

	@Override
	public void onDestroy() {
		//Toast.makeText(this, "My Service Stopped", Toast.LENGTH_LONG).show();
		Log.d(LOG_TAG, "onDestroy");
		//player.stop();
	}
	
	@Override
	public void onStart(Intent intent, int startid) {
		//Toast.makeText(this, "My Service Started", Toast.LENGTH_LONG).show();
		Log.d(LOG_TAG, "onStart");
		//player.start();
	}
}
