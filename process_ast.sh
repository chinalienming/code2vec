#!/usr/bin/env bash
# run `JavaExtractor` on a java project
# the main output is :
#       '.dictionary' : dictionary { "Path+Method" : "key in '.vectors'" }
#       '.redundant' : dictionary for redundant vectors, { "AST PATH" : "Path+Method" }
#       'c2v.vectors' : dictionary { "processed method name" : "code vector" }
#   and other output files used in `code2vec` tool:
#       '.dict.c2v'
#       '.c2v'
#       '.c2v.num_examples'


TRAIN_DIR=data/rjc0815
DATASET_NAME=mydataset0815

MAX_CONTEXTS=200
WORD_VOCAB_SIZE=1301136
PATH_VOCAB_SIZE=911417
TARGET_VOCAB_SIZE=261245

NUM_THREADS=64
PYTHON=python3
###########################################################

TRAIN_DATA_FILE=${DATASET_NAME}.train.raw.txt

EXTRACTOR_JAR=JavaExtractor/JPredict/out/artifacts/JavaExtractor_0_0_2_SNAPSHOT/JavaExtractor.jar

mkdir -p data
mkdir -p data/${DATASET_NAME}

echo "Extracting paths from training set..."
${PYTHON} JavaExtractor/extract.py --dir ${TRAIN_DIR} --max_path_length 8 --max_path_width 2 --num_threads ${NUM_THREADS} --jar ${EXTRACTOR_JAR} > ${TRAIN_DATA_FILE}
echo "Finished extracting paths from training set"

TARGET_HISTOGRAM_FILE=data/${DATASET_NAME}/${DATASET_NAME}.histo.tgt.c2v
ORIGIN_HISTOGRAM_FILE=data/${DATASET_NAME}/${DATASET_NAME}.histo.ori.c2v
PATH_HISTOGRAM_FILE=data/${DATASET_NAME}/${DATASET_NAME}.histo.path.c2v

echo "Creating histograms from the training data"
cat ${TRAIN_DATA_FILE} | cut -d' ' -f1 | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > ${TARGET_HISTOGRAM_FILE}
cat ${TRAIN_DATA_FILE} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f1,3 | tr ',' '\n' | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > ${ORIGIN_HISTOGRAM_FILE}
cat ${TRAIN_DATA_FILE} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f2 | awk '{n[$0]++} END {for (i in n) print i,n[i]}' > ${PATH_HISTOGRAM_FILE}

${PYTHON} query_vector.py --train_data ${TRAIN_DATA_FILE}   \
  --max_contexts ${MAX_CONTEXTS} --word_vocab_size ${WORD_VOCAB_SIZE} --path_vocab_size ${PATH_VOCAB_SIZE} \
  --target_vocab_size ${TARGET_VOCAB_SIZE} --word_histogram ${ORIGIN_HISTOGRAM_FILE} \
  --path_histogram ${PATH_HISTOGRAM_FILE} --target_histogram ${TARGET_HISTOGRAM_FILE} --output_name data/${DATASET_NAME}/${DATASET_NAME}

# If all went well, the raw data files can be deleted, because preprocess.py creates new files
# with truncated and padded number of paths for each example.
rm ${TRAIN_DATA_FILE}   ${TARGET_HISTOGRAM_FILE} ${ORIGIN_HISTOGRAM_FILE} \
  ${PATH_HISTOGRAM_FILE}


DEFAULT_MODEL=models/java14_model/saved_model_iter8.release
C2V_FILE=data/${DATASET_NAME}/${DATASET_NAME}.c2v

#${PYTHON} code2vec.py --load ${DEFAULT_MODEL} --test ${C2V_FILE}  --export_code_vectors
