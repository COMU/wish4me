package com.wish4me.android;


import java.io.IOException;
import java.lang.reflect.Method;
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

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.koushikdutta.urlimageviewhelper.UrlImageViewHelper;

public class UserHomeActivity extends Activity {
	private String session_id;
	private String wish_xml;
	
	public static enum Wishes {
		MYWISHES, FRIENDWISHES
	}
	
	Wishes currentWishes;
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.mywishes);
	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
	    	int temp = extras.getInt("wishes_to_list");
	    	if(temp >= 0 && temp < Wishes.values().length)
	    	    currentWishes = Wishes.values()[temp];
	    	else {
	    		Log.e("wish4me-userHome-oncreate","wishes_to_list value is not passed.");
	    		currentWishes = Wishes.FRIENDWISHES;								//this makes default.
	    	}
		}
	    
		ImageButton addNewWishButton = (ImageButton) findViewById(R.id.add_new_wish_button);
		// Register the onClick listener with the implementation above
		addNewWishButton.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				Intent addNewWishActivity = new Intent(
						UserHomeActivity.this,
						AddWishActivity.class);
				addNewWishActivity.putExtra("session_id", session_id);
				startActivityForResult(addNewWishActivity, 0);
			}
		});
	    
	    updateView();

	}
	
	@Override
	public boolean onPrepareOptionsMenu(Menu menu) {
	    super.onPrepareOptionsMenu(menu);
    	menu.findItem(R.id.menu_listmywishes).setChecked(true);
    	if (currentWishes == Wishes.FRIENDWISHES)
    		menu.findItem(R.id.menu_listfriendswishes).setChecked(true);
	    return true;
	}

	
    private String getMywishes() {
    	// Create a new HttpClient and Post Header
    	HttpClient httpclient = new DefaultHttpClient();
    	HttpPost httppost = new HttpPost("http://"+LoginActivity.SERVERIP+"/android/listfollowingwishes");	// list my wishes by default.
    	if (currentWishes == Wishes.MYWISHES)
    		httppost = new HttpPost("http://"+LoginActivity.SERVERIP+"/android/listmywishes");

    	HttpResponse response = null;
    	String responseText = null;
    	try {
    	    // Add your data
    	    List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
    	    nameValuePairs.add(new BasicNameValuePair("sessionid", session_id));
    	    Log.e("wish4me-UserHome", "List my wishes:session id = "+ session_id);
    	    httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

    	    // Execute HTTP Post Request
    	    response = httpclient.execute(httppost);
        	
        	responseText = LoginActivity.responseToString(response);
		    Log.i("wish4me-UserHome-ResponseText", responseText);

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

    
    private void scaleImage(ImageView view, int boundBoxInDp)
    {
        // Get the ImageView and its bitmap
        Drawable drawing = view.getDrawable();
        if(drawing == null)
        	Log.e("wish4me-scaleimage", "view has no drawable");
        Bitmap bitmap = ((BitmapDrawable)drawing).getBitmap();

        // Get current dimensions
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();

        // Determine how much to scale: the dimension requiring less scaling is
        // closer to the its side. This way the image always stays inside your
        // bounding box AND either x/y axis touches it.
        float xScale = ((float) boundBoxInDp) / width;
        float yScale = ((float) boundBoxInDp) / height;
        float scale = (xScale <= yScale) ? xScale : yScale;

        // Create a matrix for the scaling and add the scaling data
        Matrix matrix = new Matrix();
        matrix.postScale(scale, scale);

        // Create a new bitmap and convert it to a format understood by the ImageView
        Bitmap scaledBitmap = Bitmap.createBitmap(bitmap, 0, 0, width, height, matrix, true);
        BitmapDrawable result = new BitmapDrawable(scaledBitmap);
        width = scaledBitmap.getWidth();
        height = scaledBitmap.getHeight();

        // Apply the scaled bitmap
        view.setImageDrawable(result);

        // Now change ImageView's dimensions to match the scaled image
        RelativeLayout.LayoutParams params = (RelativeLayout.LayoutParams) view.getLayoutParams();
        params.width = width;
        params.height = height;
        view.setLayoutParams(params);
    }

    @SuppressWarnings("unused")
	private int dpToPx(int dp)
    {
        float density = getApplicationContext().getResources().getDisplayMetrics().density;
        return Math.round((float)dp * density);
    }
    
    public void updateView(){

        ViewGroup parent = (ViewGroup) findViewById(R.id.layount_in_scroll);

        
    	// XML node keys
    	final String KEY_WISH = "wish"; // parent node
    	final String KEY_NAME = "name";
    	final String KEY_BRAND = "brand";
    	final String KEY_DESC = "description";
    	//final String KEY_PHOTOS = "photos";
    	final String KEY_PHOTO = "photo";
    	 
    	String xml = getMywishes(); // getting XML
    	if(xml == null){
    	    Context context = getApplicationContext();
    	    int duration = Toast.LENGTH_LONG;
    	    Toast toast = Toast.makeText(context, "connection failed, try again later...", duration);
    	    toast.show();
    	    Intent intent = new Intent(
					UserHomeActivity.this,
					LoginActivity.class);
    	    startActivity(intent);
    	    finish();
    	    return;
    	}
    	wish_xml = xml;								//this is for sending next activity.
    	Document doc = ParseXML.getDomElement(xml); // getting DOM element
    	 
    	NodeList nl = doc.getElementsByTagName(KEY_WISH);
    	if(nl.getLength() == 0) {
    		ImageView noWishToShow = new ImageView(getApplicationContext());
    		noWishToShow.setImageResource(R.drawable.nowish_1);
    		LinearLayout ll = (LinearLayout)findViewById(R.id.layount_in_scroll);
    		ll.addView(noWishToShow);
    	}
    	 
    	// looping through all item nodes <item>
    	for (int i = 0; i < nl.getLength(); i++) {
    		Element e = (Element) nl.item(i);
    	    String name = ParseXML.getValue(e, KEY_NAME); // name child value
    	    String brand = ParseXML.getValue(e, KEY_BRAND); // cost child value
    	    String description = ParseXML.getValue(e, KEY_DESC); // description child value
    	    NodeList nPhoto = e.getElementsByTagName(KEY_PHOTO);
    	    List<String>photos = new ArrayList<String>();
    	    for (int j = 0; j < nPhoto.getLength(); j++) {
    	    	e = (Element) nPhoto.item(j);
    	    	photos.add(ParseXML.getValue(e, KEY_PHOTO));
    	    }
    	    //LayoutInflater inflater = (LayoutInflater)getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    	    
    	    //View view = LayoutInflater.from(getBaseContext()).inflate(R.layout.userhome, parent, true);
    	    View view = View.inflate(this, R.layout.wish_as_list, parent);
    	    view = parent.getChildAt(parent.getChildCount()-1);
    	    
    	    Method createGalleryMethod = null;
			try {
				/*Class<?> c = Class.forName("UserHomeActivity");
				Method  method = c.getDeclaredMethod ("createGalleryMethod", new Class[] {int.class});
				method.invoke (objectToInvokeOn, params)
				*/
				createGalleryMethod = this.getClass().getMethod("createGalleryActivity", new Class[] {int.class});
			    Log.e("wish4me-getMethod", "clicked "+ createGalleryMethod.getName() + " " + createGalleryMethod.getParameterTypes().toString());
			    
				
			} catch (SecurityException e1) {
				Log.e("wish4me-SecurityException", e1.toString());
				e1.printStackTrace();
			} catch (NoSuchMethodException e1) {
				Log.e("wish4me-NoSuchMethodException", e1.toString());
				e1.printStackTrace();
			}

    	    view.setOnClickListener(new OnClickListenerWithInt(i, createGalleryMethod, this));

    	    //View view = inflater.inflate(R.layout.userhome, parent); 
    	    TextView wishName = (TextView)view.findViewById(R.id.wish_name);
    	    wishName.setText((CharSequence)name);
    	    TextView wishBrand = (TextView)view.findViewById(R.id.wish_brand);
    	    wishBrand.setText((CharSequence)(brand+" "));
    	    TextView wishDescription = (TextView)view.findViewById(R.id.wish_description);
    	    wishDescription.setText((CharSequence)description);
    	    ImageView wishPhoto = (ImageView)view.findViewById(R.id.wish_image);
    	    if(photos.size() > 0){
    	    	UrlImageViewHelper.setUrlDrawable(wishPhoto, photos.get(0), R.drawable.wish_icon);
    	    	Log.e("wish4me-wishimage", "for wish named "+name+", photo is "+photos.get(0));
    	    	scaleImage(wishPhoto, 100);
    	    }
    	    photos.clear();
    	    //parent.addView(view);

    	}
    }
    public void createGalleryActivity(int wishID) {
    	
    	String KEY_WISH = "wish";
    	String KEY_PHOTO = "photo";
    	
    	Document doc = ParseXML.getDomElement(wish_xml);
   	 
    	NodeList nl = doc.getElementsByTagName(KEY_WISH);
    	 
    	// looping through all item nodes <item>
    	if(wishID < nl.getLength()) {
    		Element e = (Element) nl.item(wishID);
    	    NodeList nPhoto = e.getElementsByTagName(KEY_PHOTO);
        	Context context = getApplicationContext();
    	    if(nPhoto.getLength() > 0){
    			Intent wishGallery = new Intent(
    					context,
    					WishPhotoGalleryActivity.class);
    			wishGallery.putExtra("wish_xml", wish_xml);
    			wishGallery.putExtra("wish_index", wishID);
    			startActivity(wishGallery);
    			
    	    } else {
    		    int duration = Toast.LENGTH_SHORT;
    		    Toast toast = Toast.makeText(context, "this wish has no image to show", duration);
    		    toast.show();    	    	
    	    }
    	}


    }
 
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.wishestoshow, menu);
        return true;
    }

    private int selectedResolutionItem;
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
    	Intent userHome;
    	UserHomeActivity.Wishes wishes_to_list;
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.menu_listmywishes:
            	if(currentWishes != Wishes.MYWISHES){
					userHome = new Intent(
							UserHomeActivity.this,
							UserHomeActivity.class);
					userHome.putExtra("session_id", session_id);
					wishes_to_list = Wishes.MYWISHES;
					userHome.putExtra("wishes_to_list", wishes_to_list.ordinal());
					startActivity(userHome);
					finish();
				} else {
					Context context = getApplicationContext();
					int duration = Toast.LENGTH_LONG;
					Toast toast = Toast.makeText(context, R.string.already_on_my_wishes, duration);
					toast.show();
				}
                return true;
            case R.id.menu_listfriendswishes:
            	if(currentWishes != Wishes.FRIENDWISHES){
					userHome = new Intent(
							UserHomeActivity.this,
							UserHomeActivity.class);
					userHome.putExtra("session_id", session_id);
					wishes_to_list = Wishes.FRIENDWISHES;
					userHome.putExtra("wishes_to_list", wishes_to_list.ordinal());
					startActivity(userHome);
					finish();
            	} else {
					Context context = getApplicationContext();
					int duration = Toast.LENGTH_LONG;
					Toast toast = Toast.makeText(context, R.string.already_on_friend_wishes, duration);
					toast.show();
            	}
                return true;
            case R.id.menu_select_upload_res:
            	//show a dialogbox with possible resolutions.
            	selectedResolutionItem = getSharedPreferences("Upload_resolution", MODE_WORLD_READABLE).getInt("selected_item", -1);
            	final CharSequence[] digitList = { "640 x 640", "1024 x 1024", "Full Size" };
            	AlertDialog.Builder alt_bld = new AlertDialog.Builder(this);
            	alt_bld.setIcon(R.drawable.icon);
            	alt_bld.setTitle("Select The Maximum Resolution For Upload");
            	
            	alt_bld.setSingleChoiceItems(digitList , selectedResolutionItem,
            	new DialogInterface.OnClickListener() {
            		public void onClick(DialogInterface dialog, int item) {
            			selectedResolutionItem = item;
        			}
        		});
            	alt_bld.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            		public void onClick(DialogInterface dialog, int which) {
            			Toast.makeText(getApplicationContext(),
            					"Selected resolution: " + digitList [selectedResolutionItem],
            					Toast.LENGTH_SHORT).show();
        	        	SharedPreferences mPrefs = getSharedPreferences("Upload_resolution", MODE_WORLD_READABLE);
        				SharedPreferences.Editor editor = mPrefs.edit();
        				switch (selectedResolutionItem) {
        				case 0:
        					editor.putInt("resolution", 640);
        					editor.putInt("selected_item", 0);
        					break;
        				case 1:
        					editor.putInt("resolution", 1024);
        					editor.putInt("selected_item", 1);
        					break;
        				case 2:
        					editor.putInt("resolution", 0);
        					editor.putInt("selected_item", 1);
        					break;
        				default:
        					break;
        				}
        				editor.commit();
            			
            			}
            		});
            	alt_bld.setNegativeButton("Cancel",
            	new DialogInterface.OnClickListener() {
            	public void onClick(DialogInterface dialog, int which) {
            	}
            	});

            	AlertDialog alert = alt_bld.create();
            	alert.show();

            	return true;
            case R.id.menu_logout:
				Intent loginActivity = new Intent(
						UserHomeActivity.this,
						LoginActivity.class);
				loginActivity.putExtra("logout", "true");
				startActivity(loginActivity);
				finish();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
 
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        //Handle the back button
        if(keyCode == KeyEvent.KEYCODE_BACK) {
        	//check if there is a on going upload
        	SharedPreferences mPrefs;
        	mPrefs = getSharedPreferences("backGroundUpload", MODE_WORLD_READABLE);
			if(mPrefs.getBoolean("onGoingUpload", false)){
				Context context = getApplicationContext();
				CharSequence text = "your wish is still uploading...";
				int duration = Toast.LENGTH_LONG;
				Toast toast = Toast.makeText(context, text, duration);
				toast.show();
				return true;
			} else {
	            //Ask the user if they want to quit
	            new AlertDialog.Builder(this)
	            .setIcon(android.R.drawable.ic_dialog_alert)
	            .setTitle(R.string.title_quit)
	            .setMessage(R.string.confirm_quit)
	            .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
	
	                
	                public void onClick(DialogInterface dialog, int which) {
	
	                    //Stop the activity
	                    UserHomeActivity.this.finish();    
	                }
	
	            })
	            .setNegativeButton(R.string.no, null)
	            .show();
	
	            return true;
	        }
        }
        else {
            return super.onKeyDown(keyCode, event);
        }

    }
    
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
    	Intent userHome;
    	UserHomeActivity.Wishes wishes_to_list;
		if (requestCode == 0){
			if (resultCode == RESULT_OK) {
				userHome = new Intent(
						UserHomeActivity.this,
						UserHomeActivity.class);
				userHome.putExtra("session_id", session_id);
				wishes_to_list = Wishes.MYWISHES;
				userHome.putExtra("wishes_to_list", wishes_to_list.ordinal());
				startActivity(userHome);
				finish();
			}

		}
	}

}
