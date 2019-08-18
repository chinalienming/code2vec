import os
import pandas as pd
import numpy as np
from pandas.errors import EmptyDataError
import json

"""
对由word2vec获得的bug report vectors,以及由code2vec获得的code vectors
预处理, 得到输入  模型的list
"""

project_id_sep = "_"
dir_sep = "/"
buggy_tag = 1
normal_tag = 0


# 读文件
def load_single_brv(file_path):
	df = pd.read_csv(file_path, header=None, delim_whitespace=True, dtype=float )
	return df


def load_single_brv_for_ist(file_path):
	# print(file_path)
	f = open(file_path, 'r')
	while True:
		line = f.readline()
		if not line:
			break
		if len(line) > 0 :
			list = parse_str_to_list(line, sep = ' ')
			# print(list)
			return list
	return


def load_brvs_dic_for_ist(br_dir):
	# brv_list = []
	dic = {}
	for project_dir in os.listdir(br_dir):
		project_dir_path = os.path.join(br_dir, project_dir)
		if os.path.isdir(project_dir_path):
			for file in os.listdir(project_dir_path):
				if file == '.DS_Store':
					continue
				file_path = os.path.join(project_dir_path, file)

				list = load_single_brv_for_ist(file_path)
				dic[file] = list
		else:
			if project_dir == '.DS_Store':
				continue
			list = load_single_brv_for_ist(project_dir_path)
			dic[project_dir] = list

	return dic



# 池化函数
def pooling_brv(df):
	return np.amax(df, 0)


# 池化操作
def handle_brvs(br_dir, pooling_br_dir):
	# 创建文件目录
	if not os.path.exists(pooling_br_dir):
		os.mkdir(pooling_br_dir)
	# 遍历项目目录
	for project_dir in os.listdir(br_dir):
		project_dir_path = os.path.join(br_dir, project_dir)
		if os.path.isdir(project_dir_path):
			for file in os.listdir(project_dir_path):
				file_path = os.path.join(project_dir_path, file)
				try:
					# 读取br_vector/../..
					df = load_single_brv(file_path)

					# 池化操作
					pooling_df = pooling_brv(df)

					# 创建项目目录
					pooling_project_dir_path = os.path.join(pooling_br_dir, project_dir)
					if not os.path.exists(pooling_project_dir_path):
						os.mkdir(pooling_project_dir_path)

					# 写文件
					pooling_file_path = os.path.join(pooling_br_dir, project_dir, file)
					# with open(pooling_file_path, 'w') as pooling_br_file:
					# pooling_br_file.write()

					a = np.array(pooling_df)
					b = a.reshape((1, 100), order='C')
					# np.save(pooling_file_path, b)
					np.savetxt(pooling_file_path, b)

				except EmptyDataError:
					# 存在br_vector可能为空, 是否需要创建空文件?
					print(file_path+" is empty.")


# 读取所有bug report vectors
def load_brvs_dic(br_dir):
	# brv_list = []
	dic = {}
	for project_dir in os.listdir(br_dir):
		project_dir_path = os.path.join(br_dir, project_dir)
		if os.path.isdir(project_dir_path):
			for file in os.listdir(project_dir_path):
				if file == '.DS_Store':
					continue
				file_path = os.path.join(project_dir_path, file)

				# 读取br_vector/../..
				df = load_single_brv(file_path)

				# f = open(file_path, 'r')
				# line = f.readline()
				# if len(line) == 0:
				# 	continue

				# 第一行
				single_list = df[0:1].values
				# single_list = df[0:1].values

				# if len(single_list) == 0:
				# 	list.append([])
				# brv_list.append(single_list)
				dic[file] = single_list[0]
		else:
			if project_dir == '.DS_Store':
				continue

			df = load_single_brv(project_dir_path)
			single_list = df[0:1].values
			dic[project_dir] = single_list[0]

	return dic


# def load_all_cvs(cv_dir):
# 	cv_list = []
# 	for project_dir in os.listdir(cv_dir):
# 		project_dir_path = os.path.join(cv_dir, project_dir)
# 		if os.path.isdir(project_dir_path):
# 			for file in os.listdir(project_dir_path):
# 				if file == '.DS_Store':
# 					continue
# 				file_path = os.path.join(project_dir_path, file)
# 				with open(file_path, 'r') as f:
# 					for line in f:
# 						line = line.strip()
# 						# avoid blank lines
# 						line_str = line.split(" ")
# 						cv_list.append(line_str)
# 	return cv_list


