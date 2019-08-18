import os
import json
import random
from argparse import ArgumentParser

sep = "#"


def construct_p2v_dictionary(path_prefix):
    path_file_path = path_prefix + ".path"
    vectors_file_path = path_prefix + ".c2v.vectors"
    save_path = path_prefix + ".p2v.vectors"

    dic_file = open(path_file_path, 'r', encoding='utf-8')
    vectors_file = open(vectors_file_path, 'r', encoding='utf-8')

    p2v_dictionary = {}

    # new dictionary : path_method -> code vector
    while True:
        path_method = dic_file.readline()
        if not path_method:
            break
        path_method = path_method.rstrip('\n')

        code_vector = vectors_file.readline()
        code_vector = code_vector.rstrip('\n')
        p2v_dictionary[path_method] = code_vector

    dic_file.close()
    vectors_file.close()
    save_file = open(save_path, 'w')
    json.dump(p2v_dictionary, save_file)
    # save_file.write(json.dumps(p2v_dictionary))
    print("p2v dictionary save to: " + save_path)


# def construct_p2v_dictionary_for_ist(path_prefix):
#     path_file_path = path_prefix + ".path"
#     vectors_file_path = path_prefix + ".c2v.vectors"
#     save_path = path_prefix + ".p2v.vectors"
#
#     dic_file = open(path_file_path, 'r', encoding='utf-8')
#     vectors_file = open(vectors_file_path, 'r', encoding='utf-8')
#
#     p2v_dictionary = {}
#
#     # new dictionary : path_method -> code vector
#     while True:
#         path_method = dic_file.readline()
#         if not path_method:
#             break
#         path_method = path_method.rstrip('\n')
#         # path_method = "/Users/lienming/Desktop/code2vec/" + path_method
#         code_vector = vectors_file.readline()
#         code_vector = code_vector.rstrip('\n')
#         # print(path_method)
#         p2v_dictionary[path_method] = code_vector
#
#     dic_file.close()
#     vectors_file.close()
#     save_file = open(save_path, 'w')
#     json.dump(p2v_dictionary, save_file)
#     # save_file.write(json.dumps(p2v_dictionary))
#     print("p2v dictionary save to: " + save_path)


def export_buggy_method_vector_for_ist(path_method_list, path_prefix, save_path):
    p2v_file_path = path_prefix + ".p2v.vectors"
    redun_file_path = path_prefix + ".redundant"
    p2v_file = open(p2v_file_path, 'r', encoding='utf-8')
    p2v_dictionary = json.load(p2v_file)
    p2v_file.close()

    redun_file = open(redun_file_path, 'r', encoding='utf-8')
    redun_dictionary = json.load(redun_file)
    redun_file.close()

    save_dic = {}
    save_file = open(save_path, 'w')

    for path_method in path_method_list:
        # path_method = "data/istDat4exp/allMethods/" + path_method
        # print(path_method)
        if path_method in p2v_dictionary:
            save_dic[path_method] = p2v_dictionary[path_method]
            # save_file.write(path_method+"$"+p2v_dictionary[path_method] + '\n')
            print("get vector from p2v dictionary!")
        else:
            ast_path_lists = get_other_values_from_dictionary(redun_dictionary, value=path_method)
            # method存在于多个ast path的问题?
            ast_path_lists_size = len(ast_path_lists)
            if ast_path_lists_size == 0:
                pm_parts = path_method.split(sep)
                me_parts = pm_parts[1].split(' ')
                ret_type = me_parts[0]
                # print(ret_type[-2:])
                # problem for AST can not parse return type of array
                if ret_type.endswith('[]'):
                    # ret_type = ret_type[:-2]
                    new_path_method = pm_parts[0] + sep + ret_type[:-2] + ' '
                    for i in range(1, len(me_parts)):
                        new_path_method += me_parts[i] + ' '
                    new_path_method = new_path_method.strip()
                    # print(new_path_method)
                    if new_path_method in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[new_path_method]
                        # save_file.write(path_method+"$"+p2v_dictionary[new_path_method] + '\n')
                        print("successfully to find in p2v by modifying return type (remove [])")
                    else:
                        new_ast_path_lists = get_other_values_from_dictionary(redun_dictionary, value=new_path_method)
                        new_ast_path_lists_size = len(ast_path_lists)
                        if new_ast_path_lists_size == 0:
                            # save_file.write(new_path_method+"$"+'\n')
                            print("[ " + path_method +
                                  " ] return type is array, try to remove [], but can not found in same AST Path! ")
                        elif new_ast_path_lists_size > 1:
                            random_choice = random.randint(0, new_ast_path_lists_size-1)
                            new_ast_path_list = new_ast_path_lists[random_choice]
                            for pm in new_ast_path_list:
                                if pm in p2v_dictionary:
                                    save_dic[path_method] = p2v_dictionary[pm]
                                    # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                                    print(path_method + " exists in " + str(ast_path_lists_size) +
                                          " AST Path, and randomly choose No." + str(random_choice) + " path.")
                                    break
                        else:
                            new_ast_path_list = new_ast_path_lists[0]
                            for pm in new_ast_path_list:
                                if pm in p2v_dictionary:
                                    # print(p2v_dictionary[pm])
                                    save_dic[path_method] = p2v_dictionary[pm]
                                    # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                                    print("successfully to find in redundant dictionary by remove [].")
                                    break
                else:
                    # save_file.write(path_method+"$"+'\n')
                    print("[ " + path_method + " ] can not found in same AST Path! ")
            elif ast_path_lists_size > 1:
                random_choice = random.randint(0, ast_path_lists_size - 1)
                ast_path_list = ast_path_lists[random_choice]
                for pm in ast_path_list:
                    if pm in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[pm]
                        # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                        print(path_method + " exists in " + str(ast_path_lists_size) +
                              " AST Path, and randomly choose No." + str(random_choice) + " path.")
                        break
            else:
                ast_path_list = ast_path_lists[0]
                for pm in ast_path_list:
                    if pm in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[pm]
                        # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                        print("get vector from redundant dictionary!")

    json.dump(save_dic, save_file)


