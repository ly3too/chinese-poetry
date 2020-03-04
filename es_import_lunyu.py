from elasticsearch_dsl import *
import os
from glob import glob
import json
from . import to_zh_cn


class LunYu(Document):
    chapter = Text(analyzer='jieba_index', search_analyzer='jieba_search')
    paragraphs = Text(analyzer='jieba_index', search_analyzer='jieba_search')

    class Index:
        name = 'poetry_lunyu'
        settings = {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }


def do_es_import():
    """
    import data from current dir
    """
    LunYu.init()

    cur_dir = os.path.dirname((os.path.abspath(__file__)))
    data_files = glob("{}/lunyu/lunyu*.json".format(cur_dir))
    for file in data_files:
        with open(file, 'r') as f:
            data = json.load(f)
            for item in data:
                one = LunYu(**to_zh_cn(item))
                one.save()
