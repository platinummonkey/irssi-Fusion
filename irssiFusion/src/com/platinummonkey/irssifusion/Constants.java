package com.platinummonkey.irssifusion;

import android.net.Uri;
import android.provider.BaseColumns;

public interface Constants extends BaseColumns {
	public static final String TABLE_NAME = "messages";
	// turn this into a content provider
	public static final String AUTHORITY = "com.platinummonkey.irssifusion";
	public static final Uri CONTENT_URI = Uri.parse("content://"
	         + AUTHORITY + "/" + TABLE_NAME);
	
	// Columns in the Messages database
	public static final String TIME = "time" ;
	public static final String SEND = "send";
	public static final String SERVER = "server";
	public static final String TYPE = "type";
	public static final String TOPIC = "topic" ;
	public static final String NICK = "nick";
	public static final String ADDRESS = "address";
	public static final String MESSAGE = "message";
	public static final String HILIGHT = "hilight";
	public static final String NICKLIST = "nicklist";
}
