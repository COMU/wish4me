package com.wish4me.android;

import android.app.Activity;
import android.os.Bundle;

public class AddWishActivity extends Activity{
	private String session_id;
	
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.addnewwish);

	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
		}
	    

	}

}
