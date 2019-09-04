import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
class FileNotFoundException{
    public static void main(String[] agrs){
        File file = new File("jkal");
        try {
            BufferedReader br = new BufferedReader(new FileReader(file));
            br.readLine();
        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }
}
