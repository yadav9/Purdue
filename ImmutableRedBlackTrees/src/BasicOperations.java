
public interface BasicOperations {
	
	/**
	 * 
	 * @param item
	 * @return true for successful add, false otherwise
	 * @throws Exception
	 */
	boolean add(Integer item);
	
	/**
	 * 
	 * @param item
	 * @return true for successful add, false otherwise
	 */
	boolean remove(Integer item);
	
	/**
	 *	to iterate over the tree 
	 */
	void iterator();
	
}
