package com.wish4me.android;


import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;

import org.apache.http.NameValuePair;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;

import org.apache.http.client.entity.UrlEncodedFormEntity;

import org.apache.http.client.methods.HttpPost;

import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;

import android.util.Log;
import android.widget.Toast;

public class UserHomeActivity extends Activity {
	private String session_id;
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.userhome);
	    // TODO Auto-generated method stub
	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
	    }
	    getNewIdeaForm();

	}
	
    private String getNewIdeaForm() {
    	// Create a new HttpClient and Post Header
    	HttpClient httpclient = new DefaultHttpClient();
    	HttpPost httppost = new HttpPost("http://"+Wish4meAndroidActivity.SERVERIP+"/android/newidea");
    	HttpResponse response = null;
    	String responseText = null;
    	try {
    	    // Add your data
    	    List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
    	    nameValuePairs.add(new BasicNameValuePair("sessionid", session_id));
    	    Log.e("getNewIdeaForm", "session id = "+ session_id);
    	    httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

    	    // Execute HTTP Post Request
    	    response = httpclient.execute(httppost);
        	
        	responseText = Wish4meAndroidActivity.responseToString(response);
		    Log.i("wish4me-engin", responseText);

    	} catch (ClientProtocolException e) {
        	Context context = getApplicationContext();
		    CharSequence text = "Client protocol exception : "+ e.toString();
		    int duration = Toast.LENGTH_LONG;
		    Toast toast = Toast.makeText(context, text, duration);
		    toast.show();
    	} catch (IOException e) {
        	Context context = getApplicationContext();
		    CharSequence text = "io exception : "+ e.toString();
		    int duration = Toast.LENGTH_LONG;
		    Toast toast = Toast.makeText(context, text, duration);
		    toast.show();
    	} catch (Exception e) {
        	Context context = getApplicationContext();
		    CharSequence text = "General error occured : "+ e.toString();
		    int duration = Toast.LENGTH_LONG;
		    Toast toast = Toast.makeText(context, text, duration);
		    toast.show();
		}
    	return responseText;

    }

}
