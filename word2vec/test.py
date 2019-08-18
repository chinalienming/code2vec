import br2vec
import porterstemmer
import os
from argparse import ArgumentParser
def stem(sword):
	ps = porterstemmer.PorterStemmer()
	return ps.stem(sword, 0, len(sword)-1)


def query(word):
	processed_word  = stem(word)
	print(processed_word)


def produce_vector(dir_name, wv_output_path):
	# dir_name = "preprocessed_br"
	# vector_dir = "br_vector"
	vector_dir = wv_output_path
	if not os.path.exists(wv_output_path):
		os.mkdir(wv_output_path)
	model = br2vec.load_model("br2vec.model")
	for dir in os.listdir(dir_name):
		dir_path = os.path.join(dir_name, dir)
		vector_dir_path = os.path.join(vector_dir, dir)
		if os.path.isdir(dir_path):
			if not os.path.exists(vector_dir_path):
				os.mkdir(vector_dir_path)
			for f in os.listdir(dir_path):
				file_path = os.path.join(dir_path, f)
				vector_file_path = os.path.join(vector_dir_path, f)
				for line in open(file_path):
					words_list = line.split(' ')
					words_list.remove('\n')
					with open(vector_file_path, 'w') as outfile:
						for word in words_list:
							try:
								word_vector = model[word]

								outfile.write(str(word_vector))
								# outfile.write(',' + '\n')
							except KeyError:
								print('word \"'+word+'\" not in vocabulary')


def build(preprocessed_dir_path):
	model = br2vec.build_model(preprocessed_dir_path, model_save_path = "br2vec.model")
	# model = br2vec.load_model("br2vec.model")
	model.wv.save_word2vec_format("vectors")


# build()
# produce_vector()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest = "preprocessed_dir_path", required = True)
    parser.add_argument("-o", "--output", dest = "wv_output_path", required = True)

    args = parser.parse_args()
    preprocessed_dir_path = args.preprocessed_dir_path
    wv_output_path = args.wv_output_path
    build(preprocessed_dir_path=preprocessed_dir_path)
    produce_vector(preprocessed_dir_path, wv_output_path)


# print(wv['bug'])

# print(br2vec.similarity(model, 'remot', 'bug'))

# print(br2vec.most_similar(model, ['bug', 'remot'], ['window'], 5))

# print(model['remot'])
# print(model.wv.word_vec('remot'))
# print(wv['remot'][:20])
# print(model.predict_output_word(["remot", "messag"]))
