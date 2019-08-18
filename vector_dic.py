import os
import json

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
    save_file.write(json.dumps(p2v_dictionary))
    print("p2v dictionary save to: " + save_path)


def path_method2vector(path_method_list, path_prefix, save_path):
    p2v_file_path = path_prefix + ".p2v.vectors"
    redun_file_path = path_prefix + ".redundant"
    p2v_file = open(p2v_file_path, 'r', encoding='utf-8')
    p2v_dictionary = json.load(p2v_file)
    p2v_file.close()

    redun_file = open(redun_file_path, 'r', encoding='utf-8')
    redun_dictionary = json.load(redun_file)
    redun_file.close()

    save_file = open(save_path, 'w')

    for path_method in path_method_list:
        if path_method in p2v_dictionary:
            save_file.write(p2v_dictionary[path_method] + '\n')
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
                    print(new_path_method)
                    if new_path_method in p2v_dictionary:
                        save_file.write(p2v_dictionary[new_path_method] + '\n')
                        print("successfully to find in p2v by modifying return type (remove [])")
                    else:
                        new_ast_path_lists = get_other_values_from_dictionary(redun_dictionary, value=new_path_method)
                        new_ast_path_lists_size = len(ast_path_lists)
                        if new_ast_path_lists_size == 0:
                            save_file.write('\n')
                            print("[ " + path_method + " ] return type is array, but can not found in same AST Path! ")
                        elif new_ast_path_lists_size > 1:
                            save_file.write('\n')
                            print(path_method + " exists in " + str(ast_path_lists_size) + " AST Path.")
                        else:
                            new_ast_path_list = new_ast_path_lists[0]
                            for pm in new_ast_path_list:
                                if pm in p2v_dictionary:
                                    # print(p2v_dictionary[pm])
                                    save_file.write(p2v_dictionary[pm] + '\n')
                                    print("successfully to find in redundant dictionary by remove []")
                else:
                    save_file.write('\n')
                    print("[ " + path_method + " ] can not found in same AST Path! ")
            elif ast_path_lists_size > 1:
                save_file.write('\n')
                print(path_method + " exists in " + str(ast_path_lists_size) + " AST Path.")
            else:
                ast_path_list = ast_path_lists[0]
                for pm in ast_path_list:
                    if pm in p2v_dictionary:
                        save_file.write(p2v_dictionary[pm] + '\n')
                        print("get vector from redundant dictionary!")


def get_other_values_from_dictionary(ast_dictionary, value):
    return [v for k, v in ast_dictionary.items() if value in v]


def read_pm_from_csv(csv_dir_path, save_path):
    dir_prefix = "data/rjc0815/"
    list = []

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
                        path_name_list = modified.split('外')
                        for path_name_str in path_name_list:
                            path_name_parts = path_name_str.split('内')
                            path = path_name_parts[0]
                            name = path_name_parts[1]
                            path = dir_prefix + project_str + "/" + path
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
                                path = dir_prefix + project_str + "/" + path
                                # print("path : " + path)
                                # print("name : " + name)

                                query_pm = path + sep + name
                                query_pm = query_pm.strip()
                                # print(query_pm)
                                list.append(query_pm)

    path_method2vector(list, path_prefix = "data/mydataset0815/mydataset0815", save_path = save_path)


construct_p2v_dictionary(path_prefix="data/mydataset0815/mydataset0815")

read_pm_from_csv("tmp_bm", "tmp_bm/time_cv")






# vector = path_method2vector(path_method="data/rawjavacode0808/my_test_dir/Time_11/java/org/joda/time/field/DecoratedDateTimeField.java\u5185DateTimeField getWrappedField()",
#                             p2v_file_path="data/mydataset0814/mydataset0814.p2v.vectors",
#                             redun_file_path="data/mydataset0814/mydataset0814.redundant")
#
# print(vector)
#
#
# vector = path_method2vector(path_method="data/rawjavacode0808/my_test_dir/Time_11/java/org/joda/time/field/DelegatedDateTimeField.java\u5185DateTimeField getWrappedField()",
#                             p2v_file_path="data/mydataset0814/mydataset0814.p2v.vectors",
#                             redun_file_path="data/mydataset0814/mydataset0814.redundant")
# print(vector)
