package com.wish4me.android;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;


public class OnClickListenerWithInt implements OnClickListener {
	private int value;
	private Method methodToCall;
	private Object objectOfMethod;
	public OnClickListenerWithInt(int value, Method methodToCall, Object objectOfMethod) {
		this.value = value;
		this.methodToCall = methodToCall;
		this.objectOfMethod = objectOfMethod;
	}
	public void onClick(View v) {
		try {
			methodToCall.invoke(objectOfMethod, new Object[] {value});
		} catch (IllegalArgumentException e) {
			Log.e("Wish4me-OnclickWithInt", "IllegalArgumentException"+ e.toString());
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			Log.e("Wish4me-OnclickWithInt", "IllegalAccessException"+ e.toString());
			e.printStackTrace();
		} catch (InvocationTargetException e) {
			Log.e("Wish4me-OnclickWithInt", "InvocationTargetException"+ e.toString());
			e.printStackTrace();
		}
		/*
		Context context = v.getContext();
		CharSequence text = "clicked to "+ value;
		int duration = Toast.LENGTH_LONG;
		Toast toast = Toast.makeText(context, text, duration);
		toast.show();
		*/
	}

}