# function to look up vectors in dictionary, and save vectors to "save_path"
def export_buggy_method_vector(path_method_list, path_prefix, save_path):
    p2v_file_path = path_prefix + ".p2v.vectors"
    redun_file_path = path_prefix + ".redundant"
    p2v_file = open(p2v_file_path, 'r', encoding='utf-8')
    p2v_dictionary = json.load(p2v_file)
    p2v_file.close()

    redun_file = open(redun_file_path, 'r', encoding='utf-8')
    redun_dictionary = json.load(redun_file)
    redun_file.close()

    save_dic = {}
    save_file = open(save_path, 'w')

    for path_method in path_method_list:
        if path_method in p2v_dictionary:
            save_dic[path_method] = p2v_dictionary[path_method]
            # save_file.write(path_method+"$"+p2v_dictionary[path_method] + '\n')
            print("get vector from p2v dictionary!")
        else:
            ast_path_lists = get_other_values_from_dictionary(redun_dictionary, value=path_method)
            # method存在于多个ast path的问题?
            ast_path_lists_size = len(ast_path_lists)
            if ast_path_lists_size == 0:
                pm_parts = path_method.split(sep)
                me_parts = pm_parts[1].split(' ')
                ret_type = me_parts[0]
                # print(ret_type[-2:])
                # problem for AST can not parse return type of array
                if ret_type.endswith('[]'):
                    # ret_type = ret_type[:-2]
                    new_path_method = pm_parts[0] + sep + ret_type[:-2] + ' '
                    for i in range(1, len(me_parts)):
                        new_path_method += me_parts[i] + ' '
                    new_path_method = new_path_method.strip()
                    # print(new_path_method)
                    if new_path_method in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[new_path_method]
                        # save_file.write(path_method+"$"+p2v_dictionary[new_path_method] + '\n')
                        print("successfully to find in p2v by modifying return type (remove [])")
                    else:
                        new_ast_path_lists = get_other_values_from_dictionary(redun_dictionary, value=new_path_method)
                        new_ast_path_lists_size = len(ast_path_lists)
                        if new_ast_path_lists_size == 0:
                            # save_file.write(new_path_method+"$"+'\n')
                            print("[ " + path_method +
                                  " ] return type is array, try to remove [], but can not found in same AST Path! ")
                        elif new_ast_path_lists_size > 1:
                            random_choice = random.randint(0, new_ast_path_lists_size-1)
                            new_ast_path_list = new_ast_path_lists[random_choice]
                            for pm in new_ast_path_list:
                                if pm in p2v_dictionary:
                                    save_dic[path_method] = p2v_dictionary[pm]
                                    # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                                    print(path_method + " exists in " + str(ast_path_lists_size) +
                                          " AST Path, and randomly choose No." + str(random_choice) + " path.")
                                    break
                        else:
                            new_ast_path_list = new_ast_path_lists[0]
                            for pm in new_ast_path_list:
                                if pm in p2v_dictionary:
                                    # print(p2v_dictionary[pm])
                                    save_dic[path_method] = p2v_dictionary[pm]
                                    # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                                    print("successfully to find in redundant dictionary by remove [].")
                                    break
                else:
                    # save_file.write(path_method+"$"+'\n')
                    print("[ " + path_method + " ] can not found in same AST Path! ")
            elif ast_path_lists_size > 1:
                random_choice = random.randint(0, ast_path_lists_size - 1)
                ast_path_list = ast_path_lists[random_choice]
                for pm in ast_path_list:
                    if pm in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[pm]
                        # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                        print(path_method + " exists in " + str(ast_path_lists_size) +
                              " AST Path, and randomly choose No." + str(random_choice) + " path.")
                        break
            else:
                ast_path_list = ast_path_lists[0]
                for pm in ast_path_list:
                    if pm in p2v_dictionary:
                        save_dic[path_method] = p2v_dictionary[pm]
                        # save_file.write(path_method + "$" + p2v_dictionary[pm] + '\n')
                        print("get vector from redundant dictionary!")

    json.dump(save_dic, save_file)
    # save_file.write(json.dumps(save_dic))


