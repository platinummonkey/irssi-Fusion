package com.platinummonkey.irssifusion;

import java.util.Timer;
import java.util.TimerTask;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class IrssiFusionService extends Service {
	private static final String TAG = IrssiFusionService.class.getSimpleName();
	
	private Timer timer;
	
	private TimerTask updateTask = new TimerTask() {
		@Override
		public void run() {
			// pass
		}
	};
	
	@Override
	public IBinder onBind(Intent intent) {
		//TODO
		return null;
	}
	
	@Override
	public void onCreate() {
		super.onCreate();
		
		timer = new Timer("irssiFusion Timer");
		timer.schedule(updateTask, 1000L, 60 * 1000L);
	}
	
	@Override
	public void onDestroy() {
		super.onDestroy();
		
		timer.cancel();
		timer = null;
	}
}
