// java code to download all files from a list of urls with multithreading
import java.util.*;
import java.util.concurrent.*;
import java.nio.file.*;
import java.net.*;
import java.io.*;
import java.nio.channels.*;

public class Download{
	private static int count = 1;
	public static class ThreadDownloader implements Runnable{
		private Thread curr = null;
		private String url;
		private String id;
		public ThreadDownloader(String url) {
			this.url = url;
			this.id = String.valueOf(count);
			count ++;
		}

		public void start() {
			if(curr == null) {
				System.out.println("Starting download of file " + id);
				curr = new Thread(this, "download-" + id);
				curr.start();
			}
		}

		public void run(){
			Thread currStream = Thread.currentThread();
			try {
				URL website = new URL(url);
				ReadableByteChannel rbc = Channels.newChannel(website.openStream());
				FileOutputStream fos = new FileOutputStream("books/" + id);
				fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
				this.stop();
			} catch (Exception e) {
				System.out.println(e.toString());
				System.out.println("Error while downloading " + id);
			}
		}

		private void stop() {
			System.out.println("Finished downloading file " + id);
		}
	}

	public static void main(String[] args) {
		try{
			ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(16);
	        File f = new File("urls.txt");
	        FileReader fr = new FileReader(f);
	        BufferedReader br = new BufferedReader(fr);
	        String url = new String();
	        while((url = br.readLine()) != null) {
	            ThreadDownloader td = new ThreadDownloader(url);
	            executor.execute(td);
	            // System.out.println(url);
	        }
	        executor.shutdown();
	    } catch (Exception e){
	    	System.out.println("Error while reading URLs");
	    }
	}

}