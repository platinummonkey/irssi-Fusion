package com.platinummonkey.irssifusion;

import static android.provider.BaseColumns._ID;
import static com.platinummonkey.irssifusion.Constants.TABLE_NAME;
import static com.platinummonkey.irssifusion.Constants.TIME;
import static com.platinummonkey.irssifusion.Constants.SEND;
import static com.platinummonkey.irssifusion.Constants.SERVER;
import static com.platinummonkey.irssifusion.Constants.TYPE;
import static com.platinummonkey.irssifusion.Constants.TOPIC;
import static com.platinummonkey.irssifusion.Constants.NICK;
import static com.platinummonkey.irssifusion.Constants.ADDRESS;
import static com.platinummonkey.irssifusion.Constants.MESSAGE;
import static com.platinummonkey.irssifusion.Constants.HILIGHT;
import static com.platinummonkey.irssifusion.Constants.NICKLIST;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class MessagesData extends SQLiteOpenHelper {
	private static final String DATABASE_NAME = "irssiFusionMessages.db";
	private static final int DATABASE_VERSION = 1;

	/** Create helper object for the Messages database **/
	public MessagesData(Context ctx) {
		super(ctx, DATABASE_NAME, null, DATABASE_VERSION);
	}
	
	@Override
	public void onCreate(SQLiteDatabase db) {
		db.execSQL("CREATE TABLE " + TABLE_NAME + " (" + _ID
				+ " INTEGER PRIMARY KEY AUTOINCREMENT, " + TIME
				+ " INTEGER, " + SEND + " INTEGER," + SERVER
				+ " TEXT NOT NULL," + TYPE + " TEXT NOT NULL," + TOPIC
				+ " TEXT NOT NULL," + NICK + " TEXT NOT NULL," + ADDRESS
				+ " TEXT NOT NULL," + MESSAGE + " TEXT," + HILIGHT
				+ " INTEGER," + NICKLIST + " TEXT);");
	}
	
	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		db.execSQL("DROP TABLE IF EXISTS" + TABLE_NAME);
		onCreate(db);
	}
}
