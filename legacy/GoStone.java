package marek.go;

public class GoStone {
	private boolean color;
	private int x_position;
	private int y_position;
	
	public GoStone(){
	}
	
	public GoStone(boolean color, int x_position, int y_position){
		this.color = color;
		this.x_position = x_position;
		this.y_position = y_position;
	}
	
	//True iff the stone is white.
	public boolean getColor(){
		return this.color;
	}
	
	public int get_x(){
		return this.x_position;
	}
	
	public int get_y(){
		return this.y_position;
	}
	
	public static int[] get_xy(String stonePosition){
		int[] positions = new int[2];
		positions[0] = stonePosition.charAt(0) - 'a' + 1;
		positions[1] = stonePosition.charAt(1) - 'a' + 1;
		return positions;
	}
	
	public static String getStonePosition(int[] xy){
		char x_pos = ((char) (xy[0] - 1 + 'a'));
		char y_pos = ((char) (xy[1] - 1 + 'a'));
		return Character.toString(x_pos) + Character.toString(y_pos);
	}
	

}
