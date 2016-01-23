package marek.go;

import java.util.ArrayList;
import java.util.Random;

import marek.go.SGFNode.SGF_PROPERTIES;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;

public class GoProblemBoardView extends GoBoardView {
	private SGFNode goProblem;
	private SGFNode currentNode;
	private int tranformation;
	
	public GoProblemBoardView(Context context, AttributeSet attrs){
		super(context, attrs);
		tranformation = 0;
		
	}
	
	public void addGoProblem(SGFNode goProblem)
	{
		this.goProblem = goProblem;
		this.currentNode = goProblem;
		if(this.goProblem.getProperty(SGF_PROPERTIES.SIZE) != null)
			this.boardSide = Integer.parseInt(
					this.goProblem.getProperty(SGF_PROPERTIES.SIZE)
					.get(0));
	}
	
	public void setUpGoProblem(){
		
    	for (String whiteStone : this.goProblem.getProperty(SGFNode.SGF_PROPERTIES.ADD_WHITE)){
    		int[] stonePosition = GoStone.get_xy(whiteStone);
    		this.addStone(new GoStone(true, stonePosition[0], stonePosition[1]));
    	}
    	for (String whiteStone : this.goProblem.getProperty(SGFNode.SGF_PROPERTIES.ADD_BLACK)){
    		int[] stonePosition = GoStone.get_xy(whiteStone);
    		this.addStone(new GoStone(false, stonePosition[0], stonePosition[1]));
    	}
    	//Draw the stones.
    	this.invalidate();
	}
	
	public String getCurrentComment(){
		ArrayList<String> comments;
		
		comments = this.currentNode.getProperty(SGF_PROPERTIES.COMMENT);
		if (comments == null)
			return "";
		return comments.get(0);
	}
	
	public void setRandomTransform(){
		/*
		 * Set up a random combination of hor, vert and diag flips.
		 */
		this.tranformation = new Random().nextInt(8);
	}
	
	public void applyTransformToProblem(){
		/*
		 * Applies any tranformation that we've set, and redraws the board.
		 * Note: Removes any stones placed by the user.
		 */
		
		//No need to do anything if there is no transformation.
		if (this.tranformation == 0)
			return;
		
		//First we clear all the stones.
		this.stones.clear();
		
		//Then we apply the tranformation to the GoProblem.
		this.goProblem.applyTransformation(this);
		
		//Finally we reset the GoProblem.
		this.setUpGoProblem();
	}

	public String transform(String currentPosition){
		/*
		 * Transforms the current string by applying a random subset of a horizontal,
		 * vertical, and diagonal flip, based on the stored transformation integer.
		 */
		int currentTransformation = this.tranformation;
		int[] positions = GoStone.get_xy(currentPosition);
		
		//First we do the vertical flip.
		if(currentTransformation % 2 == 1)
			positions[1] = this.flipVertical(positions[1]);
		currentTransformation /= 2;
		
		//Next we do the horizontal flip.
		if(currentTransformation % 2 == 1)
			positions[0] = this.flipHorizontal(positions[0]);
		currentTransformation /= 2;
				
		//Finally we do the diagonal flip.
		if(currentTransformation % 2 == 1)
			positions = this.flipDiagonal(positions);
		
		return GoStone.getStonePosition(positions);
	}
	
	
	//Assumes pos is a vertical position and returns the mirror position.
	//Distinct from flipHorizontal in case of rectangular boards.
	private int flipVertical(int pos){
		return pos + 2*(this.boardSide/2 - pos + 1); //The + 1 is because we're counting from 1, not 0.
	}
	
	//Assumes pos is a horizontal position and returns the mirror position.
	//Distinct from flipVertical in case of rectangular boards.
	private int flipHorizontal(int pos){
		return pos + 2*(this.boardSide/2 - pos + 1); //The + 1 is because we're counting from 1, not 0.
	}
	
	private int[] flipDiagonal(int[] stonePosition){
		int[] retArray = {stonePosition[1], stonePosition[0]};
		return retArray;
	}
	