def get_other_values_from_dictionary(ast_dictionary, value):
    return [v for k, v in ast_dictionary.items() if value in v]


def get_buggy_method_vector_list(csv_dir_path, source_code_dir):
    list = []

    pms_splitor = '外'
    intern_pm_splitor = '内'

    # analyse csv file, add path_method to "query_pm" list
    for file in os.listdir(csv_dir_path):
        if file == ".DS_Store":
            continue
        file_path = os.path.join(csv_dir_path, file)

        if not os.path.isdir(file_path):
            for line in open(file_path):
                line = line.rstrip('\n')
                parts = line.split('\t')
                parts_len = len(parts)
                project_name = parts[0]
                br_id = parts[1]
                project_str = project_name + '_' + br_id
                # print(project_str + " , len: " + str(parts_len))

                if parts_len >= 5:
                    modified = parts[4]
                    if len(modified) > 0:
                        path_name_list = modified.split(pms_splitor)
                        for path_name_str in path_name_list:
                            path_name_parts = path_name_str.split(intern_pm_splitor)
                            path = path_name_parts[0]
                            name = path_name_parts[1]
                            path = source_code_dir + "/" + project_str + "/" + path
                            # print("path : " + path)
                            # print("name : " + name)

                            query_pm = path + sep + name
                            query_pm = query_pm.strip()
                            # print(query_pm)
                            list.append(query_pm)
                    if parts_len == 7:
                        deleted = parts[6]
                        if len(deleted) > 0:
                            path_name_list = modified.split('外')
                            for path_name_str in path_name_list:
                                path_name_parts = path_name_str.split('内')
                                path = path_name_parts[0]
                                name = path_name_parts[1]
                                path = source_code_dir + "/" + project_str + "/" + path
                                # print("path : " + path)
                                # print("name : " + name)

                                query_pm = path + sep + name
                                query_pm = query_pm.strip()
                                # print(query_pm)
                                list.append(query_pm)

    return list


