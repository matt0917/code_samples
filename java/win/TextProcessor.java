package win;

//import java.io.IOException;
//import java.nio.file.Files;
//import java.nio.file.Path;
//import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Set;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


public class TextProcessor {
	// symbolic constant
	public static final Pattern P1 = Pattern.compile("[a-zA-Z]+");
	
	// static variable
	public static char[] alphabet = "abcdefghijklmnopqrstuvwxyz".toCharArray();
	
	// instance variable
	private String textContent;
	private int mostFrequentLetterCount;
	private int mostFrequentWordCount;
	private HashMap<Character, Integer> letterMap;
	private HashMap<String, Integer> wordMap;
	
	
	// constructor
	public TextProcessor() {
		letterMap = new HashMap<Character, Integer>();
		wordMap = new HashMap<String, Integer>();
	}
	
	/**
	 * getter
	 * @return testContent
	 */
	public String getTextContent() {
		return textContent;
	}
		
	/**
	 * setter
	 * set the textContent
	 */
	public void setTextContent(String text) {
		textContent = text;
	}
	
	/**
	 * @return the mostFrequentLetterCount
	 */
	public int getMostFrequentLetterCount() {
		return mostFrequentLetterCount;
	}

	/**
	 * @return the mostFrequentWordCount
	 */
	public int getMostFrequentWordCount() {
		return mostFrequentWordCount;
	}

	/**
	 * @return the letterMap
	 */
	public HashMap<Character, Integer> getLetterMap() {
		return letterMap;
	}

	/**
	 * @return the wordMap
	 */
	public HashMap<String, Integer> getWordMap() {
		return wordMap;
	}

	public void buildLetterMap(String st) {
		st = st.toLowerCase();
		for (int i=0; i < st.length(); i++) {
			char c = st.charAt(i);
			if (isLetter(c)) {				
//				if (!letterMap.containsKey(c)) {
//					letterMap.put(c, 1);
//				} else {
//					letterMap.put(c, letterMap.get(c) + 1);
//				}
				// this is the ternary method simpler version of the above
				letterMap.put(c, letterMap.containsKey(c) ? letterMap.get(c)+1 : 1);
			}
		}
	}
	
	public void buildWordMap(String st) {
		st = st.toLowerCase();
		Matcher matcher = P1.matcher(st);
		while (matcher.find()) {
			String word = matcher.group();
			wordMap.put(word, wordMap.containsKey(word) ? wordMap.get(word)+1 : 1);
		}
	}
	
	/**
	 * return letterMap
	 * @param st
	 * @return
	 */
	public void histogramOfLetters() {
		Set<Character> keySet = letterMap.keySet();
		int i = 0;
		for (Character l : keySet) {
			++i;
			System.out.println(String.format("%d. %c : %d", i, l, letterMap.get(l)));
		}
	}
	
	/**
	 * return wordMap
	 * @param st
	 * @return
	 */
	public void historgramOfWords() {
		Set<String> keySet = wordMap.keySet();
		int i = 0;
		for (String w : keySet) {
			++i;
			System.out.println(String.format("%d. %s : %d", i, w, wordMap.get(w)));
		}
	}
	
	/**
	 * 
	 * @param st
	 * @return
	 */
	public String mostFrequentWord() {
		String mostFrequentWord = null;
		Set<String> keySet = wordMap.keySet();
		for (String w : keySet) {
			if (wordMap.get(w) > mostFrequentWordCount) {
				mostFrequentWord = w;
				mostFrequentWordCount = wordMap.get(w);
			}
		}
		return mostFrequentWord;
	}
	
	/**
	 * 
	 * @param st
	 * @return
	 */
	public Character mostFrequentLetter() {
		char mostFrequentCharacter = '\u0000';
		Set<Character> keySet = letterMap.keySet();
		for (Character c : keySet) {
			if (letterMap.get(c) > mostFrequentLetterCount) {
				mostFrequentCharacter = c;
				mostFrequentLetterCount = letterMap.get(c);
			} 
		}
		return mostFrequentCharacter;
	}
	
//	/**
//	 * Read the file using Paths class
//	 * @param filePath
//	 * @return
//	 */
//	private String readFile(String filePath) {
//		String content = "";
//		Path path = Paths.get(filePath).toAbsolutePath();
//		try {
//			content = new String (Files.readAllBytes(path));
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//		return content;
//	}
	
	/**
	 * Using binarySearch to find a key from an array is the least time cost compare to loop, List, HashSet
	 * @param c
	 * @return
	 */
	private boolean isLetter(char c) {
		int result = Arrays.binarySearch(alphabet, c);
		if (result > 0)
			return true;
		else
			return false;
	}
}


























