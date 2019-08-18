package org.gajnineteen;

import org.gajnineteen.analyzer.impl.CompoundWordsAnalyzer;
import org.gajnineteen.analyzer.impl.PorterStemmberAnalyzer;
import org.gajnineteen.analyzer.impl.StopWordsAnalyzer;
import org.gajnineteen.processor.Processor;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;


/**
 * Normalizer：是否要切词
 * 停用词：NLTK、Lucene、?
 * 词干：Stemmer Porter、？
 */
public class App {
    @Option(name = "-f", usage = "a")
    private String fileName;
    @Option(name = "-brs", usage = "a")
    private String bugReports = "";
    @Option(name = "-cols", required = true, usage = "a")
    private String cols = "";
    @Option(name = "-s",  usage = "a")
    private String stopWordsFilePath = "";

    private final static String COL_SPLITER = ",";
    private final static String ANALYZER_SPLITER = "-";

    public static void main(String[] args) {
        App app = new App();
        CmdLineParser cmdLineParser = new CmdLineParser(app);
        try {
            cmdLineParser.parseArgument(args);
        } catch (CmdLineException e) {
            System.out.println("ERROR: Failed to parser argument.");
            e.printStackTrace();
        }

        Processor processor = new Processor();
        if (app.fileName != null && app.bugReports == null) {
            System.out.println("Analysing Source Code...");
            for (String col : app.cols.split(COL_SPLITER)) {
                for (String analyzer : col.split(ANALYZER_SPLITER)) {
                    switch (analyzer) {
                        case "PorterStemmer":
                            processor.addAnalyzer(new PorterStemmberAnalyzer());
                            break;
                        case "NLTKStopWord":
                            processor.addAnalyzer(new StopWordsAnalyzer(StopWordsAnalyzer.JAVA_KEY_WORDS));
                            break;
                        case "CamelCaseSplitting":
                            processor.addAnalyzer(new CompoundWordsAnalyzer());
                            break;
                        default:
                            System.out.println("ERROR: Invalid analyzer.");
                    }
                }

            }
        } else if (app.bugReports != null && app.fileName == null) {
            System.out.println("Analysing Bug Reports...");
            for (String col : app.cols.split(COL_SPLITER)) {
                for (String analyzer : col.split(ANALYZER_SPLITER)) {
                    switch (analyzer) {
                        case "PorterStemmer":
                            processor.addAnalyzer(new PorterStemmberAnalyzer());
                            break;
                        case "NLTKStopWord":
                            processor.addAnalyzer(new StopWordsAnalyzer(StopWordsAnalyzer.NLTK_STOP_WORDS));
                            break;
                        case "CamelCaseSplitting":
                            processor.addAnalyzer(new CompoundWordsAnalyzer());
                            break;
                        default:
                            System.out.println("ERROR: Invalid analyzer.");
                    }
                }

            }
        }else{
            System.out.println("ERROR: Unsupported analysis type.");
        }



        System.out.println(processor.process());


    }
}
