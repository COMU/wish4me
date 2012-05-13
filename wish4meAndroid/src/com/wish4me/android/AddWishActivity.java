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
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;

import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ImageView.ScaleType;
import android.widget.Toast;

public class AddWishActivity extends Activity{
	private String session_id;
	private Uri capturedImage;
	
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.addnewwish);

	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
		}

		ImageButton launchCameraButton = (ImageButton) findViewById(R.id.capture_image_button);
		// Register the onClick listener with the implementation above
		launchCameraButton.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {
			    Intent intent = new Intent("android.media.action.IMAGE_CAPTURE");
			    intent.putExtra(MediaStore.EXTRA_OUTPUT, capturedImage);
			    
			    startActivityForResult(intent, 0);
				
			}
		});


		ImageButton addWishButton = (ImageButton) findViewById(R.id.addwish_button);
		// Register the onClick listener with the implementation above
		addWishButton.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {
				postNewWish();
				
			}
		});

		

	}
	
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		if (resultCode == Activity.RESULT_OK && requestCode == 0) {
		String result = data.toURI();
		Log.e("wish4me-capture", "result is "+result);
		
		ImageView capturedImageView = (ImageView) findViewById(R.id.captured_image);
		capturedImageView.setImageURI(Uri.parse(result));
		capturedImageView.setScaleType(ScaleType.CENTER_INSIDE);
		}
		}

	private String postNewWish() {
		// Create a new HttpClient and Post Header
		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost("http://" + LoginActivity.SERVERIP + "/android/addnewwish");
		HttpResponse response = null;
		String responseText = null;
		try {
			// Add your data
			
			EditText newWishBrand = (EditText) findViewById(R.id.addwish_edit_brand);
			EditText newWishName = (EditText) findViewById(R.id.addwish_edit_name);
			EditText newWishDescription = (EditText) findViewById(R.id.addwish_edit_description);
			
			List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
			nameValuePairs.add(new BasicNameValuePair("sessionid", session_id));
			nameValuePairs.add(new BasicNameValuePair("brand", newWishBrand.getText().toString()));
			nameValuePairs.add(new BasicNameValuePair("name", newWishName.getText().toString()));
			nameValuePairs.add(new BasicNameValuePair("description", newWishDescription.getText().toString()));
			httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

			// Execute HTTP Post Request
			response = httpclient.execute(httppost);

			responseText = LoginActivity.responseToString(response);
			Log.i("wish4me-engin", responseText);

		} catch (ClientProtocolException e) {
			Log.e("wish4me-postFacebookID", e.toString());
			Context context = getApplicationContext();
			CharSequence text = "Client protocol exception : " + e.toString();
			int duration = Toast.LENGTH_LONG;
			Toast toast = Toast.makeText(context, text, duration);
			toast.show();
		} catch (IOException e) {
			Log.e("wish4me-postFacebookID", e.toString());
			Context context = getApplicationContext();
			CharSequence text = "io exception : " + e.toString();
			int duration = Toast.LENGTH_LONG;
			Toast toast = Toast.makeText(context, text, duration);
			toast.show();
		} catch (Exception e) {
			Log.e("wish4me-postFacebookID", e.toString());
			Context context = getApplicationContext();
			CharSequence text = "General error occured : " + e.toString();
			int duration = Toast.LENGTH_LONG;
			Toast toast = Toast.makeText(context, text, duration);
			toast.show();
		}
		return responseText;

	}


}
