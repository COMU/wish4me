package com.wish4me.android;


import java.io.IOException;
import android.view.View.OnClickListener;

import java.io.StringReader;

import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;


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
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;


import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;

import android.util.Log;

import android.view.View;
import android.view.ViewGroup;

import android.widget.ImageView;

import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.koushikdutta.urlimageviewhelper.UrlImageViewHelper;

public class UserHomeActivity extends Activity {
	private String session_id;
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.userhome);
	    Bundle extras = getIntent().getExtras();
	    if(extras !=null) {
	    	session_id = extras.getString("session_id");
	    }
	    updateView();

	}
	
    private String getMywishes() {
    	// Create a new HttpClient and Post Header
    	HttpClient httpclient = new DefaultHttpClient();
    	HttpPost httppost = new HttpPost("http://"+Wish4meAndroidActivity.SERVERIP+"/android/listmywishes");
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

    public Document getDomElement(String xml){
        Document doc = null;
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try {
 
            DocumentBuilder db = dbf.newDocumentBuilder();
 
            InputSource is = new InputSource();
                is.setCharacterStream(new StringReader(xml));
                doc = db.parse(is);
 
            } catch (ParserConfigurationException e) {
                Log.e("Error: ", e.getMessage());
                return null;
            } catch (SAXException e) {
                Log.e("Error: ", e.getMessage());
                return null;
            } catch (IOException e) {
                Log.e("Error: ", e.getMessage());
                return null;
            }
                // return DOM
            return doc;
    }
    
    public String getValue(Element item, String str) {
        NodeList n = item.getElementsByTagName(str);
        return this.getElementValue(n.item(0));
    }
     
    public final String getElementValue( Node elem ) {
             Node child;
             if( elem != null){
                 if (elem.hasChildNodes()){
                     for( child = elem.getFirstChild(); child != null; child = child.getNextSibling() ){
                         if( child.getNodeType() == Node.TEXT_NODE  ){
                             return child.getNodeValue();
                         }
                     }
                 }
             }
             return "";
      }
    
    private void scaleImage(ImageView view, int boundBoxInDp)
    {
        // Get the ImageView and its bitmap
        Drawable drawing = view.getDrawable();
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
    	setContentView(R.layout.mywishes);

        ViewGroup parent = (ViewGroup) findViewById(R.id.mywishes_linear_layout);
        
        
        
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
					Wish4meAndroidActivity.class);
    	    startActivity(intent);
    	    finish();
    	    return;
    	}
    	Document doc = getDomElement(xml); // getting DOM element
    	 
    	NodeList nl = doc.getElementsByTagName(KEY_WISH);
    	 
    	// looping through all item nodes <item>
    	for (int i = 0; i < nl.getLength(); i++) {
    		Element e = (Element) nl.item(i);
    	    String name = getValue(e, KEY_NAME); // name child value
    	    String brand = getValue(e, KEY_BRAND); // cost child value
    	    String description = getValue(e, KEY_DESC); // description child value
    	    NodeList nPhoto = e.getElementsByTagName(KEY_PHOTO);
    	    List<String>photos = new ArrayList<String>();
    	    for (int j = 0; j < nPhoto.getLength(); j++) {
    	    	e = (Element) nPhoto.item(j);
    	    	photos.add(getValue(e, KEY_PHOTO));
    	    }
    	    //LayoutInflater inflater = (LayoutInflater)getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    	    
    	    //View view = LayoutInflater.from(getBaseContext()).inflate(R.layout.userhome, parent, true);
    	    View view = View.inflate(this, R.layout.userhome, parent);
    	    view = parent.getChildAt(parent.getChildCount()-1);

    	    view.setOnClickListener(new OnClickListenerWithInt(i));
			
    	    //View view = inflater.inflate(R.layout.userhome, parent); 
    	    TextView wishName = (TextView)view.findViewById(R.id.wish_name);
    	    wishName.setText((CharSequence)name);
    	    TextView wishBrand = (TextView)view.findViewById(R.id.wish_brand);
    	    wishBrand.setText((CharSequence)(brand+" "));
    	    TextView wishDescription = (TextView)view.findViewById(R.id.wish_description);
    	    wishDescription.setText((CharSequence)description);
    	    ImageView wishPhoto = (ImageView)view.findViewById(R.id.wish_image);
    	    if(photos.size() > 0){
    	    	UrlImageViewHelper.setUrlDrawable(wishPhoto,photos.get(0));
    	    	scaleImage(wishPhoto, 100);
    	    	Log.e("wish4me-wishimage", "for wish named "+name+", photo is "+photos.get(0));
    	    }
    	    //parent.addView(view);

    	}
    }
 
}
