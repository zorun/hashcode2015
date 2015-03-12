package java_hashcode;

public class Server {
	public Server(int size, int cpu){
		this.size = size;
		this.cpu = cpu;
	}
	public Server(){
		this.size = 0;
		this.cpu = 0;
	}
	
	public boolean compareTo(Server comp){
		return this.ratio > comp.ratio; 
	}
	
	public int index;
	public int size;
	public int cpu;
	public int row;
	public int slot;
        public int pool;
	public int ratio;
}
