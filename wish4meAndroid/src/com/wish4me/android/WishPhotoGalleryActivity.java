package com.wish4me.android;

import java.io.InputStream;
import java.net.URL;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.res.TypedArray;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.BaseAdapter;
import android.widget.Gallery;
import android.widget.ImageView;
import android.widget.Toast;

public class WishPhotoGalleryActivity extends Activity {
    Drawable[] pics;
	private String wish_xml;
	private int wish_index;
	ImageView imageView;
	
	public static Drawable LoadImageFromWebOperations(String url) {
	    try {
	        InputStream is = (InputStream) new URL(url).getContent();
	        Drawable d = Drawable.createFromStream(is, "src name");
	        return d;
	    } catch (Exception e) {
	        return null;
	    }
	}

	private void fillPicsFromXML(){
		// XML node keys
    	String KEY_WISH = "wish"; // parent node
    	/*String KEY_NAME = "name";
    	String KEY_BRAND = "brand";
    	String KEY_DESC = "description";*/
    	//final String KEY_PHOTOS = "photos";
    	String KEY_PHOTO = "photo";

    	if(wish_xml == null){
    	    Context context = getApplicationContext();
    	    int duration = Toast.LENGTH_LONG;
    	    Toast toast = Toast.makeText(context, "internal error!", duration);
    	    toast.show();
    	    Intent intent = new Intent(
					WishPhotoGalleryActivity.this,
					LoginActivity.class);
    	    startActivity(intent);
    	    finish();
    	    return;
    	}
    	
    	Document doc = ParseXML.getDomElement(wish_xml); // getting DOM element
    	 
    	NodeList nl = doc.getElementsByTagName(KEY_WISH);
    	 
    	// looping through all item nodes <item>
    	if(wish_index < nl.getLength()) {
    		Element e = (Element) nl.item(wish_index);
    	    NodeList nPhoto = e.getElementsByTagName(KEY_PHOTO);

    	    pics = new Drawable[nPhoto.getLength()];
    	    for (int i = 0; i < nPhoto.getLength(); i++) {
    	    	e = (Element) nPhoto.item(i);
    	    	pics[i] = LoadImageFromWebOperations(ParseXML.getValue(e, KEY_PHOTO));
    	    }
    	    

    	}
	}
	
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.wishphotos);
	    Context context = getApplicationContext();
	    int duration = Toast.LENGTH_LONG;
	    Toast toast = Toast.makeText(context, "ehe ehe", duration);
	    toast.show();
	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	wish_xml = extras.getString("wish_xml");
	    	wish_index = extras.getInt("wish_index");
	    }
	    fillPicsFromXML();
	    imageView = (ImageView)findViewById(R.id.wishImageSelected);
	    Gallery gallery = (Gallery) findViewById(R.id.wishPhotoGallery);
	    gallery.setAdapter(new ImageAdapter(this));
	    
        gallery.setOnItemClickListener(new OnItemClickListener() {

			public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,
					long arg3) {

				imageView.setImageDrawable(pics[arg2]);
				
			}

        	
        });
	    
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
    		
    		return pics.length;
    	}

    	public Object getItem(int arg0) {
    		
    		return arg0;
    	}

    	public long getItemId(int arg0) {
    		
    		return arg0;
    	}

    	public View getView(int arg0, View arg1, ViewGroup arg2) {
    		ImageView iv = new ImageView(ctx);

			Bitmap bitmap = ((BitmapDrawable) pics[arg0]).getBitmap();
			// Scale it to 50 x 50
			Drawable d = new BitmapDrawable(Bitmap.createScaledBitmap(bitmap, 50, 50, true));
			// Set your new, scaled drawable "d"
    		//iv.setImageDrawable(pics[arg0]);
			iv.setImageDrawable(d);
    		iv.setScaleType(ImageView.ScaleType.FIT_XY);
    		iv.setLayoutParams(new Gallery.LayoutParams(150,120));
    		iv.setBackgroundResource(imageBackground);
    		return iv;
    	}

    }
}
