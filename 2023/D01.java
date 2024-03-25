import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

public class D01 {

  public static void main(String[] args) {
    String inputFile = "data/D01_input.txt";
    int sum = 0;
    int sumCorrected = 0;

    try (BufferedReader br = new BufferedReader(new FileReader(inputFile))) {
      String line;
      while ((line = br.readLine()) != null) {
        // Part one counts
        int firstDigit = extractFirstDigit(line);
        int lastDigit = extractLastDigit(line);
        int calibrationValue = combineDigits(firstDigit, lastDigit);
        sum += calibrationValue;

        // Part two counts
        String lineCorrected = convertToNumeric(line); // all to digits
        int firstDigitCorrected = extractFirstDigit(lineCorrected);
        int lastDigitCorrected = extractLastDigit(lineCorrected);
        int calibrationValueCorrected = combineDigits(firstDigitCorrected, lastDigitCorrected);
        sumCorrected += calibrationValueCorrected;
      }
    } catch (IOException e) {
      e.printStackTrace();
    }

    // Part one result
    System.out.println("Sum of all the calibration values: " + sum);
    System.out.println();

    // Part two pre-test
    String example = "7twoneight8nnine";
    System.out.println("Example: " + example);
    System.out.println("Expected output: " + "721889");
    String convertedLine = convertToNumeric(example);
    System.out.println("Actual output: " + convertedLine);
    System.out.println();

    // Part two result
    System.out.println("Sum of all the calibration values (lettre-digits corrected): " + sumCorrected);
    System.out.println();
  }

  private static String convertToNumeric(String line) {
    // Define mappings for spelled-out numbers to digits
    String[] numbers = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

    // Replace spelled-out numbers with digits, favoring the first appearance
    boolean foundDigit = true; // boost the loop
    while (foundDigit) {
      foundDigit = false; //pause the loop

      int firstIndexInLine = line.length(); // initialize to the length of the line
      String numberToReplace = null;
      // Check each spelled-out number
      for (String number : numbers) {
        // Check if the current spelled-out number exists in the line
        if (line.contains(number)) {
          // Find the index of the current spelled-out number in the line
          int index = line.indexOf(number.charAt(0));
          // If the number is found and its index is smaller than the smallest index found so far
          if (index != -1 && index < firstIndexInLine) {
            firstIndexInLine = index;
            numberToReplace = number;
            foundDigit = true; // set foundDigit to true to continue the loop
          }
        }
      }
      // If a spelled-out number was found, replace it with its corresponding digit
      if (foundDigit) {
        String digitString = String.valueOf(Arrays.asList(numbers).indexOf(numberToReplace) + 1);
        line = line.replaceFirst(numberToReplace, digitString);
        // System.out.println(line);
      }
    }

    return line;
  }

  private static int extractFirstDigit(String line) {
    for (char c : line.toCharArray()) {
      if (Character.isDigit(c)) {
        return Character.getNumericValue(c);
      }
    }
    return -1; // no digit found
  }

  private static int extractLastDigit(String line) {
    for (int i = line.length() - 1; i >= 0; i--) {
      char c = line.charAt(i);
      if (Character.isDigit(c)) {
        return Character.getNumericValue(c);
      }
    }
    return -1; // no digit found
  }

  private static int combineDigits(int firstDigit, int lastDigit) {
    if (firstDigit == -1 || lastDigit == -1) {
      return 0; // return 0 if any of the digits is not found
    }
    return firstDigit * 10 + lastDigit;
  }

}
