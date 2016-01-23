package marek.go;

import java.lang.Math;
import java.util.HashMap;

import marek.go.R;
import marek.go.R.color;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import android.util.Pair;
import android.util.Log;

public class GoBoardView extends View{
	protected HashMap<Pair<Integer, Integer>, GoStone> stones;
	protected boolean white; //Is this necessary?
	protected int gridSize;
	protected int boardSize;
	protected int boardSide;

	//Constructor.
	public GoBoardView(Context context, AttributeSet attrs) {
		super(context, attrs);
		this.stones = new HashMap<Pair<Integer, Integer>, GoStone>();
		this.white = false; //Currently hard coding that black is first.
		this.boardSide = 19; //Hardcoding a standard length/width.
	}
	
	public void changeBoardSize(int new_size)
	{
		this.boardSide = new_size;
	}
	
	//What we use to get the current size of the screen.
	//Currently used to figure out what size the gridlines should be.
	@Override 
	protected void onSizeChanged(int w, int h, int oldw, int oldh){
		this.boardSize = Math.min(w,h);
		this.gridSize = this.boardSize/(this.boardSide + 1);
	}

	@Override
	public void onDraw(Canvas canvas){
		//draw wood
		Paint boardColour = new Paint();
		boardColour.setColor(this.getResources().getColor(R.color.board_colour));
		canvas.drawRect(0, 0, this.boardSize, this.boardSize, boardColour);
		
		//draw lines
		Paint lineColour = new Paint();
		lineColour.setColor(this.getResources().getColor(R.color.line_colour));
		//Draw vertical lines.
		for(int i = 1; i < (this.boardSide + 1); ++i){
			canvas.drawLine(this.gridSize*i, this.gridSize,
					this.gridSize*i, this.boardSide*this.gridSize, lineColour);
		}
		//draw horizontal lines.
		for(int i = 1; i < (this.boardSide + 1); ++i){
			canvas.drawLine(this.gridSize, this.gridSize*i, 
					this.boardSide*this.gridSize, this.gridSize*i, lineColour);
		}
		
		//draw star points if full size board.
		if(this.boardSide == 19)
		{
			this.drawThreeStars(canvas, 4, lineColour);
			this.drawThreeStars(canvas, 10, lineColour);
			this.drawThreeStars(canvas, 16, lineColour);
		}
		
		//draw stones.
		
		for (GoStone stone : this.stones.values()) {
			this.drawStone(canvas, stone);
		}
	}
	
	protected void showToastMessage(String msg){
		Context context = this.getContext();
		int duration = Toast.LENGTH_SHORT;
		Toast toast = Toast.makeText(context, msg, duration);
		toast.show();
	}
	
	public void addStone(GoStone stone){
		this.stones.put(new Pair<Integer, Integer>(stone.get_x(), stone.get_y()) , stone);
		String msg = String.format("x_position %d, y_position %d", stone.get_x(), stone.get_y());
		Log.v("addStone StonePositions", msg);
	}
	
	//Draws the given stone on the canvas.
	private void drawStone(Canvas canvas, GoStone stone){
		//Set the stone colour.
		Paint stoneColour = new Paint();
		if (stone.getColor()){
			stoneColour.setColor(this.getResources().getColor(R.color.white_stone_colour));
		}
		else{
			stoneColour.setColor(this.getResources().getColor(R.color.black_stone_colour));
		}
		canvas.drawCircle(stone.get_x()*this.gridSize, stone.get_y()*this.gridSize, 
				(this.gridSize*2)/5, stoneColour);
	}
	
	//Draws three stars on the given row at the appropriate points with the line colour.
	private void drawThreeStars(Canvas canvas, int row, Paint lineColour){
		canvas.drawCircle(this.gridSize*row, this.gridSize*4, this.gridSize/5, lineColour);
		canvas.drawCircle(this.gridSize*row, this.gridSize*10, this.gridSize/5, lineColour);
		canvas.drawCircle(this.gridSize*row, this.gridSize*16, this.gridSize/5, lineColour);
		
		
	}

	@Override
	public boolean onTouchEvent(MotionEvent event) {
		//first we figure what square we just touched.
		int x_pos = Math.round(event.getX()/(float)(this.gridSize));
		int y_pos = Math.round(event.getY()/(float)(this.gridSize));
		
		//Now if there is no stone present we add a new stone to our HashMap.
		Pair<Integer, Integer> position = new Pair<Integer, Integer> (x_pos, y_pos);
		/*Log.v("Current Position", Integer.toString(x_pos) + "," + Integer.toString(y_pos));
		Log.v("Hashcode of Position", Integer.toString(position.hashCode()));
		Log.v("Result of containsKey", Boolean.toString(this.stones.containsKey(position)));
		Log.v("Result of !this.stones.containsKey(position)", Boolean.toString(!this.stones.containsKey(position)));//*/
		if(!this.stones.containsKey(position))
		{
			this.stones.put(position, new GoStone(this.white, x_pos, y_pos));
			//Finally we update the colour.
			this.white = !this.white;
			this.invalidate();
		}
		return false;
	}

}