def load_cv_from_dic_file(file_path):
	cv_f = open(file_path, 'r')
	jsObj = json.load(cv_f)
	# for item in jsObj:
	# 	print(item)

	return jsObj


# def get_brv(dir_path, project_name, project_br_id):
# 	f = open(dir_path + "/" + project_name + "/" + project_name + "_" +project_br_id, 'r')
# 	return


def parse_str_to_list(str, sep):
	list = []
	parts = str.split(sep)
	for p in parts:
		if len(p) > 0:
			list.append(float(p))
	return list


# for every project eg. "Time"
def build_input(project_brv_dir, buggy_cv_file_path, normal_cv_file_path, train_percent, valid_percent):

	# Calculate size of useful projects
	# format: eg. "{'Closure_1':brv}"
	brv_dic = load_brvs_dic(project_brv_dir)
	dataset_size = len(brv_dic)
	print("dataset size: " + str(dataset_size))
	train_set_size = int(dataset_size * train_percent)
	valid_set_size = int(dataset_size * valid_percent)
	test_set_size = dataset_size - train_set_size - valid_set_size
	print("trainset size: " + str(train_set_size))
	print("validset size: " + str(valid_set_size))
	print("testset size: " + str(test_set_size))
	if train_set_size <= 0 or valid_set_size <= 0 or test_set_size <= 0:
		print("Exist dataset size <= 0. ")
		return

	# build train, valid, test dictionary { project_name: list } eg. { Time: [1,2,3], Math: [1,2] ..}
	train_dic, valid_dic, test_dic = {}, {}, {}
	id_list = []
	for project_id in brv_dic:
		br_id = int(project_id.split(project_id_sep)[1])
		id_list.append(br_id)
	id_list.sort()

	# print("sorted id_list: " + str(id_list))
	# print(id_list[:train_set_size])
	# print(id_list[train_set_size:train_set_size+valid_set_size])
	# print(id_list[-(valid_set_size+1):])
	project_name = ''.join(project_brv_dir.split(dir_sep)[-1:])
	train_dic[project_name] = id_list[:train_set_size]
	valid_dic[project_name] = id_list[train_set_size:train_set_size+valid_set_size]
	test_dic[project_name] = id_list[-(valid_set_size+1):]

	train_wv, train_cv, train_tag = [], [], []
	valid_wv, valid_cv, valid_tag = [], [], []
	test_wv, test_cv, test_tag = [], [], []

	# loop in buggy_cv_dic
	buggy_cv_dic = load_cv_from_dic_file(buggy_cv_file_path)

	for path_name in buggy_cv_dic:
		project_str = path_name.split(dir_sep)[2]
		# project_parts = project_str.split("_")
		# project_name = project_parts[0]
		# project_br_id = project_parts[1]
		# print(project_str)
		try:
			bug_report_vector = brv_dic[project_str]
		except KeyError:
			# can not find brv
			# print(project_str + " bug report does not exists. ")
			continue

		br_info = project_str.split(project_id_sep)
		br_name = ''.join(br_info[0])
		br_id = int(br_info[1])
		code_vector = buggy_cv_dic[path_name]
		cv_list = parse_str_to_list(code_vector, sep = ' ')

		if br_id in train_dic[br_name]:
			train_wv.append(bug_report_vector)
			train_cv.append(cv_list)
			train_tag.append(buggy_tag)
		elif br_id in valid_dic[br_name]:
			valid_wv.append(bug_report_vector)
			valid_cv.append(cv_list)
			valid_tag.append(buggy_tag)
		elif br_id in test_dic[br_name]:
			test_wv.append(bug_report_vector)
			test_cv.append(cv_list)
			test_tag.append(buggy_tag)
		else:
			print(str(project_str) + " : find code vector, but can not find corresponding bug report vector.")
			continue

	# loop in normal_cv_dic ?
	normal_cv_dic = load_cv_from_dic_file(normal_cv_file_path)

	for path_name in normal_cv_dic:
		project_str = path_name.split(dir_sep)[2]
		# project_parts = project_str.split("_")
		# project_name = project_parts[0]
		# project_br_id = project_parts[1]
		# print(project_str)
		try:
			bug_report_vector = brv_dic[project_str]
		except KeyError:
			# can not find brv
			# print(project_str + " bug report does not exists. ")
			continue

		br_info = project_str.split(project_id_sep)
		br_name = ''.join(br_info[0])
		br_id = int(br_info[1])
		code_vector = normal_cv_dic[path_name]
		cv_list = parse_str_to_list(code_vector, sep = ' ')

		if br_id in train_dic[br_name]:
			train_wv.append(bug_report_vector)
			train_cv.append(cv_list)
			train_tag.append(normal_tag)
		elif br_id in valid_dic[br_name]:
			valid_wv.append(bug_report_vector)
			valid_cv.append(cv_list)
			valid_tag.append(normal_tag)
		elif br_id in test_dic[br_name]:
			test_wv.append(bug_report_vector)
			test_cv.append(cv_list)
			test_tag.append(normal_tag)
		else:
			print(str(project_str) + " : find code vector, but can not find corresponding bug report vector.")
			continue

	return train_wv, train_cv, train_tag, valid_wv, valid_cv, valid_tag, test_wv, test_cv, test_tag


