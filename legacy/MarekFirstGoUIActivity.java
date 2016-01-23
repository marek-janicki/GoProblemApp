package marek.go;

import android.app.Activity;
import android.content.Context;

import java.io.FileInputStream;
import java.util.ArrayList;

import marek.go.R;
import marek.go.fileBrowser.FileActivity;

import android.os.Bundle;
import android.os.Environment;
import android.widget.Button;
import android.widget.Toast;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;

public class MarekFirstGoUIActivity extends Activity {
	
	protected Button zoomInButton;
	protected Button zoomOutButton;
	protected GoProblemBoardView boardView;
	protected SGFNode currentSgfNode;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        
        //For testing, hard code an SGF file, to see what happens.
        try{
        	FileInputStream in = new FileInputStream(FileActivity.chosenFile);
        	this.currentSgfNode = SGFNode.SingleSGFNodeFromFile(in); 
        	}
        catch (Exception e){
        	Context context = getApplicationContext();
    		CharSequence text = e.getMessage();
    		Log.v("OnCreate", e.getMessage());
    		int duration = Toast.LENGTH_LONG;

    		Toast toast = Toast.makeText(context, text, duration);
    		toast.show();
        }
        this.initLayout();
        this.initListeners();
    }
    
    protected void initLayout(){
        setContentView(R.layout.main);
        this.zoomInButton = (Button) this.findViewById(R.id.zoomInButton);
        this.zoomOutButton = (Button) this.findViewById(R.id.zoomOutButton);
        this.boardView = (GoProblemBoardView) this.findViewById(R.id.goProblemBoardView);

        this.boardView.addGoProblem(this.currentSgfNode);
    	this.boardView.setUpGoProblem();
    	//Draw the stones.
    	this.boardView.invalidate();
    	String comment = this.boardView.getCurrentComment();
    	if (comment != ""){
    		Context context = getApplicationContext();
    		int duration = Toast.LENGTH_LONG;

    		Toast toast = Toast.makeText(context, comment, duration);
    		toast.show();
    	}//*/
    }
    	
    protected void initListeners(){
    	this.zoomInButton.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				finish();
			}
    	});
    	this.zoomOutButton.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				boardView.setRandomTransform();
				boardView.applyTransformToProblem();				
			}
    	});
    	
    }
}