package com.wish4me.android;

import android.content.Context;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Toast;

public class OnClickListenerWithInt implements OnClickListener {
	private int value;
	public OnClickListenerWithInt(int value) {
		this.value = value;
	}
	public void onClick(View v) {
		Context context = v.getContext();
		CharSequence text = "clicked to "+ value;
		int duration = Toast.LENGTH_LONG;
		Toast toast = Toast.makeText(context, text, duration);
		toast.show();
		
	}

}
