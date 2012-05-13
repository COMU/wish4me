package com.wish4me.android;

import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.BaseAdapter;
import android.widget.Gallery;
import android.widget.ImageView;
import android.widget.Toast;

public class WishPhotoGalleryActivity extends Activity {
    List<Drawable> pics;
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

    	    pics = new ArrayList<Drawable>();
    	    for (int i = 0; i < nPhoto.getLength(); i++) {
    	    	e = (Element) nPhoto.item(i);
    	    	pics.add(LoadImageFromWebOperations(ParseXML.getValue(e, KEY_PHOTO)));
    	    }
    	    

    	}
	}
	
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.wishphotos);
	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	wish_xml = extras.getString("wish_xml");
	    	wish_index = extras.getInt("wish_index");
	    }
	    fillPicsFromXML();
	    imageView = (ImageView)findViewById(R.id.wishImageSelected);
	    Gallery gallery = (Gallery) findViewById(R.id.wishPhotoGallery);
	    gallery.setAdapter(new ImageAdapter(this));
	    gallery.setOnItemSelectedListener(new OnItemSelectedListener() {
			public void onItemSelected(AdapterView<?> arg0, View arg1,
					int arg2, long arg3) {
				imageView.setImageDrawable(pics.get(arg2));
				}

			public void onNothingSelected(AdapterView<?> arg0) {
				if(pics.size() == 0){
					Context context = getApplicationContext();
				    int duration = Toast.LENGTH_LONG;
				    Toast toast = Toast.makeText(context, "this wish has no image", duration);
				    toast.show();
				    return;
				}
				imageView.setImageDrawable(pics.get(0));
			}
	    	
		});
        gallery.setOnItemClickListener(new OnItemClickListener() {

			public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,
					long arg3) {

				imageView.setImageDrawable(pics.get(arg2));
				
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
}
