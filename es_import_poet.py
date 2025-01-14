from elasticsearch_dsl import *
import os
from glob import glob
import json
import re
from . import to_zh_cn


class Poet(Document):
    dynasty = Text()
    author = Text()
    title = Text(analyzer='jieba_index', search_analyzer='jieba_search')
    paragraphs = Text(analyzer='jieba_index', search_analyzer='jieba_search')

    class Index:
        name = 'poetry_shi'
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }


class Author(Document):
    name = Text()
    desc = Text(analyzer='jieba_index', search_analyzer='jieba_search')

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
    Poet.init()
    Author.init()

    patt = re.compile(r'^[a-zA-Z]+\.([a-zA-Z]+)\.')
    cur_dir = os.path.dirname((os.path.abspath(__file__)))
    data_files = glob("{}/json/poet.*.json".format(cur_dir))
    for file in data_files:
        with open(file, 'r') as f:
            data = json.load(f)
            dynasty = patt.findall(os.path.basename(file))[0]
            for item in data:
                item["dynasty"] = dynasty
                one = Poet(**to_zh_cn(item))
                one.save()

    data_files = glob("{}/json/authors.*.json".format(cur_dir))
    for file in data_files:
        with open(file, 'r') as f:
            data = json.load(f)
            dynasty = patt.findall(os.path.basename(file))[0]
            for item in data:
                item["dynasty"] = dynasty
                one = Author(**to_zh_cn(item))
                one.save()
