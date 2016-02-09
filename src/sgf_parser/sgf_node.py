from ..go_model import *

class SGFNode:
    '''
	This class represents an implied node in an SGF tree.
	The children are represented in an list, with the first element
	of the list representing the A branch (or the correct solution branch)
	Each node has several properties that are stored in a dictionary, whose
    keys come from the class SGF_PROPERTIES dictionary.
	These properties are fixed by the SGF format.
    '''


    SGF_PROPERTIES = {
                       'AB': 'ADD_BLACK',
                       'ADD_BLACK': 'AB',
                       'AW': 'ADD_WHITE',
                       'ADD_WHITE': 'AW',
                       'B': 'BLACK',
                       'BLACK': 'B',
                       'C': 'COMMENT',
                       'COMMENT': 'C',
                       'FF': 'FILE_FORMAT',
                       'FILE_FORMAT': 'FF',
                       'GM': 'GAME',
                       'GAME': 'GM',
                       'PB': 'PLAYER_BLACK',
                       'PLAYER_BLACK': 'PB',
                       'PL': 'PLAYER_TO_PLAY',
                       'PLAYER_TO_PLAY': 'PL',
                       'PW': 'PLAYER_WHITE',
                       'PLAYER_WHITE': 'PW',
                       'SZ': 'SIZE',
                       'SIZE': 'SZ',
                       'W': 'WHITE',
                       'WHITE': 'W',
                     }

    def __init__(self):
        self.children = []
        self.properties = {}
        #Maybe tranformation number if I redo this.

	def SGFParser(String SGFString):
        '''Return an SGFString
        
           TODO: Convert all this Java into python

		 * Requires the input string to contain an entire GameTree.
		 * That is, it must begin with an open parenthesis, and end with the matching parenthesis.
		 */
		SGFNode root = null; //The node that will be returned.
		SGFNode currentNode = null; //The current or more recent Node that was created.
		SGFNode tempNode =null; //Just a temporary node to allow currentNode to be updated.
		
		int currentIndex = 1; //A pointer into SGFString that refers to the beginning of a node or GameTree.
		int currentTerminal = -1;//A pointer into SGFString that refers to the end of a node or GameTree.
		int FirstTerminalGuess = -1; //Used to see if a terminal exists, so that we don't incorrectly assign -1 to terminals.
		int SecondTerminalGuess = -1; //Possibly needed if there is more than one possiblility for the terminal. 
		
		
		
		//Replace all non-space whitespace. Spaces are left because they may be a part of comments.
		//Try this regex
		//   \s+&&[^C\[.*?\]]
		Log.v("SGFParser", SGFString);
		//SGFString = SGFString.replaceAll("\\s+&&[^C\\[.*?\\]]", "");
		//SGFString = SGFString.replaceAll("\\s+", "");
		SGFString = SGFNode.removeNonCommentedWhitespace(SGFString);
		Log.v("SGFParser2", SGFString);
		
		//DEBUG
		if (SGFString.charAt(0) != '(')
			throw new ParseException(String.format("The following String is expected to have an initial (. Instead it is\n%s", SGFString), 0);
		
		
		while(SGFString.charAt(currentIndex) != ')'){
			//DEBUG
			Log.v("SGFParserCurrentSubstring", SGFString.substring(currentIndex));
			if ((SGFString.charAt(currentIndex) != ';')&&(SGFString.charAt(currentIndex) != '(')){
				Log.v("SGFParserString", SGFString);
				Log.v("SGFParserIndex", Integer.toString(currentIndex));
				throw new ParseException(String.format("The following String is expected to have a ( or ; at position %d. Instead it is\n%s", currentIndex, SGFString), currentIndex);
			}
			//If we see a new game tree, we find the matching parenthesis and recurse.
			if (SGFString.charAt(currentIndex) == '('){
				if (root == null)
					throw new ParseException(String.format("The following String appears to start with two open parentheses which is not legal SGF syntax:\n%s", SGFString), 0);
				currentTerminal = SGFNode.findMatchingParen(SGFString, currentIndex);
				if (currentNode.children == null)
					currentNode.children = new ArrayList<SGFNode>();
				currentNode.children.add(new SGFNode(SGFString.substring(currentIndex, currentTerminal)));
				//Right now current Terminal will point to the matching end parenthesis, but we need it to point to the following character.
				currentTerminal++;
			}//Else we've found a node. We find the end point of the node and construct a new node.
			else{
				//Log.v("SGFParserCurrentSubstring", SGFString.substring(currentIndex));
				FirstTerminalGuess = SGFString.indexOf(";", currentIndex + 1);
				SecondTerminalGuess = SGFString.indexOf("(", currentIndex + 1);
				
				//After this block, we should have our best answer so far in First Terminal Guess.
				if (FirstTerminalGuess != -1 && SecondTerminalGuess != -1)
					FirstTerminalGuess = Math.min(FirstTerminalGuess, SecondTerminalGuess);
				else if(FirstTerminalGuess == -1)
					FirstTerminalGuess = SecondTerminalGuess;
				
				SecondTerminalGuess = SGFString.indexOf(")", currentIndex + 1);
				//Now First and Second Terminal Guess possibly contain the best guesses so far  but they may contain -1s, so we check for that.
				
				if (FirstTerminalGuess != -1 && SecondTerminalGuess != -1)
					currentTerminal = Math.min(FirstTerminalGuess, SecondTerminalGuess);
				else if (FirstTerminalGuess == -1)
					currentTerminal = SecondTerminalGuess;
				else 
					currentTerminal = FirstTerminalGuess;
					
				//This block should only happen if we can't fine any appropriate terminal.
				if (currentTerminal == -1)
				{
					Log.v("SGFParserString", SGFString);
					Log.v("SGFParserIndex", Integer.toString(currentIndex));
					throw new ParseException(String.format("The parser cannot find an ; ) or ( denoting an endpoint of the node starting at %d. The string is\n%s", currentIndex, SGFString), currentIndex);	
					
				}
				
				//OLD BUGGED, can incorrectly assign -1 to the terminal.
				//currentTerminal = Math.min(SGFString.indexOf(";", currentIndex + 1), SGFString.indexOf("(", currentIndex + 1));
				//currentTerminal = Math.min(currentTerminal, SGFString.indexOf(")", currentIndex + 1));
				
				//Make a new node.
				tempNode = new SGFNode(SGFString.substring(currentIndex, currentTerminal));
				//Is the root null? If so, set this node to be the root and the currentNode.
				if (root == null){
					root = tempNode;
					currentNode = tempNode;
				}//Otherwise, add this node to the children of currentNode, and then update currentNode.
				else{
					if (currentNode.children == null)
						currentNode.children = new ArrayList<SGFNode>();
					currentNode.children.add(tempNode);
					currentNode = tempNode;
				}
			}
			//Don't need +1 because of differenced in slice notation.
			currentIndex = currentTerminal;
			
		}
		Log.v("SGFParser", "Done Parsing!");
		return root;
	}
	

    pass
public class SGFNode {
	/* 
	This class represents an implied node in an SGF tree.
	The children are represented in an arraylist, with the first element
	of the list representing the A branch (or the correct solution branch)
	Each node has several properties that are stored in a HashMap.
	These properties are fixed by the SGF format.
	The class also includes a static method that 
	*/
	
	public static enum SGF_PROPERTIES {
		ADD_BLACK, ADD_WHITE, BLACK, COMMENT, FILE_FORMAT, GAME, PLAYER_BLACK,
		PLAYER_TO_PLAY, PLAYER_WHITE, NULL, SIZE, WHITE
	}
	
	private static SGF_PROPERTIES[] transformableProperties = 
		{SGF_PROPERTIES.ADD_BLACK, SGF_PROPERTIES.ADD_WHITE, SGF_PROPERTIES.BLACK, SGF_PROPERTIES.WHITE};
	public ArrayList<SGFNode> children;
	private HashMap<SGF_PROPERTIES, ArrayList<String>> propertyMap;
	private int transformation;
	
	public SGFNode(){
		this.children = null;
	}
	
	
	public SGFNode(String properties) throws ParseException{
		/*
		 * properties should only contain the properties of this node. It should not contain any information about its children.
		 * It should not have any initial or trailing whitespace.
		 * Create an SGF node and give it the properties specified in the String.
		 */
		int currentIndex; //Where we are in analysing the string.
		this.children = null;
		this.transformation = 0;
		this.propertyMap = new HashMap<SGF_PROPERTIES, ArrayList<String>>();
		
		currentIndex = properties.indexOf(";") + 1;
		while (currentIndex < properties.length()){
			String currentProperty = SGFNode.getNextProperty(properties, currentIndex);
			int propertyEnd = SGFNode.findEndOfProperty(properties, currentIndex + currentProperty.length());
			//We split on ][. There should be an intial [ and a trailing ] that we shall ignore.
			String[] propertyInformation = properties.substring(currentIndex + currentProperty.length(), propertyEnd).split("\\]\\[");
			Log.v("SGFNodeLineCurrentProperty",currentProperty);
			Log.v("SGFNodeLinePropertyNameBeginning", Integer.toString(currentIndex));
			Log.v("SGFNodeLinePropertyNameEnd", Integer.toString(currentIndex + currentProperty.length()));
			Log.v("SGFNodeLinePropertyEnd", Integer.toString(propertyEnd));
			Log.v("SGFNodeLineProperties", properties.substring(currentIndex + currentProperty.length(), propertyEnd));
			for (int i=0; i < propertyInformation.length; i++)
				Log.v("SGFNodeLine48", propertyInformation[i]);
			Log.v("SGFNodeLine48", propertyInformation.toString());
			
			//DEBUG
			if (propertyInformation[0].charAt(0) != '[') 
				throw new ParseException(String.format("The first character of %s should be a [", propertyInformation[0]),0);
			propertyInformation[0] = propertyInformation[0].substring(1);
			int end = propertyInformation.length - 1;
			if (propertyInformation[end].charAt(propertyInformation[end].length() - 1) != ']') 
				throw new ParseException(String.format("The last character of %s should be a ]", propertyInformation[end]),end);
			propertyInformation[end] = propertyInformation[end].substring(0, propertyInformation[end].length() - 1);
			
			//Now we add the property information to the HashMap
			SGF_PROPERTIES this_property = SGF_PROPERTIES.NULL;
			
			//Switch does not work with Strings, hence the massive if Block.
			if (currentProperty.equals("AB")) this_property = SGF_PROPERTIES.ADD_BLACK;
			if (currentProperty.equals("AW")) this_property = SGF_PROPERTIES.ADD_WHITE;
			if (currentProperty.equals("B")) this_property = SGF_PROPERTIES.BLACK;
			if (currentProperty.equals("C")) this_property = SGF_PROPERTIES.COMMENT;
			if (currentProperty.equals("FF")) this_property = SGF_PROPERTIES.FILE_FORMAT;
			if (currentProperty.equals("GM")) this_property = SGF_PROPERTIES.GAME;
			if (currentProperty.equals("PB")) this_property = SGF_PROPERTIES.PLAYER_BLACK;
			if (currentProperty.equals("PL")) this_property = SGF_PROPERTIES.PLAYER_TO_PLAY;
			if (currentProperty.equals("PW")) this_property = SGF_PROPERTIES.PLAYER_WHITE;
			if (currentProperty.equals("SZ")) this_property = SGF_PROPERTIES.SIZE;
			if (currentProperty.equals("W")) this_property = SGF_PROPERTIES.WHITE;
			
			Log.v("SGFNodeThisProperty",this_property.toString());
			
			//If the property is Null, that means we didn't recognise it, so we ignore it.
			if (this_property != SGF_PROPERTIES.NULL){
				//If we recognise it, we add it to our Hashmap. Note that since some files incorrectly implement the format
				//we might see multiple instances of the same property for a node.
				//this.propertyMap.co
				if (!this.propertyMap.containsKey(this_property))
					this.propertyMap.put(this_property, new ArrayList<String>(Arrays.asList(propertyInformation)));
				else
					((ArrayList<String>)this.propertyMap.get(this_property)).addAll(Arrays.asList(propertyInformation));
			}	
			
			currentIndex = propertyEnd;
		}
		
		
	}
	
	public static SGFNode SingleSGFNodeFromFile(FileInputStream in) throws ParseException, IOException{
		/* 
		 * Requires that a FileInputStream be given from the context.
		 * Requires that a single sgf Node be present in the file.
		 * Create an SGF node and give it the properties specified in the open File.
		 */
		InputStreamReader inputStreamReader = new InputStreamReader(in);
	    BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
	    StringBuilder sb = new StringBuilder();
	    String line;
	    while ((line = bufferedReader.readLine()) != null) {
	        sb.append(line);
	    }
	    
	    return SGFNode.SGFParser(sb.toString().trim());
	}
	
	protected static int findEndOfProperty(String properties, int fromIndex){
		/*Assumes that properties is a string that contains the data of an SGF property. fromIndex is the index
		at which the property begins. Return the index of the last ] of the property.
		Allows for one property to have multiple instances of data, for eg. supports
		"AW[aa][bb][cc][dd]"
		*/
		String currentSubstring = properties.substring(fromIndex, fromIndex + 2);
		Log.v("SGFNodeFindEndOfProperty",properties.substring(fromIndex));
		while (!currentSubstring.matches("\\][A-Z]?") && fromIndex + 2 < properties.length()){//&& !currentSubstring.equals("")){
			fromIndex++;
			currentSubstring = properties.substring(fromIndex, fromIndex + 2);
		}
		if (currentSubstring.matches("\\][A-Z]?"))
			return fromIndex + 1;
		else
			return properties.length();
	}
	
	
	protected static String getNextProperty(String properties, int fromIndex) throws ParseException{
		//TODO Add Comments 
		
		char[] propertyArray = properties.toCharArray();
		
		Log.v("SGFNodeGetNextPropertyProperties", properties.substring(fromIndex));
		Log.v("SGFNodeGetNextPropertyFromIndex", Integer.toString(fromIndex));
		
		//Upon exit we expect to have access to the index of the first Letter in the Property. 
		while (fromIndex < propertyArray.length && !Character.toString(propertyArray[fromIndex]).matches("[A-Z]")){
			fromIndex++;
		}
		
		Log.v("SGFNodeGetNextPropertyFromIndex", Integer.toString(fromIndex));
		
		//This shouldn't happen, but on the off-chance that we miss the end of the properties,
		//We exist.
		if (fromIndex >= propertyArray.length){
			return "";
		}
		int firstLetter = fromIndex;
		
		//Now we want to get the index of the first token after the property is specified.
		while (fromIndex < propertyArray.length && propertyArray[fromIndex] != '['){
			fromIndex++;
		}
		
		Log.v("SGFNodeGetNextPropertyFromIndex", Integer.toString(fromIndex));
		
		//DEBUG code
		if (propertyArray[fromIndex] != '['){
			//throw new ParseException("", 5);
			String msg = String.format("The following String is expected to have an [ at position %d, \n%s", fromIndex, properties);
			Log.v("SGFNodeGetNextProperty", msg);
		    throw new ParseException(msg, fromIndex);
		}
		return properties.substring(firstLetter, fromIndex);
	}
	
	protected static String removeNonCommentedWhitespace(String SGFString){
		/*
		 * Removes all whitespace that is not enclosed in a comment tag. Currently
		 * supports escape braces. So if the white space is not between a C[ and the
		 * first ] that follows a C[ that is not a subset of \] the whitespace is removed.
		 * 
		 */
		
		int currentIndex = 0; //An index to the beginning of the non-formatted string.
		int beginComment = 0; //Index to the beginning of the next comment.
		int endComment = 0; //Index to the end of the next comment.
		String returnString = ""; //The return String
		
		beginComment = SGFString.indexOf("C[", currentIndex);
		
		while(beginComment != -1){
			//First we remove the whitespace up to the comment, and add it to the return string.
			returnString +=  SGFString.substring(currentIndex, beginComment).replaceAll("\\s+", "");
			//Now we find the endpoint of the comment.
			endComment = beginComment;
			endComment = SGFString.indexOf("]", endComment);
			//We check that this is not an escape ].
			while(SGFString.charAt(endComment-1) == '\\' && endComment != -1){
				endComment = SGFString.indexOf("]", endComment + 1);
					}
			//Now we add the comment and update the indices
			returnString += SGFString.substring(beginComment, endComment + 1);
			currentIndex = endComment + 1;
			beginComment = SGFString.indexOf("C[", currentIndex);
		}
		//Finally, we remove the rest of the whitespace.
		returnString +=  SGFString.substring(currentIndex).replaceAll("\\s+", "");
		return returnString;
	}
	
	public static int findMatchingParen(String SGFString, int fromIndex){
		//Return the index of the matching closeParen for the openParen at fromIndex. Requires that such a matching
		//Paren Exists.
		
		//Find the next open and close paren in the string.
		int nextOpenParen = SGFString.indexOf("(", fromIndex + 1);
		int nextCloseParen = SGFString.indexOf(")", fromIndex + 1);
		
		//If the close paren comes first then we're done.
		if (nextCloseParen < nextOpenParen) return nextCloseParen; 
		
		//Otherwise we have one extra open paren, so we need to keep track of this.
		int numSurplus = 1;
		fromIndex = nextOpenParen + 1;
		nextOpenParen = SGFString.indexOf("(", fromIndex);
		
		while (numSurplus > 0 && nextCloseParen < nextOpenParen){
			//Move the current search string to the smaller of the two indices.
			//Increment the surplus if we've consumed an open paren, else decrement the surplus.
			//In either case, find the next open or close paren as required.
			fromIndex = Math.min(nextOpenParen, nextCloseParen) + 1;
			if(nextOpenParen < nextCloseParen){
				numSurplus++;
				nextOpenParen = SGFString.indexOf("(", nextOpenParen + 1);
			}
			else{
				numSurplus--;
				nextCloseParen = SGFString.indexOf(")", nextCloseParen + 1);
			}
		}
		
		return nextCloseParen;
	}

}'''
