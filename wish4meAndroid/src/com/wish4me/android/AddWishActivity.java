package com.wish4me.android;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;

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

		Button launchCameraButton = (Button) findViewById(R.id.capture_image_button);
		// Register the onClick listener with the implementation above
		launchCameraButton.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {
			    Intent intent = new Intent("android.media.action.IMAGE_CAPTURE");
			    intent.putExtra(MediaStore.EXTRA_OUTPUT, capturedImage);
			    
			    startActivityForResult(intent, 0);
				
			}
		});
	    

	}
	
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		if (resultCode == Activity.RESULT_OK && requestCode == 0) {
		String result = data.toURI();
		Log.e("wish4me-capture", "result is "+result);
		
		ImageView capturedImageView = (ImageView) findViewById(R.id.captured_image);
		capturedImageView.setImageURI(Uri.parse(result));
		}
		}


}
