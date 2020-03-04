from elasticsearch_dsl import *
import os
from glob import glob
import json
import re
from . import to_zh_cn


class Ci(Document):
    dynasty = Text()
    author = Text()
    rhythmic = Text(analyzer='jieba_index', search_analyzer='jieba_search')
    paragraphs = Text(analyzer='jieba_index', search_analyzer='jieba_search')

    class Index:
        name = 'poetry_ci'
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }


class Author(Document):
    name = Text()
    desc = Text(analyzer='jieba_index', search_analyzer='jieba_search')
    short_desc = Text(analyzer='jieba_index', search_analyzer='jieba_search')

    class Index:
        name = 'author'
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }


def do_es_import():
    """
    import data from current dir
    """
    Ci.init()
    Author.init()

    patt = re.compile(r'^[a-zA-Z]+\.([a-zA-Z]+)\.')
    cur_dir = os.path.dirname((os.path.abspath(__file__)))
    # data_files = glob("{}/ci/ci.*.json".format(cur_dir))
    # for file in data_files:
    #     with open(file, 'r') as f:
    #         data = json.load(f)
    #         dynasty = patt.findall(os.path.basename(file))[0]
    #         for item in data:
    #             item["dynasty"] = dynasty
    #             one = Ci(**to_zh_cn(item))
    #             one.save()

    data_files = glob("{}/ci/author.*.json".format(cur_dir))
    for file in data_files:
        with open(file, 'r') as f:
            data = json.load(f)
            dynasty = patt.findall(os.path.basename(file))[0]
            for item in data:
                item["dynasty"] = dynasty
                item["desc"] = item["description"]
                item["short_desc"] = item["short_description"]
                del item["description"]
                del item["short_description"]
                one = Author(**to_zh_cn(item))
                one.save()
