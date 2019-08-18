from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import os
import logging
import warnings
from numpy import exp, dot, sum as np_sum
from gensim import matutils
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences(object):
	def __init__(self, preprocessed_dir_path):
		self.dir_name = preprocessed_dir_path

	def __iter__(self):
		for dir in os.listdir(self.dir_name):
			dir_path = os.path.join(self.dir_name, dir)
			if os.path.isdir(dir_path):
				for f in os.listdir(dir_path):
					file_path=os.path.join(dir_path, f)
					for line in open(file_path):
						words_list = line.split(' ')
						words_list.remove("\n")
						yield words_list
			else:
				for line in open(dir_path):
					words_list = line.split(' ')
					words_list.remove("\n")
					yield words_list


def build_model(preprocessed_dir_path, model_save_path):
	sentences = MySentences(preprocessed_dir_path)

	# word2vec(train, output, size=100, window=5, sample='1e-3', hs=0,
	# negative=5, threads=12, iter_=5, min_count=5, alpha=0.025,
	# debug=2, binary=1, cbow=1, save_vocab=None, read_vocab=None,
	# verbose=False)
	# word2vec的常用参数介绍：
	# train：要训练的文件；
	# output：输出的词向量文件；
	# size：词向量维度大小；
	# window=5：训练的窗口，训练的窗口为5就是考虑一个词的前5个词和后5个词（实际代码中还有一个随机选窗口的过程，窗口大小<=5) ；
	# sample：采样的阈值，如果一个词语在训练样本中出现的频率越大，那么就会被采样；
	# hs：如果为1则会采用hierarchica·softmax技巧。如果设置为0，则negative sampling会被使用；
	# negative：如果>0,则会采用negativesamp·ing，用于设置多少个noise words；
	# min_count：可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉, 默认值为5；
	# binary：表示输出的结果文件是否采用二进制存储，0表示不使用（即普通的文本存储，可以打开查看），1表示使用，即vectors.bin的存储类型；
	# cbow：是否使用cbow模型，0表示使用skip-gram模型，1表示使用cbow模型，默认情况下是skip-gram模型，cbow模型快一些，skip-gram模型效果好一些 ；
	# save_vocab：词汇表保存到文件；
	# read_vocab：词汇表从文件中读取，不从训练数据中读取。
	# works , for training parallelization, to speed up training. only effect if you have Cython installed
	model = Word2Vec(sentences, min_count=1)
	# path="word2vec.model"
	model.save(model_save_path)
	return model

def load_model(path):
	# "word2vec.model"
	model = Word2Vec.load(path)
	return model


def train_model(model, words_list):
	# [["hello", "world"]]
	model.train(words_list, total_examples=1, epochs=1)


def most_similar(model, positive, negative, topn):
	print(model.most_similar(positive, negative, topn))


def similarity(model, word_a, word_b):
	return model.similarity(word_a, word_b)



def save_model_vector(model, path):
	# path = get_tmpfile("wordvectors.kv")
	model.wv.save(path)


def load_model_vector(path):
	wv = KeyedVectors.load("wordvectors.kv", mmap='r')
	# vector = wv['hello']
	# print(vector)
	return wv


def load_model_txt(path):
	# path = '/tmp/vectors.txt'
	model = Word2Vec.load_word2vec_format(path, binary=False)
	return model


def load_model_bin(path):
	# using gzipped/bz2 input works too, no need to unzip:
	# path = '/tmp/vectors.bin.gz'
	model = Word2Vec.load_word2vec_format(path, binary=True)
	return model

