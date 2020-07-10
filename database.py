'''
@Author: Gao S
@Date: 2020-07-06 08:49:36
@LastEditTime: 2020-07-09 17:29:22
@Description: 
@FilePath: /English-Translation/database.py
'''
import json
import hashlib
import os
import logging
import sqlite3 as sqlite
import sys
import re

class UserIdDB(object):
    """用户管理
    登录、注册等事宜
    """
    def __init__(self, user_id_db_filename='./db/user_id.json'):
        """初始化

        Args:
            user_id_db_filename (str, optional): user_id.json路径. Defaults to './db/user_id.json'.
        """
        super().__init__()
        self.__user_id_db_filename = user_id_db_filename
        try:
            with open(self.__user_id_db_filename, 'r') as f:
                self.__user_id_db = json.load(f)
        except FileNotFoundError as e:
            logging.error('找不到文件: ' + e.filename)
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error('json文件数据格式错误: ' + self.__user_id_db_filename)
            sys.exit(1)
                
    def user_id_format(self, user_id):
        """检查用户名合规性

        Args:
            user_id (str): 用户名/id

        Returns:
            bool, str: 是否匹配到，第二个是描述
        """
        NUM_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")   #数字和字母组合，不允许纯数字
        FIRST_LETTER = re.compile("^[a-zA-Z]")  #只能以字母开头
        length = len(user_id)
        
        if length >= 5:
            if length <= 20:
                if NUM_LETTER.search(user_id):
                    if FIRST_LETTER.search(user_id):
                        return True, '用户名符合规范'
                    else:
                        return False, '应该以字母开头'
                else:
                    return False, '包含非法字符'
            else:
                return False, '长度过长'
        else:
            return False, '长度过短'
        
    def user_password_format(self, user_password):
        """检查密码合规性

        Args:
            user_password (str): 密码

        Returns:
            bool, str: 是否匹配到，第二个是描述
        """
        length = len(user_password)
        
        if length >= 5:
            if length <= 20:
                return True, '密码符合规范'
            else:
                return False, '密码过长'
        else:
            return False, '密码过短'
        
        
    def __get_password_hex(self, user_password):
        """得到密码的MD5表示

        Args:
            user_password (str): 密码

        Returns:
            str: 密码的MD5表示
        """
        password = hashlib.md5(user_password.encode()).hexdigest()
        return password
    
    def __write_user_id_db(self):
        """将id字典写回文件
        """
        try:
            with open(self.__user_id_db_filename, 'w') as f:
                f.write(json.dumps(self.__user_id_db))
        except FileNotFoundError as e:
            logging.error('无法写入文件: ' + e.filename)
            sys.exit(1)
    
    def __check_id_exist(self, user_id):
        """检查用户名是否存在

        Args:
            user_id (str): 用户名/id

        Returns:
            (Bool, str): True为存在，False不存在，第二个返回值为描述
        """
        if user_id in self.__user_id_db:
            return True, '用户名已存在'
        else:
            return False, '用户名不存在'
    
    def __check_user_id_password(self, user_id, user_password, check_id_exist=False):
        """检查用户名密码是否匹配

        Args:
            user_id (str): 用户名/id
            user_password (str): 密码
            check_id_exist (bool, optional): 是否检查用户名存在. Defaults to False.

        Returns:
            (Bool, str): True为匹配，False不匹配，第二个返回值为描述
        """
        if check_id_exist == True:
            check_id_bool, check_id_msg = self.__check_id_exist(user_id)
            if check_id_bool == False:
                return False, check_id_msg
        
        password = self.__get_password_hex(user_password)
        if password == self.__user_id_db[user_id]:
            return True, '账号密码匹配'
        else:
            return False, '密码错误'
        
    
    def register(self, user_id, user_password):
        """用户注册

        Args:
            user_id (str): 用户名/id
            user_password (str): 密码

        Returns:
            (Bool, str): True为注册成功，第二个返回值为描述
        """
        # 处理id
        # 检查用户名合规性
        check_id_bool, check_id_msg = self.user_id_format(user_id)
        if check_id_bool == False:
            return False, check_id_msg
        # 检查密码合规性
        check_id_bool, check_id_msg = self.user_password_format(user_password)
        if check_id_bool == False:
            return False, check_id_msg
        
        check_id_bool, check_id_msg = self.__check_id_exist(user_id)
        if check_id_bool == True:
            return False, check_id_msg
        
        password = self.__get_password_hex(user_password)
        
        self.__user_id_db[user_id] = password
        self.__write_user_id_db()
        
        return True, '注册成功'
        
    def unregister(self, user_id, user_password):
        """用户注销

        Args:
            user_id (str): 用户名/id
            user_password (str): 密码

        Returns:
            (Bool, str): True为注销成功，第二个返回值为描述
        """
        # 检查账号密码相关
        check_bool, check_msg = self.__check_user_id_password(user_id, user_password, check_id_exist=True)
        if check_bool == False:
            return False, check_msg
        
        del self.__user_id_db[user_id]
        self.__write_user_id_db()
        
        return True, '注销成功'
    
    def change_password(self, user_id, user_password_old, user_password_new):
        """修改用户密码

        Args:
            user_id (str): 用户名/id
            user_password_old (str): 旧密码
            user_password_new (str): 新密码

        Returns:
            (Bool, str): True为修改密码成功，第二个返回值为描述
        """
        check_id_bool, check_id_msg = self.user_password_format(user_password_new)
        if check_id_bool == False:
            return False, check_id_msg
        
        # 检查用户名、密码相关
        check_bool, check_msg = self.__check_user_id_password(user_id, user_password_old, check_id_exist=True)
        if check_bool == False:
            return False, check_msg
        
        password = self.__get_password_hex(user_password_new)
        
        self.__user_id_db[user_id] = password
        self.__write_user_id_db()
        
        return True, '修改密码成功'
        
    
    def login(self, user_id, user_password):
        """用户登录

        Args:
            user_id (str): 用户名/id
            user_password (str): 密码

        Returns:
            (Bool, str): True为登录成功，第二个返回值为描述
        """
        # 检查用户名、密码相关
        check_bool, check_msg = self.__check_user_id_password(user_id, user_password, check_id_exist=True)
        if check_bool == False:
            return False, check_msg

        return True, '登录成功'
    

