import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

/**
 * This class performs plagiarism detection using a N-tuple 
 * comparison algorithm allowing for synonyms in the text.
 * @author Kanishk Yadav
 *
 */

public class PlagiarismDetector 
{
	private int tupleLength;
	private String synonymsFileName;
	private HashMap<String, String> synonymsDict;
	
	/**
	 * @param tupleLength
	 * @param synonymsFileName
	 * @param inputFile1
	 * @param inputFile2
	 * @throws IOException 
	 */
	public PlagiarismDetector(String synonymsFileName, int tupleLength) throws IOException
	{
		this.tupleLength = tupleLength;
		this.synonymsFileName = synonymsFileName;
		this.synonymsDict = buildSynonymsDict();
	}
	
	/**
	 * @param synonymsFileName
	 * @throws IOException 
	 */
	public PlagiarismDetector(String synonymsFileName) throws IOException
	{
		this(synonymsFileName, 3);
	}
	
	/**
	 * Creates a dictionary of the synonym words using the file passes in. 
	 * Maps all the synonym words to one synonym word value to make it more space efficient. 
	 * @return
	 * @throws IOException
	 */
	private HashMap<String, String> buildSynonymsDict() throws IOException
	{
		HashMap<String, String> synonymsDict = new HashMap<String, String>();
		try 
		{	
			File inFile = new File(synonymsFileName);
			BufferedReader br = new BufferedReader(new FileReader(inFile));
			String line = null;
			while((line = br.readLine()) != null)
			{
				String[] words = line.split("\\s+");
				for(String item : words)
				{
					synonymsDict.put(item.trim().toLowerCase(), words[0].trim().toLowerCase());			
				}
			}
		} catch (FileNotFoundException e) 
		{
			System.out.println("Cannot find the Synonyms file");
		} 
		return synonymsDict;
	}
	
	/**
	 * Reads from input file and creates a tuple list of tuple strings of given tuple length.
	 * The tuple strings are delimited by space.
	 * @param fileName
	 * @return
	 * @throws IOException
	 */
	private ArrayList<String> createTuplesFromInputFile(String fileName) throws IOException
	{
		ArrayList<String> tupleList = new ArrayList<String>();
		FileInputStream fileIn = new FileInputStream(fileName);
		BufferedReader br = new BufferedReader(new InputStreamReader(fileIn));
		String line = null;
		int counter = 1;
		Queue<String> tupleQueue = new LinkedList<String>();
		
		while((line = br.readLine()) != null)
		{
			String[] words = line.split("\\s+");
			for(String item : words)
			{
				if(synonymsDict.containsKey(item))
				{
					tupleQueue.add(synonymsDict.get(item));
				}
				else
				{
					tupleQueue.add(item.trim().toLowerCase());
				}
				if(counter == tupleLength)
				{
					String temp = "";
					for(String word : tupleQueue)
					{
						temp += word + " ";
					}
					tupleList.add(temp.trim());
					tupleQueue.remove();
					counter = tupleLength - 1;
				}
				++counter;
			}
		}
		return tupleList;	
	}
	
	/**
	 * Performs all the calculation. Creates tuple list of file and check for
	 * common tuple element and returns the % of same tuples.
	 * @param inputFile1
	 * @param inputFile2
	 * @return
	 * @throws IOException
	 */
	public double getPlagiarismAnalysis(String inputFile1, String inputFile2) throws IOException
	{
		ArrayList<String> tupleListOfFile1 = createTuplesFromInputFile(inputFile1);	
		ArrayList<String> tupleListOfFile2 = createTuplesFromInputFile(inputFile2);		
		double matchedTuples = 0;
		Set<String> duplicates = new HashSet<String>();
		for(String item : tupleListOfFile1)
		{
			duplicates.add(item);
		}
		for(String item : tupleListOfFile2)
		{
			if(duplicates.contains(item))
			{
				matchedTuples++;
			}
		}
		double result;
		if(tupleListOfFile1.size() > tupleListOfFile2.size())
		{
			result = Math.round((matchedTuples/tupleListOfFile1.size())*100*100)/100.0;
		}
		else
		{
			result = Math.round((matchedTuples/tupleListOfFile2.size())*100*100)/100.0;
		}
		return result;
	}
	
	/**
	 * Creates an object of PlagiarismDetector and passes in arguments 
	 * to it from command line. Also it does the necessary checks like 
	 * if proper number of command line arguments have been passed or not.
	 * @param args
	 * @throws IOException 
	 * @throws NumberFormatException 
	 */
	public static void main(String[] args) throws NumberFormatException, IOException 
	{
		int argLength = args.length;
		PlagiarismDetector findPlagiarism;
		if(argLength < 3 || argLength > 4)
		{
			System.out.println("Usage: sysnonymsFileName inputFile1 inputFile2 optionalTupleSize");
			return;
		}
		else if(argLength == 4)
		{
			if(Integer.parseInt(args[3]) < 1)
			{
				System.out.println("Tuple Length must be greater than 0");
				return;
			}
			findPlagiarism = new PlagiarismDetector(args[0], Integer.parseInt(args[3]));
		}
		else
		{
			findPlagiarism = new PlagiarismDetector(args[0]);
		}
		System.out.println(findPlagiarism.getPlagiarismAnalysis(args[1], args[2]) + "%");	
	}	
}
