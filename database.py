'''
@Author: Gao S
@Date: 2020-07-06 08:49:36
@LastEditTime: 2020-07-06 17:31:48
@Description: 
@FilePath: /English-Translation/database.py
'''
import json
import hashlib


class UserIdDB(object):
    """用户管理
    登录、注册等事宜
    """
    def __init__(self, user_id_db_filename='./db/user_id.json'):
        super().__init__()
        self.__user_id_db_filename = user_id_db_filename
        try:
            with open(user_id_db_filename, 'r') as f:
                self.__user_id_db = json.load(f)
        except FileNotFoundError as e:
            print('找不到文件:', e.filename)
        except json.JSONDecodeError as e:
            print('json文件数据格式错误:', e)
                
    # TODO 检查用户名的合规性
    # def compliance_checks(self):
    #     
    #     pass
    
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
            print('找不到文件:', e.filename)
    
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
        # TODO 检查用户用户名密码...
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
        # TODO 检查用户名合规性
        
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
    
    def leave(self):
        print('拜拜')
    
# ! user_info应该写为分别以user_id挂名的文件
class UserInfoDB(object):
    """处理用户信息
    答题记录等
    """
    def __init__(self, user_info_db_filename='./db/user_info.json'):
        super().__init__()
        self.__user_info_db_filename = user_info_db_filename
        try:
            with open(user_info_db_filename, 'r') as f:
                self.__user_info_db = json.load(f)
        except FileNotFoundError as e:
            print('找不到文件:', e.filename)
        except json.JSONDecodeError as e:
            print('json文件数据格式错误:', e)
            
    def write_user_info_db(self):
        """将info字典写回文件
        """
        try:
            with open(self.user_info_db_filename, 'w') as f:
                f.write(json.dumps(self.__user_info_db))
        except FileNotFoundError as e:
            print('找不到文件:', e.filename)
            
    # TODO 函数：得到对应user_id的字典
    def get_dict(self, user_id):
        if user_id not in self.__user_info_db:
            return None, '记录中未包含该字典'
        
        return self.__user_info_db[user_id]
    
    def write_dict(self, user_id, user_dict, write_db=True):
        self.__user_info_db[user_id] = user_dict
        if write_db == True:
            self.write_user_info_db()
        
    
    
    # ! 以下应该在另一个class中处理 
    # TODO 函数：得到用户所有历史题号
    
    # TODO 函数：学习得到题号，每次一个题
    # TODO 函数：复习得到题号，每次一个题
    
    # TODO 函数：学习插入题号，每次一个题
    # TODO 函数：复习修正题号，每次一个题
    
    # TODO 得到用户在某项上的历史回答
    # TODO 艾宾浩斯
    # TODO 得到用户已经学习的列表
    # TODO 得到用户
    # TODO 学习列表：根据艾宾浩斯等方式得到
    # TODO 学习任务，每日多少多少等

class CorpusDB(object):
    # 平行语料库用SQLite管理
    pass


if __name__ == '__main__':
    pass
