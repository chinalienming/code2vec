# encoding: utf-8
import keras, os, pandas as pd
from keras.layers import  Flatten
from keras.layers import Input, Dense
from keras.models import Model, load_model
import numpy as np
import preprocess_vector as pv
from argparse import ArgumentParser
from keras.datasets import mnist

brv_dir = "pooling_br_vector/Time"
buggy_cv_file_path = "/Users/lienming/Desktop/code2vec/vectors_output/buggy"
normal_cv_file_path = "/Users/lienming/Desktop/code2vec/vectors_output/normal"
# train_wv, train_cv, train_tag, valid_wv, valid_cv, valid_tag, test_wv, test_cv, test_tag = \
# 		pv.build_input(brv_dir, buggy_cv_file_path, normal_cv_file_path, train_percent = 0.8, valid_percent = 0.1)

# for i in range(10):
# 	print(test_wv[i])
# 	print(test_cv[i])
# 	print(test_tag[i])
# print(len(train_wv))
# print(len(valid_wv))
# print(len(test_wv))


(X_train_image, y_train_label), (X_test_image, y_test_label) = mnist.load_data("mnist.npz")
X_Train = X_train_image.reshape(60000, 784).astype('float32')
X_Test = X_test_image.reshape(10000, 784).astype('float32')



def train_model(save_path):
	# define dimension for word vector, code vector
	# word_vector_dim = 100
	# code_vector_dim = 384
	word_vector_dim = 784
	# code_vector_dim = 784
	# default dtype = 'float32'
	# wv_input = Input(shape=(word_vector_batch_size,))
	wv_input = Input(batch_shape=(None, 784), name='wv_input')
	# input for code vector
	# cv_input = Input(shape=(code_vector_batch_size,))
	# cv_input = Input(batch_shape=(None, code_vector_dim), name='cv_input')


	# axis = ?? 0-line 1-row
	# merged = keras.layers.concatenate(inputs=[wv_input, cv_input])
	# We stack a deep densely-connected network on top
	# x = Dense(8, activation='relu', input_shape=(word_vector_dim+code_vector_dim,))(merged)
	# x = Dense(8, activation = 'relu', input_shape = (word_vector_dim,))(merged)
	x = Dense(4, activation='relu')(wv_input)
	x = Dense(2, activation='relu')(x)
	# And finally we add the main logistic regression layer
	output = Dense(1, activation='sigmoid', name='output')(x)
	model = Model(inputs = [wv_input], outputs = output)
	# model = Model(inputs=[wv_input, cv_input], outputs=output)
	model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
	# model.fit(x=[train_wv, train_cv], y=[train_tag], validation_data=([valid_wv, valid_cv], [valid_tag]), epochs=1)
	model.fit(x = [X_Train], y = [y_train_label], validation_data = ([X_Test], [y_test_label]),
	          epochs = 1)
	model.save(save_path)
	return model

print(len(X_test_image))

m = train_model("mnist")
res = m.predict(X_Train)
for i in range(100):
	print(res[i])
# train_model("first_model")
# model = load_model("first_model")
# res = model.predict([test_wv, test_cv])
# for i in range(len(res)):
# 	print(str(res[i][0]) + ' ' + str(test_tag[i]))


# if __name__ == '__main__':
# 	parser = ArgumentParser()
# 	parser.add_argument("-brv", "--brv_dir", dest = "brv_dir", required = True)
# 	parser.add_argument("-bcv", "--buggy_cv_file_path", dest = "buggy_cv_file_path", required = True)
# 	parser.add_argument("-ncv", "--normal_cv_file_path", dest = "normal_cv_file_path", required = True)
# 	parser.add_argument("-pbrv", "--pooling_brv_path", dest = "pooling_brv_path", required = True)
# 	args = parser.parse_args()
# 	brv_dir = args.brv_dir
# 	buggy_cv_file_path = args.buggy_cv_file_path
# 	normal_cv_file_path = args.normal_cv_file_path
# 	pooling_brv_path = args.pooling_brv_path
#
# 	# pv.handle_brvs(br_dir = brv_dir, pooling_br_dir = pooling_brv_path)
#
# 	train_wv, train_cv, train_tag, valid_wv, valid_cv, valid_tag, test_wv, test_cv, test_tag = \
# 		pv.build_input_for_ist(pooling_brv_path, buggy_cv_file_path, normal_cv_file_path, train_percent = 0.8, valid_percent = 0.1)
#
# 	train_model("ist_model")
# 	model = load_model("ist_model")
# 	res = model.predict([test_wv, test_cv])
# 	for i in range(len(res)):
# 		print(str(res[i][0]) + ' ' + str(test_tag[i]))