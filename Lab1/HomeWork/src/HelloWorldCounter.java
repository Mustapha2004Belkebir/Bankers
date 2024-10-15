package src;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class HelloWorldCounter {
    private int counter = 0;

    public static void main(String[] args) {
        // Create a new instance of HelloWorldCounter
        new HelloWorldCounter().createGUI();
    }

    public void createGUI() {
        // Create the main frame (window)
        JFrame frame = new JFrame("Hello World Counter");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 200);

        // Create a label that displays the message
        JLabel label = new JLabel("Hello, World!", SwingConstants.CENTER);
        label.setFont(new Font("Serif", Font.PLAIN, 24));

        // Create a button that increments the counter
        JButton button = new JButton("Click me! Count: 0");

        // Set the action for the button
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Increment the counter and update the button text
                counter++;
                button.setText("Click me! Count: " + counter);
            }
        });

        // Add the label and button to the frame
        frame.setLayout(new BorderLayout());
        frame.add(label, BorderLayout.CENTER);
        frame.add(button, BorderLayout.SOUTH);

        // Make the frame visible
        frame.setVisible(true);
    }
}
