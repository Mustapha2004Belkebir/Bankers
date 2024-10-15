import javax.swing.*;
import java.io.*;
import java.awt.*;

public class ReadFileApp {

    private static final String EXECUTION_COUNT_FILE = "executionCount.txt";  
    private static final String TEXT_FILE = "textFile.txt";  

    public static void main(String[] args) {
        
        int executionCount = readExecutionCount();
        executionCount++;
        writeExecutionCount(executionCount);

        
        String fileContent = readTextFileContent();
        
        
        System.out.println(fileContent + " " + executionCount);
        
    }

    private static String readTextFileContent() {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(TEXT_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
            return "Error: Could not read the file!";
        }
        return content.toString().trim();  
    }

    
    private static int readExecutionCount() {
        try (BufferedReader reader = new BufferedReader(new FileReader(EXECUTION_COUNT_FILE))) {
            return Integer.parseInt(reader.readLine());
        } catch (IOException | NumberFormatException e) {
            return 0;
        }
    }

    private static void writeExecutionCount(int count) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(EXECUTION_COUNT_FILE))) {
            writer.write(String.valueOf(count));
        } catch (IOException e) {
            System.err.println("Error writing execution count: " + e.getMessage());
        }
    }

}
