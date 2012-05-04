package com.wish4me.android;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.NameValuePair;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;

import android.widget.Toast;

import com.wish4me.android.R;

import com.facebook.android.DialogError;
import com.facebook.android.Facebook;
import com.facebook.android.Facebook.DialogListener;
import com.facebook.android.FacebookError;



public class Wish4meAndroidActivity extends Activity {
	
	EditText name;
	
	Facebook facebook = new Facebook("255768354473895");
	private SharedPreferences mPrefs;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        // Capture our button from layout
        Button button = (Button)findViewById(R.id.go);
        // Register the onClick listener with the implementation above
        button.setOnClickListener(mAddListener);
      
    }
    
    // Create an anonymous implementation of OnClickListener
    private OnClickListener mAddListener = new OnClickListener() {
    	public void onClick(View v) {
		    long id = 0;
		    // do something when the button is clicked
		    try {
			    
			    if(facebookLogin()) {
				  postFacebookID();
			    }
		    } catch (Exception ex) {
			    Context context = getApplicationContext();
			    CharSequence text = ex.toString() + "ID = " + id;
			    int duration = Toast.LENGTH_LONG;
			    Toast toast = Toast.makeText(context, text, duration);
			    toast.show();
		    }
	    }
    };
    
    public static String responseToString(HttpResponse response){
        String result = "";
        try{
            InputStream in = response.getEntity().getContent();
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));
            StringBuilder str = new StringBuilder();
            String line = null;
            while((line = reader.readLine()) != null){
                str.append(line + "\n");
            }
            in.close();
            result = str.toString();
        }catch(Exception ex){
            result = "Error";
        }
        return result;
    }
    
    private void postFacebookID() {
    	// Create a new HttpClient and Post Header
    	HttpClient httpclient = new DefaultHttpClient();
    	HttpPost httppost = new HttpPost("http://192.168.1.40/android/flogin");

    	try {
    	    // Add your data

	    	JSONObject jObject = new JSONObject(facebook.request("me"));    
	    	String facebookID =jObject.getString("id");
	    	String facebookEmail =jObject.getString("email");
	    	String facebookUsername = "";
    		try {
    			facebookUsername = jObject.getString("username");
			} catch (JSONException e) {
				//in case no username, just pass 
			}
		    

    	    List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
    	    nameValuePairs.add(new BasicNameValuePair("id", facebookID));
    	    nameValuePairs.add(new BasicNameValuePair("email", facebookEmail));
    	    if(!facebookUsername.isEmpty())
    	    	nameValuePairs.add(new BasicNameValuePair("username", facebookUsername));
    	    httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

    	    // Execute HTTP Post Request
    	    HttpResponse response = httpclient.execute(httppost);
        	Context context = getApplicationContext();
        	String responseText = responseToString(response);
		    CharSequence text = "answer returned : "+ response;
		    Log.i("wish4me-engin", responseText);
		    int duration = Toast.LENGTH_LONG;
		    Toast toast = Toast.makeText(context, text, duration);
		    toast.show();
		    
		    

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

    }
    
    private boolean facebookLogin(){
    	
        mPrefs = getPreferences(MODE_PRIVATE);
        String access_token = mPrefs.getString("access_token", null);
        long expires = mPrefs.getLong("access_expires", 0);
        if(access_token != null) {
            facebook.setAccessToken(access_token);
        }
        if(expires != 0) {
            facebook.setAccessExpires(expires);
        }
        if(!facebook.isSessionValid()) {
		    facebook.authorize(this, new String[] { "email" }, new DialogListener() {
	            public void onComplete(Bundle values) {
                    SharedPreferences.Editor editor = mPrefs.edit();
                    editor.putString("access_token", facebook.getAccessToken());
                    editor.putLong("access_expires", facebook.getAccessExpires());
                    editor.commit();
                    
	            	Context context = getApplicationContext();
				    CharSequence text = "Facebook success : "+ facebook.getAccessToken();
				    int duration = Toast.LENGTH_LONG;
				    Toast toast = Toast.makeText(context, text, duration);
				    toast.show();
	            }
	
	            public void onFacebookError(FacebookError error) {
	            	Context context = getApplicationContext();
				    CharSequence text = "Facebook error occured : "+ error.toString();
				    int duration = Toast.LENGTH_LONG;
				    Toast toast = Toast.makeText(context, text, duration);
				    toast.show();
	            }
	
	            public void onError(DialogError e) {
	            	Context context = getApplicationContext();
				    CharSequence text = "dialog error occured";
				    int duration = Toast.LENGTH_LONG;
				    Toast toast = Toast.makeText(context, text, duration);
				    toast.show();
	            }
	
	            public void onCancel() {
	            }
	        });
        } else {
        	return true;
        }
        if(facebook.isSessionValid())		//if it is valid now,
        	return true;
		return false;
        
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        facebook.authorizeCallback(requestCode, resultCode, data);

    }
}