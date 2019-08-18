package org.gajnineteen.processor.impl;

import org.gajnineteen.analyzer.impl.CompoundWordsAnalyzer;
import org.gajnineteen.analyzer.impl.PorterStemmberAnalyzer;
import org.gajnineteen.analyzer.impl.StopWordsAnalyzer;
import org.gajnineteen.processor.Processor;

public class LemProcessor extends Processor {
    public LemProcessor() {
        this.textAnalyzers.add(new StopWordsAnalyzer(StopWordsAnalyzer.NLTK_STOP_WORDS));
        this.textAnalyzers.add(new CompoundWordsAnalyzer());
        this.textAnalyzers.add(new PorterStemmberAnalyzer());
    }
}
