package com.wish4me.android;

import java.io.File;
import java.io.IOException;
import java.net.URI;
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
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import com.wish4me.android.UserHomeActivity.Wishes;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.Gallery;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

public class AddWishActivity extends Activity{
	private String session_id;
    private List<Drawable> pics = new ArrayList<Drawable>();
    private List<Uri> picUris = new ArrayList<Uri>();
	
	public void onCreate(Bundle savedInstanceState) {

		super.onCreate(savedInstanceState);
		setContentView(R.layout.addnewwish);

	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
		}

		ImageButton addPhoto = (ImageButton) findViewById(R.id.add_photo_button);
		// Register the onClick listener with the implementation above
		addPhoto.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {

				Context context = getApplicationContext();
    			Intent wishGallery = new Intent(
    					context,
    					WishPhotoGalleryActivity.class);
    			wishGallery.putExtra("add_new_wish", "true");
    			ArrayList<String> resultList = new ArrayList<String>();
    			for(int i = 0; i < picUris.size(); i++)
    				resultList.add(picUris.get(i).toString());
    			wishGallery.putStringArrayListExtra("image_uris", resultList);
    			
    			startActivityForResult(wishGallery,0);
    			//startActivity(wishGallery);
    			
				
			}

		});



		ImageButton addWishButton = (ImageButton) findViewById(R.id.addwish_button);
		// Register the onClick listener with the implementation above
		addWishButton.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {
				postNewWish();
				
			}
		});

		Gallery gallery = (Gallery) findViewById(R.id.addwish_temprory_gallery);
	    gallery.setAdapter(new ImageAdapter(this));

	}
	
	public class ImageAdapter extends BaseAdapter {

    	private Context ctx;
    	int imageBackground;
    	
    	public ImageAdapter(Context c) {
			ctx = c;
			TypedArray ta = obtainStyledAttributes(R.styleable.wishPhotoGallery);
			imageBackground = ta.getResourceId(R.styleable.wishPhotoGallery_android_galleryItemBackground, 1);
			ta.recycle();
		}

		public int getCount() {
    		
    		return pics.size();
    	}

    	public Object getItem(int arg0) {
    		
    		return arg0;
    	}

    	public long getItemId(int arg0) {
    		
    		return arg0;
    	}

    	public View getView(int arg0, View arg1, ViewGroup arg2) {
    		ImageView iv = new ImageView(ctx);
			iv.setImageDrawable(pics.get(arg0));
    		iv.setScaleType(ImageView.ScaleType.CENTER_INSIDE);
    		iv.setLayoutParams(new Gallery.LayoutParams(150,120));
    		iv.setBackgroundResource(imageBackground);
    		return iv;
    	}

    }
	
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		if (requestCode == 0){
			if (resultCode == RESULT_OK) {
				List<String> result = data.getStringArrayListExtra("image_uris");
				data.removeExtra("image_uris");
				pics.clear();
				picUris.clear();
				for(String s:result){
					picUris.add(Uri.parse(s));
					Log.e("wish4me-imageReturn", s);
				}
				
				ImageView tempImageView = new ImageView(getApplicationContext());
				for(int i=0; i < picUris.size();i++){
					
					tempImageView.setImageBitmap(WishPhotoGalleryActivity.decodeFile( 
							new File(URI.create(picUris.get(i).toString()))));
					pics.add(tempImageView.getDrawable());
					Log.e("wish4me-imageReturn-add", "added image "+i);
				}
				
				Gallery gallery = (Gallery) findViewById(R.id.addwish_temprory_gallery);
			    ((BaseAdapter)gallery.getAdapter()).notifyDataSetChanged();
				}
			else{
				
			}
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
			Log.i("wish4me-AddWish-responseText", responseText);
	    	String KEY_WISH = "wish"; // parent node
	    	String KEY_RESULT = "result";
	    	
			Document doc = ParseXML.getDomElement(responseText);
			
			NodeList nl = doc.getElementsByTagName(KEY_WISH);
			String result_status;
			if (nl.getLength() == 1){
				Element e = (Element) nl.item(1);
				result_status = ParseXML.getValue(e, KEY_RESULT);
				if(result_status == "success"){
				    AlertDialog.Builder builder = new AlertDialog.Builder(this);
				    builder.setMessage("Wish Added successfully!").create().show();
				    
				    Intent userHome = new Intent(
							AddWishActivity.this,
							UserHomeActivity.class);
					userHome.putExtra("session_id", session_id);
					UserHomeActivity.Wishes wishes_to_list = Wishes.FRIENDWISHES;
					userHome.putExtra("wishes_to_list", wishes_to_list.ordinal());
					startActivity(userHome);
					finish();
				    
				}
			}
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
