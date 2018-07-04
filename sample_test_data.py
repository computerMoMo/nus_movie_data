# -*- coding:utf-8 -*-
import codecs
import random
import os
import numpy as np
import copy


def generate_fq_dict(alpha, origin_fq_dict):
    sum_pros = 0.0
    for item_id, item_fq in origin_fq_dict.items():
        sum_pros += item_fq**alpha

    new_item_fq_dict = dict()
    for item_id, item_fq in origin_fq_dict.items():
        new_item_fq_dict[item_id] = item_fq**alpha/sum_pros
    return new_item_fq_dict


def sample_with_fq(sample_num, item_fq_list):
    sample_id_list = []
    while True:
        temp_res = list(np.random.multinomial(sample_num*5, item_fq_list, 1)[0])
        if temp_res.count(0) <= len(item_fq_list)-sample_num:
            for idx, res in enumerate(temp_res):
                if res > 0:
                    sample_id_list.append((idx, res))
            sample_id_list = sorted(sample_id_list, key=lambda x: x[1], reverse=True)
            return [item[0] for item in sample_id_list[:100]]


if __name__ == "__main__":
    movie_file_reader = codecs.open("data/data_dict/movie_id.txt", mode="r", encoding="utf-8")
    movie_set = []
    for line in movie_file_reader.readlines():
        movie_set.append(line.strip())
    movie_file_reader.close()
    movie_set = set(movie_set)
    print("item numbers:", len(movie_set))

    train_reader = codecs.open("data/origin_data/user_rate_movie_train.txt", mode="r", encoding="utf-8")
    train_user_dict = dict()
    line = train_reader.readline()
    while line:
        line_list = line.strip().split("\t")
        if line_list[0] not in train_user_dict:
            train_user_dict[line_list[0]] = [line_list[1]]
        else:
            train_user_dict[line_list[0]].append(line_list[1])
        line = train_reader.readline()
    train_reader.close()
    print("train user numbers:", len(train_user_dict))
    for k, v in train_user_dict.items():
        train_user_dict[k] = set(v)

    test_reader = codecs.open("data/origin_data/test_pos_user_item.txt", mode="r", encoding="utf-8")
    test_pos_dict = dict()
    for line in test_reader.readlines():
        line_list = line.strip().split("\t")
        test_pos_dict[line_list[0]] = line_list[1:]
    test_reader.close()
    print("test user numbers:", len(test_pos_dict))

    item_fq_reader = codecs.open("data/movie_fq.txt", mode="r", encoding="utf-8")
    item_fq_dict = dict()
    for line in item_fq_reader.readlines():
        line_list = line.strip().split("\t")
        item_fq_dict[line_list[0]] = float(line_list[1])
    item_fq_reader.close()

    for alpha in [0.4, 0.6, 0.8, 1.0]:
        print("generate new item sample pros with alpha:", alpha)
        itemFqDict = generate_fq_dict(alpha=0.2, origin_fq_dict=item_fq_dict)

        test_writer = codecs.open("data/sample_data/user_item_test_"+str(alpha)+".txt", mode="w", encoding="utf-8")
        nums = 0
        for user_id, pos_item_list in test_pos_dict.items():
            pos_item_set = set(pos_item_list)
            train_set = train_user_dict[user_id]

            neg_item_list = list(movie_set-pos_item_set-train_set)
            item_fq_list = [itemFqDict[item_id] for item_id in neg_item_list]

            for pos_item_id in pos_item_list:
                sample_id_list = sample_with_fq(sample_num=100, item_fq_list=item_fq_list)
                neg_item_id_list = [neg_item_list[idx] for idx in sample_id_list]
                test_writer.write(k + "\t" + pos_item_id + "\t" + "1.0\n")
                for neg_id in neg_item_id_list:
                    test_writer.write(k + "\t" + neg_id + "\t" + "0.0\n")
            nums += 1
            if nums % 100 == 0:
                print(nums)
        test_writer.close()
