import java.util.ArrayList;

/**
 * Class inherits RedBlackTree
 * @author Kanishk Yadav
 */

public class EmptyRedBlackTree extends RedBlackTree {
	
	private static final int RED   = 0;
	private static final int BLACK = 1;
	private static final int NONE = 2;
	final int color;
	
	/**
	 * EmptyRedBlackTree Constructor
	 */
	public EmptyRedBlackTree()
	{
		super(null, Integer.MAX_VALUE, null, NONE);
		this.color = BLACK;
	}
	
	protected boolean isEmpty()
	{
		return true;
	}
	
	/**
	 * Inserts new values to red black tree
	 */
	protected RedBlackTree insert(int value) 
	{
		RedBlackTree temp = new RedBlackTree(new EmptyRedBlackTree(), value, new EmptyRedBlackTree(), RED);
		return temp;
	}
	
	protected RedBlackTree update(RedBlackTree node)
	{
		return node;
	}


}
