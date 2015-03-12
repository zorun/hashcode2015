package java_hashcode;

import java.io.*;
import java.util.*;
import java.*;

public class inout {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		List<Integer> list = new ArrayList<Integer>();
		File file = new File("dc.in");
		BufferedReader reader = null;
		int R,S,U,P,M=0,x,y;
	//	int unavail[] = new int[1000];
		Server[] servers = new Server[625];
		int center[][] = new int[1000][1000];
		
		Data_center data_center = new Data_center();
		
		try {
		    reader = new BufferedReader(new FileReader(file));
		    String text = null;
		    text = reader.readLine();
		    String[] initial_list = text.split(" ");
		    data_center.R = Integer.parseInt(initial_list[0]);
		    data_center.S = Integer.parseInt(initial_list[1]);
		    data_center.U = Integer.parseInt(initial_list[2]);
		    data_center.P = Integer.parseInt(initial_list[3]);
		    data_center.M = Integer.parseInt(initial_list[4]);
		    for(int i=0; i<data_center.U; i++)
		    {
		    	if((text = reader.readLine())!=null){
		    		initial_list = text.split(" ");
		    		x = Integer.parseInt(initial_list[0]);
		    		y = Integer.parseInt(initial_list[1]);
		    		center[x][y] = -1;
		    	}
		    }
		    float min, max;
		    min = 10;
		    max = 0;
		    for(int i=0; i<data_center.M; i++) {
		    	if((text = reader.readLine())!=null){
		    		initial_list = text.split(" ");
		    		servers[i].index = i;
		    		servers[i] = new Server(Integer.parseInt(initial_list[0]), Integer.parseInt(initial_list[1]));
		    		servers[i].ratio = Math.round(servers[i].cpu/ servers[i].size);
		    		if(servers[i].ratio > max)
		    			max = servers[i].ratio;
		    		if(servers[i].ratio < min)
		    			min = servers[i].ratio;
		    		System.out.println(i);
		    		System.out.println(servers[i].size);
		    		System.out.println(servers[i].ratio);
		    	}
		    }
		    System.out.println(min);
		    System.out.println(max);
		    
                                       pool[] pools = new pool[48];
                                       for(int i=0; i<48; i++){
                                                pools[i].add(servers[i]);                                      
                                       }
                                       Random r=new Random();
                                       
                                       
                                       for (int i=48; i<626;i++){
                                       
                                              pools[r.nextInt(49)].add(servers[i]);
                                       
                                       }
                                       
                                       
                                       
                   
		   
		} catch (FileNotFoundException e) {
		    e.printStackTrace();
		} catch (IOException e) {
		    e.printStackTrace();
		} finally {
		    try {
		        if (reader != null) {
		            reader.close();
		        }
		    } catch (IOException e) {
		    }
		}
		
		System.out.println(servers.length);

		quick_sort_for_server server_sort = new quick_sort_for_server();
		server_sort.sort(servers);
		 for(int i=0; i<M; i++) {
			 System.out.println(servers[i].ratio);
		 }
		System.out.println(servers[0].ratio);
		System.out.println(servers[624].ratio);
		System.out.println(data_center.R);
	
		
		PrintWriter writer = null;
		try {
			writer = new PrintWriter("out.txt", "UTF-8");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		writer.println("Hello World!");
		writer.close();
	}

}