class UserInfoDB(object):
    """处理用户信息
    答题记录等
    """
    def __init__(self, user_info_db_path='./db/user_info/'):
        """初始化

        Args:
            user_info_db_path (str, optional): user_info文件夹. Defaults to './db/user_info/'.
        """
        super().__init__()
        self.__user_info_db_path = user_info_db_path
        
            
    def get_dict(self, user_id, build_file=True):
        """得到对应user_id的相关字典
        调用前确保用户已经登录
        Args:
            user_id (str): 用户名/id
            build_file (bool, optional): 是否在缺失文件时返回空字典. Defaults to False.
            
        Returns:
            dict, str: 若非None，则返回字典，第二个返回值为描述
        """
        files = os.listdir(self.__user_info_db_path)
        files = [f for f in files if f.endswith('.json') and f.startswith('user_id_')]
        files = map(lambda x:os.path.splitext(x)[0].replace('user_id_', ''), files)
        
        if user_id not in files:
            if build_file == True:
                return {}, '首次构造记录，为空'
            else:
                return None, '记录中未包含该字典'
        
        filename = self.__user_info_db_path+'user_id_'+user_id+'.json'
        try:
            with open(filename, 'r') as f:
                user_info_db = json.load(f)
        except FileNotFoundError as e:
            logging.error('找不到文件: ' + e.filename)
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error('json文件数据格式错误: ' + filename)
            sys.exit(1)
        
        return user_info_db, '返回该字典'
    
    def write_dict(self, user_id, user_dict):
        filename = self.__user_info_db_path+'user_id_'+user_id+'.json'
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(user_dict))
        except FileNotFoundError as e:
            logging.error('无法写入文件: ' + e.filename)
            sys.exit(1)
        


class CorpusDB(object):
    # 平行语料库用SQLite管理
    def __init__(self, corpus_db_filename='./db/corpus.db'):
        super().__init__()
        self.__corpus_db_filename = corpus_db_filename
        self.build_connection()
        self.__corpus_len = self.get_corpus_len()
    
    def __del__(self):
        self.close_connection()

    def get_corpus_len(self):
        cur = self.connection.cursor()
        cur.execute("SELECT count(id) from corpus")
        row = cur.fetchone()
        
        return row[0]

    def get_corpus(self, question_id):
        """得到中英文语料

        Args:
            question_id (str): 语料id

        Returns:
            str, str: 中文句子和英文句子，为空或者出错返回None
        """
        if int(question_id) > self.__corpus_len:
            logging.error('数据库检索时题号超出总长: ' + str(question_id))
            return None, None
        
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT * FROM corpus where id={}".format(question_id))
            row = cur.fetchone()
        except sqlite.DatabaseError as e:
            logging.error('数据库检索错误: ' + str(e))
            return None, None
        
        return row[1], row[2]
    
    def close_connection(self):
        """断开与数据库的连接
        """
        self.connection.close()
    
    def build_connection(self):
        """与数据库建立连接
        """
        try:
            self.connection = sqlite.connect(self.__corpus_db_filename)
        except sqlite.Error as e:
            logging.error('数据库错误: ' + str(e))
            sys.exit(1)
    
    
userIdDb = UserIdDB()
userInfoDb = UserInfoDB()
corpusDb = CorpusDB()

if __name__ == '__main__':
    pass


# TODO 平行语料数据库的构建