package JavaExtractor.FeaturesEntities;

import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.ArrayList;
import java.util.stream.Collectors;

public class ProgramFeatures {
	private String programPath ;
	private String originalName;
	private String name;

	private ArrayList<ProgramRelation> features = new ArrayList<>();

	public ProgramFeatures(String name) {
		this.name = name;
	}

	public ProgramFeatures(String programPath, String originalName , String name) {
		this.originalName = originalName;
		this.name=name;
		this.programPath=programPath;
	}

	@SuppressWarnings("StringBufferReplaceableByString")
	@Override
	public String toString() {
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.append(programPath).append("分").append(originalName).append("分");
		stringBuilder.append(name).append(" ");
		stringBuilder.append(features.stream().map(ProgramRelation::toString).collect(Collectors.joining(" ")));

		return stringBuilder.toString();
	}

	public void addFeature(Property source, String path, Property target) {
		ProgramRelation newRelation = new ProgramRelation(source, target, path);
		features.add(newRelation);
	}

	@JsonIgnore
	public boolean isEmpty() {
		return features.isEmpty();
	}

	public void deleteAllPaths() {
		features.clear();
	}

	public String getName() {
		return name;
	}

	public ArrayList<ProgramRelation> getFeatures() {
		return features;
	}

	public String getProgramPath() { return programPath; }

	public String getOriginalName() { return originalName; }

}
