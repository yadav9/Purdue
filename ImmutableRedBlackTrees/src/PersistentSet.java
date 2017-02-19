import java.util.ArrayList;
import java.util.HashSet;
import java.util.Stack;

/**
 * class to maintain an set
 * based on immutable red black tree
 * supports methods such as add, remove etc
 * @author Kanishk Yadav
 *
 */

public class PersistentSet implements BasicOperations {

    private HashSet<Integer> set = new HashSet<Integer>();;
	private ArrayList<Integer> treeVals = new ArrayList<Integer>();
	private Stack<RedBlackTree> stack;
	private RedBlackTree current;
	private boolean flag = false;
	private RedBlackTree tree;
    
	/**
	 * Constructor with an integer input
	 * @param val
	 * @throws Exception 
	 */
	public PersistentSet(Integer val) 
	{
		this.treeVals.add( val);
		tree = new EmptyRedBlackTree().insert(val);
		set.add(val);
		
	}
	
	/**
	 * Constructor with an ArrayList<Integer> input
	 * @param treeVals
	 */
	public PersistentSet(ArrayList<Integer> treeVals) 
	{
		this.treeVals = treeVals;
		
		int count = 0;
		for(Integer item: this.treeVals)
		{
			if(count == 0)
			{
				tree = new EmptyRedBlackTree().insert(item);
			}
			else
			{
				tree = tree.insert(item);
			}
			count++;
		}
		set.addAll(this.treeVals);
	}	
	
	/**
	 * adds item to immutable red black tree
	 */
	public boolean add(Integer item) 
	{
		this.treeVals.add(item);
		tree.insert(item);
		set.add(item);		
		return true;
	}
	
	/**
	 * removes item from immutable red black tree
	 */
	public boolean remove(Integer item) 
	{		
		this.treeVals.remove(item);
		int count = 0;
		for(Integer item1: this.treeVals)
		{
			if(count == 0)
			{
				tree = new EmptyRedBlackTree().insert(item1);
			}
			else
			{
				tree = tree.insert(item1);
			}
			count++;
		}		
		return true;
	}

	/**
	 * Initializes the stack and current node
	 * for hasNext() and next() method
	 */
	public void iterator() 
	{
		this.current = this.tree;
		stack = new Stack<RedBlackTree>();
		this.flag = true;
	}
	/**
	 * checks if any element left to iterate in tree
	 * @return
	 */
    public boolean hasNext() 
    {
    	if(this.flag == false)
    	{
    		throw new Error("Need to Call iterator() method to use iterator methods");
    	}
    	
        return !stack.isEmpty() || current != null;
    }	
    
    /**
     * Gives the next element in the tree
     * @return
     */
    public Integer next() 
    {
    	if(this.flag == false)
    	{
    		throw new Error("Need to Call iterator() method to use iterator methods");
    	}
    	
        while (!stack.isEmpty() || current != null) 
        {
            if (current != null && current.val != Integer.MAX_VALUE) 
            {
                stack.push(current);
                current = current.left;
            } 
            else 
            {
                current = stack.peek().right;
                break;
            }
        }
        RedBlackTree node = stack.pop();
        return node.val;
    }

    /**
     * Return root node of Red Black Tree
     * @return
     */
    public RedBlackTree getTree()
    {
    	return this.tree;
    }
    /**
     * Return persistent set
     * @return
     */
    public HashSet<Integer> getPersistentSet()
    {
    	return this.set;
    }

}
