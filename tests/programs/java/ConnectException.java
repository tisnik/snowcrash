import java.net.Socket;
import java.net.SocketAddress;

class ConnectException{
    public static void main(String[] args) {
        try{
        Socket sct = new Socket("localhost",0);
        }catch(Exception e){
            e.printStackTrace();
        }
        
    }
}