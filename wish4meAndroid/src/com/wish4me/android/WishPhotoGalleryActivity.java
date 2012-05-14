package com.wish4me.android;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.TypedArray;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.BaseAdapter;
import android.widget.Gallery;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

public class WishPhotoGalleryActivity extends Activity {
    private List<Drawable> pics = new ArrayList<Drawable>();
    private List<Uri> picUris = new ArrayList<Uri>();
	private String wish_xml;
	private int wish_index;
	ImageView imageView;
	private SharedPreferences mPrefs;

	
	public static Drawable LoadImageFromWebOperations(String url) {
	    try {
	        InputStream is = (InputStream) new URL(url).getContent();
	        //Drawable d = new BitmapDrawable(decodeInputStream(is));

	        
            //Decode image size
            BitmapFactory.Options o = new BitmapFactory.Options();
            o.inJustDecodeBounds = true;
            BitmapFactory.decodeStream(is, null, o);
            
            is.close();

            int scale = 1;
            if (o.outHeight > LoginActivity.IMAGE_MAX_SIZE || o.outWidth > LoginActivity.IMAGE_MAX_SIZE) {
                scale = (int)Math.pow(2, (int) Math.round(Math.log(LoginActivity.IMAGE_MAX_SIZE / (double) Math.max(o.outHeight, o.outWidth)) / Math.log(0.5)));
            }

            //Decode with inSampleSize
            BitmapFactory.Options o2 = new BitmapFactory.Options();
            o2.inSampleSize = scale;
	        is = (InputStream) new URL(url).getContent();
            Drawable d = new BitmapDrawable(BitmapFactory.decodeStream(is, null, o2));
            is.close();
	        
	        return d;
	    } catch (Exception e) {
	        return null;
	    }
	}