	private void performNextMove(){
		SGFNode currentChild;
		ArrayList<String> stonePosition;
		int stoneCoordinates[] = {-1, -1};
		boolean stoneColour = false;
		String msg;
		
		//If there are no children, there is no move to do.
		if(this.currentNode.children == null)
		{
			this.showToastMessage("Congratulations, you appear to have reached the end of the problem.");
			return;
		}
		
		//Otherwise we try and find out what the move is.
		currentChild = this.currentNode.children.get(0);
		stonePosition = currentChild.getProperty(SGF_PROPERTIES.BLACK);
		
		//If the stone is not black, then it is white.
		if (stonePosition == null)
		{
			stonePosition = currentChild.getProperty(SGF_PROPERTIES.WHITE);
			stoneColour = true;
		}
		
		//If the position is still null, then probably the problem is done.
		if (stonePosition == null)
		{
			this.showToastMessage("Congratulations, you appear to have reached the end of the problem, although something appears to exist still. What?");
			return;
		}
		//Otherwise we need to play the computers move, if one exists.
		stoneCoordinates = GoStone.get_xy(stonePosition.get(0));
		//More debugging. This should never happen.
		if(stoneCoordinates[0] == -1)
		{
			this.showToastMessage("This should never happen. We appear to have a stone position, but the conversion has fucked up");
			return;
		}
				
		//Updating the board so that it has the done the computers move.
		this.addStone(new GoStone(stoneColour, stoneCoordinates[0], stoneCoordinates[1]));
		//Update the current node.
		this.currentNode = currentChild;
		//Show it to the user.
		this.invalidate();
		
		//If there's a comment, why not show it?
		msg = this.getCurrentComment();
		if (msg != "")
			this.showToastMessage(msg);
	}
	
	@Override
	public boolean onTouchEvent(MotionEvent event) {
		ArrayList<String> stonePosition;
		int stoneCoordinates[] = {-1, -1};
		String msg;
		boolean stoneColour = false;
		SGFNode currentChild;
		
		//first we figure what square we just touched.
		int x_pos = Math.round(event.getX()/(float)(((GoBoardView)this).gridSize));
		int y_pos = Math.round(event.getY()/(float)(this.gridSize));
		
		//Now if there is no stone present we add a new stone to our HashMap.
		//Pair<Integer, Integer> position = new Pair<Integer, Integer> (x_pos, y_pos);
		/*Log.v("Current Position", Integer.toString(x_pos) + "," + Integer.toString(y_pos));
		Log.v("Hashcode of Position", Integer.toString(position.hashCode()));
		Log.v("Result of containsKey", Boolean.toString(this.stones.containsKey(position)));
		Log.v("Result of !this.stones.containsKey(position)", Boolean.toString(!this.stones.containsKey(position)));//*/
		
		if(this.currentNode.children == null)
		{
			this.showToastMessage("You've reached the end of the problem dude!");
			return false;
		}
				
		//We check every child to see if the user clicked on one of the branches represented by the children.
		for(int i = 0; i < this.currentNode.children.size(); i++)
		{
			currentChild = this.currentNode.children.get(i);
			//First, we get the position in the child.
			stonePosition = currentChild.getProperty(SGF_PROPERTIES.BLACK);
			//If the stone is not black, then it is white.
			if (stonePosition == null)
			{
				stonePosition = currentChild.getProperty(SGF_PROPERTIES.WHITE);
				stoneColour = true;
			}
			//If the stone position is still null, we wait until we hit another child.
			//Otherwise, we let the user know which branch they are on, and play the next move if there is one.
			if (stonePosition != null)
				stoneCoordinates = GoStone.get_xy(stonePosition.get(0));
			
			//Coordinates cannot be -1, so this block is never executed if we didn't find the stone.
			//But if we did, we update the board, show a toast, wait a bit, and then do another move.
			if (x_pos == stoneCoordinates[0] && y_pos == stoneCoordinates[1]){
				//Add the stone.
				this.addStone(new GoStone(stoneColour, stoneCoordinates[0], stoneCoordinates[1]));
				//Update the current node.
				this.currentNode = currentChild;
				//Show it to the user.
				this.invalidate();
				//Tell them which branch they are one.
				msg = String.format("This was the expected move for branch %d", i);
				this.showToastMessage(msg);
				msg = this.getCurrentComment();
				if (msg != "")
					this.showToastMessage(msg);
				
				//We show this for half a second before doing the next move.
				this.postDelayed(new Runnable(){
					public void run() {
					performNextMove();
					}
				},500);
				
				//In this case we've chose a branch, so we return. The click is not consumed so that long clicks/etc
				//work.
				return false;
				//TODO Eventually this maybe a double click method.
			}
		}
		
		//If we exit the for loop, the move appeared to be incorrect, or at least not in the problem.
		this.showToastMessage("Apologies, but this move was not foreshadowed by the problem");
		return false;
	}
}
