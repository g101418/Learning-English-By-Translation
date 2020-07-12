'''
@Author: Gao S
@Date: 2020-07-12 17:59:27
@LastEditTime: 2020-07-12 19:58:14
@Description: 初始化项目DB及将语料写入数据库
@FilePath: /English-Translation/setup_db.py
'''
import os
import sqlite3 as sqlite
import shutil
import json
import numpy as np

from configparser import ConfigParser, ExtendedInterpolation
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config.ini')


def setup():
    # 如果db文件夹已经存在，则改名新建
    if os.path.exists(config['DB']['db_path']):
        old_db_name = os.path.join(os.path.split(
            config['DB']['db_path'])[0], 'db_old')
        shutil.move(config['DB']['db_path'], old_db_name)

    # 创建db文件夹
    os.mkdir(config['DB']['db_path'])
    # 创建user_info文件夹
    os.mkdir(config['DB']['user_info_db_path'])
    # 创建user_id.json
    with open(config['DB']['user_id_db_filename'], 'w') as f:
        f.write(json.dumps({}))

    # 创建corpus.db
    con = sqlite.connect(config['DB']['corpus_db_filename'])
    with con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE corpus(id INTEGER PRIMARY KEY AUTOINCREMENT, chinese TEXT, english TEXT)")


def insert_corpus_many(corpus: list):
    check_corpus = np.array(corpus)
    if len(check_corpus.shape) != 2:
        raise TypeError('corpus格式错误')
    if check_corpus.shape[1] != 2:
        raise TypeError('corpus格式错误')
    
    con = sqlite.connect(config['DB']['corpus_db_filename'])
    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO corpus(chinese, english) VALUES(?, ?)", corpus)

if __name__ == '__main__':
    setup()
    # corpus = [
    #     ('你好', 'hello'),
    #     ('你是谁？', 'Who are you?')
    # ]
    # insert_corpus_many(corpus)
