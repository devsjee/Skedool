import java.io.*;
import java.util.*;


import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;

public class splitmailText {
	public static void main(String args[]) throws Exception{
		if (args.length != 2){
			System.out.println("Usage : splitmailText <input_file_name> <output_file_name> ");
			return;
			}
		BufferedReader input_file = new BufferedReader(new FileReader(new File("./"+args[0])));
		BufferedWriter output_file = new BufferedWriter(new FileWriter(new File("./"+args[1])));

		String next_line = null;
		boolean flag = false; 
		 while((next_line = input_file.readLine())!=null)
		 {
		 
		 StringTokenizer st = new StringTokenizer(next_line);

		 if (st.hasMoreTokens())
          	 	{
			String first_word = st.nextToken();
			if (first_word == ">" && !flag)
			{
				output_file.write("Separate Structure");
				flag = true;
			}
			
			while (st.hasMoreTokens())
			{
			String next_word = st.nextToken();
			if (next_word != ">")
				output_file.write(next_word+" ");
			
			}	
			}
		 output_file.write("\n");
  		 output_file.flush();
		
		 }			 
		 
		input_file.close();
		output_file.close();
	}
}
