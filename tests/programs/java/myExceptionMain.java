public class myExceptionMain {

    public static void main(String[] args) {
        try{
            throw new myException();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}