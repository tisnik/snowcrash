class InteruptException{
    public static void main(String[] args) {
       class inThread extends Thread{
       
           @Override
           public void run() {
               Thread.currentThread().interrupt();
               run();
           }
       };
       Thread th = new inThread();
       th.start();
       
    }
}