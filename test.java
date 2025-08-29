import java.util.Scanner;
public class test {
    public static void main(String[] args) {
            Scanner scanner = new Scanner(System.in);
            System.out.print("What item are you buying?:  ");
            String item = scanner.next();
            System.out.print("What is the cost of the item are you buying?:  ");
            double cost = scanner.nextFloat();
            System.out.print("How many of the item are you buying?:  ");
            int quantity = scanner.nextInt();
            System.out.println("You are buying " + quantity + " " + item +"(s)" + " for " + cost);
            scanner.close();
            
      
        }
    }
