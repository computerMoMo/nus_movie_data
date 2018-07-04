# -*- coding:utf-8 -*-
import codecs
import os

dataDir = os.path.join(os.path.dirname(__file__), "data")


class ckeDataFormat:
    def __init__(self):
        self.max_attribute_num = 15
        self.padding_id = 0

        self.re_entity_id_dict = dict()
        re_entity_reader = codecs.open(os.path.join(dataDir, "data_dict/re_entity_id.txt"), mode="r")
        line = re_entity_reader.readline()
        while line:
            line_list = line.strip().split("\t")
            self.re_entity_id_dict[line_list[0]] = line_list[1]
            line = re_entity_reader.readline()
        re_entity_reader.close()

        self.item_person_dict = dict()
        item_person_reader = codecs.open(os.path.join(dataDir, "origin_data/joined_principal.txt"), mode="r")
        head_line = item_person_reader.readline()
        line = item_person_reader.readline()
        while line:
            line_list = line.strip().split("\t")
            if line_list[0] not in self.item_person_dict:
                self.item_person_dict[line_list[0]] = [line_list[1]+"_"+line_list[2]]
            else:
                self.item_person_dict[line_list[0]].append(line_list[1]+"_"+line_list[2])
            line = item_person_reader.readline()
        item_person_reader.close()

        self.item_type_dict = dict()
        item_type_reader = codecs.open(os.path.join(dataDir, "origin_data/joined_movie_type.txt"), mode="r")
        head_line = item_type_reader.readline()
        line = item_type_reader.readline()
        while line:
            line_list = line.strip().split("\t")
            if line_list[0] not in self.item_type_dict:
                self.item_type_dict[line_list[0]] = ["belong_" + line_list[1]]
            else:
                self.item_type_dict[line_list[0]].append("belong_" + line_list[1])
            line = item_type_reader.readline()
        item_type_reader.close()

        self.item_id_dict = dict()
        item_id_reader = codecs.open(os.path.join(dataDir, "data_dict/movie_id_to_int.txt"), mode="r")
        for line in item_id_reader.readlines():
            line_list = line.strip().split("\t")
            self.item_id_dict[line_list[1]] = line_list[0]
        item_id_reader.close()

    def get_item_attr(self, item_id):
        item_attr_id_list = []
        imdb_id = self.item_id_dict[item_id]

        re_person_list = self.item_person_dict[imdb_id]
        for item in re_person_list:
            item_attr_id_list.append(int(self.re_entity_id_dict[item]))

        re_type_list = self.item_type_dict[imdb_id]
        for item in re_type_list:
            item_attr_id_list.append(int(self.re_entity_id_dict[item]))
        while len(item_attr_id_list) < self.max_attribute_num:
            item_attr_id_list.append(self.padding_id)

        return item_attr_id_list


# use case
if __name__ == "__main__":
    demo_cke = ckeDataFormat()

    file_reader = codecs.open(os.path.join(dataDir, "sample_data/user_item_test_0.0.txt"), mode="r", encoding="utf-8")
    line = file_reader.readline()
    while line:
        line_list = line.strip().split("\t")
        user_id = line_list[0]
        item_id = line_list[1]
        label = line_list[2]
        item_attr_id_list = demo_cke.get_item_attr(item_id=item_id)
        print("user id:", user_id)
        print("item id:", item_id)
        print("attribute id list:", item_attr_id_list)
        print("label:", label)
        line = file_reader.readline()
        break