def add_all_from_list2(list1, list2):
	for item in list2:
		list1.append(item)
	return list1


def load_link_dic(path):
	dic = {}
	f = open(path, 'r')
	while True:
		line = f.readline()
		if not line:
			break
		if len(line) > 0:
			parts = line.split('\t')
			br_id = parts[0]
			pm_lists_str = parts[1].rstrip('\n')
			pm_lists = pm_lists_str.split('外')
			for pm_list in pm_lists:
				pm_parts = pm_list.split('内')
				path = 'data/istDat4exp/allMethods/' + str(pm_parts[0])
				method = pm_parts[1]
				path_method = path + '#' + method
				if br_id not in dic:
					dic.setdefault(br_id, []).append(path_method)
				else:
					dic[br_id].append(path_method)

	# print(dic)
	return dic


def get_k_by_v(dic, value):
	for key in dic:
		if value in dic[key]:
			return key
	return


def load_pooling_brv_dir_for_ist(path):
	dic = {}
	if os.path.isdir(path):
		for project in os.listdir(path):
			# print(project)
			project_path = os.path.join(path, project)
			# print(project_path)
			if os.path.isdir(project_path):
				dic.setdefault(project, [])
				for br in os.listdir(project_path):
					dic[project].append(br)

	return dic



def build_input_for_ist(project_brv_dirs, buggy_cv_file_path, normal_cv_file_path, train_percent, valid_percent):

	total_train_wv, total_train_cv, total_train_tag = [], [], []
	total_valid_wv, total_valid_cv, total_valid_tag = [], [], []
	total_test_wv, total_test_cv, total_test_tag = [], [], []

	for project_brv_dir in os.listdir(project_brv_dirs):

		pbd_path = os.path.join(project_brv_dirs, project_brv_dir)
		# print(pbd_path)
		brv_dic = load_brvs_dic_for_ist(pbd_path)
		dataset_size = len(brv_dic)
		print("dataset size: " + str(dataset_size))
		train_set_size = int(dataset_size * train_percent)
		valid_set_size = int(dataset_size * valid_percent)
		test_set_size = dataset_size - train_set_size - valid_set_size
		print("trainset size: " + str(train_set_size))
		print("validset size: " + str(valid_set_size))
		print("testset size: " + str(test_set_size))
		if train_set_size <= 0 or valid_set_size <= 0 or test_set_size <= 0:
			print(pbd_path + "Exist dataset size <= 0. ")
			continue

		# build train, valid, test dictionary { project_name: list } eg. { Time: [1,2,3], Math: [1,2] ..}
		train_dic, valid_dic, test_dic = {}, {}, {}
		id_list = []
		for project_id in brv_dic:
			# print(project_id)
			if project_id_sep in project_id:
				br_id = int(project_id.split(project_id_sep)[1])
				id_list.append(br_id)
			else:
				id_list.append(project_id)
		id_list.sort()

		project_name = project_brv_dir

		train_dic[project_name] = id_list[:train_set_size]
		valid_dic[project_name] = id_list[train_set_size:train_set_size+valid_set_size]
		test_dic[project_name] = id_list[-(valid_set_size+1):]

		train_wv, train_cv, train_tag = [], [], []
		valid_wv, valid_cv, valid_tag = [], [], []
		test_wv, test_cv, test_tag = [], [], []

		# loop in buggy_cv_dic
		buggy_cv_dic = load_cv_from_dic_file(buggy_cv_file_path)

		link_dic = load_link_dic("/Users/lienming/Downloads/istDat4exp/linked-bugMethods/"+project_brv_dir+"_bugId_buggyMethodsName")

		for path_name in buggy_cv_dic:
			# print(path_name)

			project_str = get_k_by_v(link_dic, path_name)
			# project_str = path_name.split(dir_sep)[3]
			# 问题！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

			try:
				bug_report_vector = brv_dic[project_str]
			except KeyError:
				# can not find brv
				# print(project_str + " bug report does not exists. ")
				continue

			code_vector = buggy_cv_dic[path_name]
			cv_list = parse_str_to_list(code_vector, sep = ' ')
			br_id = project_str
			br_name = project_name
			# print(bug_report_vector)

			if br_id in train_dic[br_name]:
				train_wv.append(bug_report_vector)
				train_cv.append(cv_list)
				train_tag.append(buggy_tag)
			elif br_id in valid_dic[br_name]:
				valid_wv.append(bug_report_vector)
				valid_cv.append(cv_list)
				valid_tag.append(buggy_tag)
			elif br_id in test_dic[br_name]:
				test_wv.append(bug_report_vector)
				test_cv.append(cv_list)
				test_tag.append(buggy_tag)
			else:
				print(str(project_str) + " : find code vector, but can not find corresponding bug report vector.")
				continue

		# loop in normal_cv_dic
		normal_cv_dic = load_cv_from_dic_file(normal_cv_file_path)

		pooling_dic = load_pooling_brv_dir_for_ist("/Users/lienming/Downloads/istDat4exp/ist_pooling_brv")

		for path_name in normal_cv_dic:
			# print(path_name)
			project_name = path_name.split('/')[3]
			# print(project_name)
			if project_name in pooling_dic:
				for br_file in pooling_dic[project_name]:
					if br_file in brv_dic:

						bug_report_vector = brv_dic[br_file]
						br_name = project_name
						br_id = br_file
						code_vector = normal_cv_dic[path_name]
						cv_list = parse_str_to_list(code_vector, sep = ' ')
						if br_id in train_dic[br_name]:
							train_wv.append(bug_report_vector)
							train_cv.append(cv_list)
							train_tag.append(normal_tag)
						elif br_id in valid_dic[br_name]:
							valid_wv.append(bug_report_vector)
							valid_cv.append(cv_list)
							valid_tag.append(normal_tag)
						elif br_id in test_dic[br_name]:
							test_wv.append(bug_report_vector)
							test_cv.append(cv_list)
							test_tag.append(normal_tag)
						else:

							# print(str(project_str) + " : find code vector, but can not find corresponding bug report vector.")
							return
			else:
				continue


		# add to total list!
		print(len(train_wv))
		print(len(valid_wv))
		print(len(test_wv))
		total_train_wv = add_all_from_list2(total_train_wv, train_wv)
		total_train_cv = add_all_from_list2(total_train_cv, train_cv)
		total_train_tag = add_all_from_list2(total_train_tag, train_tag)
		total_valid_wv = add_all_from_list2(total_valid_wv, valid_wv)
		total_valid_cv = add_all_from_list2(total_valid_cv, valid_cv)
		total_valid_tag = add_all_from_list2(total_valid_tag, valid_tag)
		total_test_wv = add_all_from_list2(total_test_wv, test_wv)
		total_test_cv = add_all_from_list2(total_test_cv, test_cv)
		total_test_tag = add_all_from_list2(total_test_tag, test_tag)




	print(len(total_train_wv))
	print(len(total_valid_wv))
	print(len(total_test_wv))

	return total_train_wv, total_train_cv, total_train_tag, total_valid_wv, total_valid_cv, \
	       total_valid_tag, total_test_wv, total_test_cv, total_test_tag


brv_dir = "pooling_br_vector/Time"
source_code_dir_prefix = "data/rjc0815/"
buggy_cv_file_path = "/Users/lienming/Desktop/code2vec/vectors_output/buggy"
normal_cv_file_path = "/Users/lienming/Desktop/code2vec/vectors_output/normal"


# build_input(brv_dir, buggy_cv_file_path, normal_cv_file_path, 0.8, 0.1)


# print(len(bl))
# print(len(cl))

# print(type(bl[0]))
# print(type(cl[0]))
# print(type(tl[0]))
# for i in range(0, len(bl)):
	# print(bl[i])
	# print(cl[i])
	# print(tl[i])




# handle_bug_report_vectors("br_vector", "pooling_br_vector")
# brv_list = load_all_brvs("pooling_br_vector")
# print(brv_list)

# cv_list = load_all_cvs("cv")
# print(cv_list)




# ast_path_dic = {}
# p1 = '1234567890'
# fp1 = "aaa/123.java void func()"
# fp2 = "bbb/123.java void func()"
# addDic(ast_path_dic, p1, fp1)
# print(ast_path_dic)
# addDic(ast_path_dic, p1, fp2)
# print(ast_path_dic)


