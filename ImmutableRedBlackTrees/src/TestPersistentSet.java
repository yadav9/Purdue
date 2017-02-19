import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashSet;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.Test;


public class TestPersistentSet {

	private void inOrderTraversal(ArrayList<Integer> inOrderOutput, RedBlackTree tree)
	{
		if(tree == null)
			return;
		inOrderTraversal(inOrderOutput, tree.left);
		if(tree.val != Integer.MAX_VALUE)
			inOrderOutput.add(tree.val);
		inOrderTraversal(inOrderOutput, tree.right);
	}
	
	private boolean isSorted(ArrayList<Integer> inOrderOutput)
	{
		int prev = inOrderOutput.get(0);
		int curr;
		for(int i = 1; i < inOrderOutput.size(); ++i)
		{
			curr = inOrderOutput.get(i);
			if(curr < prev)
			{
				return false;
			}
			prev = curr;
		}
		return true;
	}
		
	@Test
	public void test() 
	{
	
		ArrayList<Integer> miniInput = new ArrayList<Integer>();
		miniInput.add(11);
		miniInput.add(12);
		miniInput.add(10);

		PersistentSet miniTest = new PersistentSet(miniInput);
		assertEquals(11, miniTest.getTree().val);
		assertEquals(10, miniTest.getTree().left.val);
		assertEquals(12, miniTest.getTree().right.val);	
		
		ArrayList<Integer> largeInput = new ArrayList<Integer>();
		for(int i = 0; i < 1000; ++i)
		{
			largeInput.add((int) Math.random() - 1000);
		}
		PersistentSet largeTest = new PersistentSet(largeInput);
		ArrayList<Integer> inOrderOutput = new ArrayList<Integer>();
		inOrderTraversal(inOrderOutput, largeTest.getTree());
		
		assertEquals(isSorted(inOrderOutput), true);	//Checks if the tree created is BST
		largeInput.add(1000);
		largeTest.add(1000);
		assertEquals(isSorted(inOrderOutput), true);	//check if add works
	
		largeInput.remove(1000);
		largeTest.remove(1000);
		assertEquals(isSorted(inOrderOutput), true);	//check if remove works	
		
		largeTest.iterator();
		assertEquals(largeTest.hasNext(), true);		//check if iterator is initialized correctly
		
	}

}