def export_normal_method_vector(buggy_method_list, path_prefix, save_path):

    # buggy_path_name remove "[]" -> buggy_dic
    for index in range(0, len(buggy_method_list)):
        path_method = buggy_method_list[index]
        pm_parts = path_method.split(sep)
        me_parts = pm_parts[1].split(' ')
        ret_type = me_parts[0]
        # problem for AST can not parse return type of array
        if ret_type.endswith('[]'):
            new_path_method = pm_parts[0] + sep + ret_type[:-2] + ' '
            for i in range(1, len(me_parts)):
                new_path_method += me_parts[i] + ' '
            new_path_method = new_path_method.strip()
            buggy_method_list[index] = new_path_method
            # print(new_path_method)

    save_dic = {}
    save_file = open(save_path, 'w')

    # get dictionary vectors in '.p2v'
    p2v_file_path = path_prefix + ".p2v.vectors"
    p2v_file = open(p2v_file_path, 'r', encoding = 'utf-8')
    p2v_dictionary = json.load(p2v_file)
    p2v_file.close()

    # p2v  ->  vectors not in buggy_dic
    for key in p2v_dictionary:
        if key not in buggy_method_list:
            save_dic[key]=p2v_dictionary[key]
            # save_file.write(key + "$" + p2v_dictionary[key] + '\n')

    # get dictionary in '.redundant'
    redun_file_path = path_prefix + ".redundant"
    redun_file = open(redun_file_path, 'r', encoding = 'utf-8')
    redun_dictionary = json.load(redun_file)
    redun_file.close()

    # redundant -> vectors except [0] and not in buggy_dic
    for key in redun_dictionary:
        pm_list = redun_dictionary[key]
        list_size = len(pm_list)
        if list_size == 1:
            continue

        # find vector
        code_vector = []
        for pm in pm_list:
            if pm in p2v_dictionary:
                code_vector = p2v_dictionary[pm]
                break

        if len(code_vector) > 0:
            for index in range(1, len(pm_list)):
                pm = pm_list[index]
                if pm not in buggy_method_list:
                    save_dic[pm] =code_vector
                    # save_file.write(pm + "$" + code_vector + "\n")
        else:
            print("code vector not found!")

    json.dump(save_dic, save_file)
    # save_file.write(json.dumps(save_dic))
    return


def get_buggy_method_vector_list_for_ist(csv_dir_path, source_code_dir):
    list = []

    pms_splitor = '外'
    intern_pm_splitor = '内'

    # analyse csv file, add path_method to "query_pm" list
    for file in os.listdir(csv_dir_path):
        if file == ".DS_Store":
            continue
        file_path = os.path.join(csv_dir_path, file)

        if not os.path.isdir(file_path):
            for line in open(file_path):
                # line = line.rstrip('\n')
                parts = line.split('\t')
                parts_len = len(parts)
                project_name = parts[0]
                modified = parts[1]
                if len(modified) > 0:
                    path_name_list = modified.split(pms_splitor)
                    for path_name_str in path_name_list:
                        path_name_parts = path_name_str.split(intern_pm_splitor)
                        path = path_name_parts[0]
                        name = path_name_parts[1]
                        path = source_code_dir + "/" + path
                        query_pm = path + sep + name
                        query_pm = query_pm.strip()
                        list.append(query_pm)

    return list


# dataset_path_prefix = "data/mydataset0815/mydataset0815"
# buggy_methods_dir = "tmp_bm"
# source_code_dir = "data/rjc0815"
# buggy_vectors_output_path = "vectors_output/buggy"
# normal_vectors_output_path = "vectors_output/normal"
#
#
# construct_p2v_dictionary(path_prefix = dataset_path_prefix)
# buggy_method_list = get_buggy_method_vector_list(csv_dir_path = buggy_methods_dir, source_code_dir = source_code_dir)
# export_buggy_method_vector(buggy_method_list, path_prefix = dataset_path_prefix, save_path = buggy_vectors_output_path)
# export_normal_method_vector(buggy_method_list, path_prefix = dataset_path_prefix, save_path = normal_vectors_output_path)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-prf", "--dataset_path_prefix", dest = "dataset_path_prefix", required = True)
    parser.add_argument("-bgd", "--buggy_methods_dir", dest = "buggy_methods_dir", required = True)
    parser.add_argument("-scd", "--source_code_dir", dest = "source_code_dir", required = True)
    parser.add_argument("-bvop", "--buggy_vectors_output_path", dest = "buggy_vectors_output_path", required = True)
    parser.add_argument("-nbop", "--normal_vectors_output_path", dest = "normal_vectors_output_path", required = True)

    args = parser.parse_args()
    dataset_path_prefix = args.dataset_path_prefix
    buggy_methods_dir = args.buggy_methods_dir # abs
    source_code_dir = args.source_code_dir  # "data/istDat4exp"
    buggy_vectors_output_path = args.buggy_vectors_output_path
    normal_vectors_output_path = args.normal_vectors_output_path

    construct_p2v_dictionary(path_prefix = dataset_path_prefix)  # 没问题

    buggy_method_list = get_buggy_method_vector_list_for_ist(csv_dir_path = buggy_methods_dir, source_code_dir = source_code_dir)

    for i in range(100):
        print(buggy_method_list[i])
    export_buggy_method_vector_for_ist(buggy_method_list, path_prefix = dataset_path_prefix,
                               save_path = buggy_vectors_output_path)
    export_normal_method_vector(buggy_method_list, path_prefix = dataset_path_prefix,
                                save_path = normal_vectors_output_path)