	private void returnPictures(){
		Intent intent = new Intent();
		ArrayList<String> resultList = new ArrayList<String>();
		for(int i = 0; i < picUris.size(); i++)
			resultList.add(picUris.get(i).toString());
		intent.putStringArrayListExtra("image_uris", resultList);
		setResult(RESULT_OK, intent);
		finish();
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

    	    for (int i = 0; i < nPhoto.getLength(); i++) {
    	    	e = (Element) nPhoto.item(i);
    	    	pics.add(LoadImageFromWebOperations(ParseXML.getValue(e, KEY_PHOTO)));

    	    }
    	    
    	}
	}
	
	private File getTempFile(Context context){  
		  //it will return /sdcard/image.tmp  
		  final File path = new File( Environment.getExternalStorageDirectory(), context.getPackageName() );  
		  if(!path.exists()){  
		    path.mkdir();  
		  }  
		  SimpleDateFormat sdf = new SimpleDateFormat("MMdd-HHmmss");
		  String curentDateandTime = sdf.format(new Date());
		  File file = new File(path, curentDateandTime+".jpg");
		  try {
			file.createNewFile();
		} catch (IOException e) {
			e.printStackTrace();
		}
		  return file;
	}  
	
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.wishphotos);
	    mPrefs = getPreferences(MODE_PRIVATE);
	    //pics = new ArrayList<Drawable>();
	    Bundle extras = getIntent().getExtras();
	    imageView = (ImageView)findViewById(R.id.wishImageSelected);
	    ImageButton launchCameraButton = (ImageButton) findViewById(R.id.launch_camera_button);
	    ImageButton addToWishButton= (ImageButton) findViewById(R.id.addtowish_button);
	    if(extras !=null) {
	    	if(extras.getString("add_new_wish") == null) {
	    		launchCameraButton.setVisibility(View.GONE);
	    		addToWishButton.setVisibility(View.GONE);
		    	wish_xml = extras.getString("wish_xml");
		    	wish_index = extras.getInt("wish_index");
		    	fillPicsFromXML();
	    	} else {
	    		pics.clear();
	    		picUris.clear();
				List<String> result = extras.getStringArrayList("image_uris");
				extras.remove("image_uris");
				for(String s:result){
					picUris.add(Uri.parse(s));
					Log.e("wish4me-wishadd-gallery", "added from caller : "+s);
				}
				
				for(int i=0; i < picUris.size();i++){
					imageView.setImageBitmap(WishPhotoGalleryActivity.decodeFile( 
							new File(URI.create(picUris.get(i).toString()))));
					pics.add(imageView.getDrawable());

				}
				
				
	    		launchCameraButton.setOnClickListener(new OnClickListener() {
					
					public void onClick(View v) {
						SharedPreferences.Editor editor = mPrefs.edit();
						editor.putInt("addImage_imageCount", picUris.size());
						Log.e("wish4me-sharedPreferences","addImage-write imageCount"+ " is "+ picUris.size());
						for(int i=0; i < picUris.size(); i++){
							Log.e("wish4me-sharedPreferences","addImage-write image"+i+" is "+ picUris.get(i));
							editor.putString("addImage_image"+i, picUris.get(i).toString());	
						}
						//add file name too.
						File file = getTempFile(getApplication());
						editor.putString("addImage-fileURI", Uri.fromFile(file).toString());
						Log.e("wish4me-sharedPreferences", "addImage-write file is "+Uri.fromFile(file).toString());
						editor.commit();
						
						pics = new ArrayList<Drawable>();
						imageView = (ImageView)findViewById(R.id.wishImageSelected);
						picUris = new ArrayList<Uri>();
						
					    Intent intent = new Intent("android.media.action.IMAGE_CAPTURE");
					    intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(file));
					    
					    startActivityForResult(intent, 0);


					}
				});
	    		
	    		addToWishButton.setOnClickListener(new OnClickListener() {
					
					public void onClick(View v) {
						returnPictures();
						
					}
				});
	    	}
	    }
	    
	    
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

    
    public static Bitmap decodeFile(File f){
        Bitmap b = null;
        try {
            //Decode image size
        	FileInputStream fis = new FileInputStream(f);
        	
            BitmapFactory.Options o = new BitmapFactory.Options();
            o.inJustDecodeBounds = true;
            BitmapFactory.decodeStream(fis, null, o);
            
            fis.close();

            int scale = 1;
            if (o.outHeight > LoginActivity.IMAGE_MAX_SIZE || o.outWidth > LoginActivity.IMAGE_MAX_SIZE) {
                scale = (int)Math.pow(2, (int) Math.round(Math.log(LoginActivity.IMAGE_MAX_SIZE / (double) Math.max(o.outHeight, o.outWidth)) / Math.log(0.5)));
            }

            //Decode with inSampleSize
            BitmapFactory.Options o2 = new BitmapFactory.Options();
            o2.inSampleSize = scale;
            fis = new FileInputStream(f);
            b = BitmapFactory.decodeStream(fis, null, o2);
            fis.close();
        } catch (IOException e) {
        }
        return b;
    }
    
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		if (resultCode == RESULT_OK) {  
		    switch(requestCode){
		      case 0:
		    	  //get old images first:
					int imageCount = mPrefs.getInt("addImage_imageCount", 0);
					Log.e("wish4me-sharedPreferences", "addImage-read image count is : "+imageCount);
					SharedPreferences.Editor editor = mPrefs.edit();
					editor.remove("addImage_imageCount");
					
					
					for(int i=0; i < imageCount; i++){
						picUris.add(Uri.parse(mPrefs.getString("addImage_image"+i, "")));
						Log.e("wish4me-sharedPreferences","addImage-read image"+i+" is "+ picUris.get(i).toString());
						editor.remove("addImage_image"+i);
					}
					String fileURI = mPrefs.getString("addImage-fileURI", "");
					
					File file = new File(URI.create(fileURI));
					editor.remove("addImage-fileURI");

					Log.e("wish4me-sharedPreferences", "addImage-read image file as "+ Uri.fromFile(file));
					editor.commit();
					for(int i=0; i < picUris.size();i++){
						
						imageView.setImageBitmap(decodeFile( 
								new File(URI.create(picUris.get(i).toString()))));
						pics.add(imageView.getDrawable());
					}
					pics.add(new BitmapDrawable(decodeFile(file)));
					
					//Bitmap captureBmp = Media.getBitmap(getContentResolver(), Uri.fromFile(file) );  
					//pics.add(new BitmapDrawable(captureBmp));
					
					picUris.add(Uri.fromFile(file));
					Log.e("wish4me-sharedPreferences","addImage to picUris as "+ Uri.fromFile(file));
					Gallery gallery = (Gallery) findViewById(R.id.wishPhotoGallery);
					((BaseAdapter)gallery.getAdapter()).notifyDataSetChanged();  
			        break;  
			    }  
		  }
	}
	
	 @Override
	    public boolean onKeyDown(int keyCode, KeyEvent event) {
	        //Handle the back button
	        if(keyCode == KeyEvent.KEYCODE_BACK) {
	    	    Bundle extras = getIntent().getExtras();
	    	    if(extras !=null) {
	    	    	if(extras.getString("add_new_wish") != null && pics.size() != 0) {
	    	            //Ask the user if they want to quit
	    	            new AlertDialog.Builder(this)
	    	            .setIcon(android.R.drawable.ic_dialog_alert)
	    	            .setTitle(R.string.title_add_photo)
	    	            .setMessage(R.string.confirm_add_photo)
	    	            .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {

	    	                
	    	                public void onClick(DialogInterface dialog, int which) {
	    	                	returnPictures();
	    	                }

	    	            })
	    	            .setNegativeButton(R.string.no, new DialogInterface.OnClickListener() {

							public void onClick(DialogInterface dialog,
									int which) {
								//return witout sending picUris
								Intent intent = new Intent();
								ArrayList<String> resultList = new ArrayList<String>();
								intent.putStringArrayListExtra("image_uris", resultList);
								setResult(RESULT_OK, intent);
								finish();
							}
	    	            	
	    	            })
	    	            .show();

	    	            return true;
	    	        } else {
	    	            return super.onKeyDown(keyCode, event);
	    	        }
    	    	}
	        }
			return false;

	    }
}
