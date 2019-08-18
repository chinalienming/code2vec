package JavaExtractor.Common;

import com.github.javaparser.ast.Node;

import java.util.ArrayList;

public class MethodContent {
	private String originalName ;
	private ArrayList<Node> leaves;
	private String name;
	private long length;

	public MethodContent(String originalName , ArrayList<Node> leaves, String name, long length) {
		this.originalName = originalName ;
		this.leaves = leaves;
		this.name = name;
		this.length = length;
	}

	public String getOriginalName(){return originalName;}

	public ArrayList<Node> getLeaves() {
		return leaves;
	}

	public String getName() {
		return name;
	}

	public long getLength() {
		return length;
	}

}
