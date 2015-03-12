/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package java_hashcode;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author gabriele
 */
public class pool {
    

    public pool(){
        this.capacity = 0;
	}
        
  public int add(Server s){           
      
      servers.add(s);
      this.capacity+=s.cpu;
            return 1;
            
    }
  
  public int get_cpu(){
        return this.capacity;
  
  }
    
        
          
               List<Server> servers = new ArrayList<Server>();
               int capacity;
}
