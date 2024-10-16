//This is the entry point of the app

public class Calculate {
    public static void main(String[] args) {
        // Check if the correct number of arguments are provided
        if (args.length != 3) {
            System.out.println("Usage: java Calculate <operator> <A> <B>");
            return;
        }

        // Extract operator and operands from the command-line arguments
        String operator = args[0];
        double A, B;

        try {
            A = Double.parseDouble(args[1]);
            B = Double.parseDouble(args[2]);
        } catch (NumberFormatException e) {
            System.out.println("Error: Please enter valid numbers for A and B.");
            return;
        }

        // Instantiate the appropriate Calculator subclass based on the operator
        Calculator calculator = null;

        switch (operator) {
            case "+":
                calculator = new Add();
                break;
            case "-":
                calculator = new Sub();
                break;
            case "*":
                calculator = new Multiply();
                break;
            case "/":
                calculator = new Divide();
                break;
            default:
                System.out.println("Error: Unknown operator. Use +, -, *, or /.");
                return;
        }

        // Perform the calculation and handle exceptions such as division by zero
        try {
            double result = calculator.compute(A, B);
            System.out.println(result);
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
