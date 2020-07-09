'''
@Author: Gao S
@Date: 2020-07-06 17:22:08
@LastEditTime: 2020-07-09 15:39:48
@Description: 
@FilePath: /English-Translation/user_info.py
'''

from database import userInfoDb, userIdDb, corpusDb

# import atexit

complexities = ['complex', 'subcomplex', 'medium', 'submedium', 'ease', 'permanent']

class UserInfo(object):
    def __init__(self, user_id):
        """初始化
        调用前确保已经登录
        Args:
            user_id (str): 用户名/id
        """
        super().__init__()
        self.__user_id = user_id
        dict_msg = userInfoDb.get_dict(self.__user_id)
        self.user_info_dict = dict_msg[0]
        
        if 'finish_id' not in self.user_info_dict:
            self.user_info_dict['finish_id'] = {'complex':[], 
                                                'subcomplex':[], 
                                                'medium':[], 
                                                'submedium':[], 
                                                'ease':[], 
                                                'permanent':[]}
        if 'finish_history' not in self.user_info_dict:
            self.user_info_dict['finish_history'] = {}
        if 'pass_id' not in self.user_info_dict:
            self.user_info_dict['pass_id'] = []
            
        self.__corpus_len = corpusDb.get_corpus_len()
        
        # atexit.register(self.write_dict)
        
    def __enter__(self):
        return self    
        
    def __exit__(self, exception_type, exception_value, traceback):
        self.write_dict()
        
        
    # TODO 得到corpus的题目数
    
    def __get_all_question_id(self):
        """得到所有做过的题目id

        Returns:
            list: 所有做过的题目id
        """
        question_id_list = list(self.user_info_dict['finish_history'].keys())
        question_id_list = question_id_list + self.user_info_dict['pass_id']
        
        return question_id_list
        
    def __get_max_question_id(self):
        """得到已做题目最大编号
        用于做新题目时得到新题目
        Returns:
            str: 已做题目最大编号
        """
        all_question_id = self.__get_all_question_id()
        if len(all_question_id) == 0:
            return '0'
        max_question_id = str(max(map(lambda x: int(x), all_question_id)))

        return max_question_id
    
    def insert_pass(self, question_id):
        """用户跳过问题后插入user_info
        
        Args:
            question_id (str): 题目id
        """
        # TODO 错误处理
        self.user_info_dict['pass_id'].append(question_id)
    
    def get_new_question(self):
        """得到新题目，每次一个

        Returns:
            str, str, str: 中文句子和英文句子，问题id
        """
        max_question_id = int(self.__get_max_question_id())
        question_id = str(max_question_id+1)
        # TODO 判断不会超出数据库长度
        # TODO 错误处理
        
        chinese, english = corpusDb.get_corpus(question_id)
        return chinese, english, question_id
    
    def get_review_question(self):
        """得到复习题目，每次一个

        Returns:
            str, str, str, str: 中文句子和英文句子，第三个为复杂度，最后为问题id；
                如果没有可复习题目，返回None
        """
        # TODO 错误处理
        if len(self.user_info_dict['finish_id']['complex']) != 0:
            question_id = self.user_info_dict['finish_id']['complex'].pop(0)
            chinese, english = corpusDb.get_corpus(question_id)
            
            return chinese, english, 'complex', question_id
        
        elif len(self.user_info_dict['finish_id']['subcomplex']) != 0:
            question_id = self.user_info_dict['finish_id']['subcomplex'].pop(0)
            chinese, english = corpusDb.get_corpus(question_id)
            
            return chinese, english, 'subcomplex', question_id
        
        elif len(self.user_info_dict['finish_id']['medium']) != 0:
            question_id = self.user_info_dict['finish_id']['medium'].pop(0)
            chinese, english = corpusDb.get_corpus(question_id)
            
            return chinese, english, 'medium', question_id
        
        elif len(self.user_info_dict['finish_id']['submedium']) != 0:
            question_id = self.user_info_dict['finish_id']['submedium'].pop(0)
            chinese, english = corpusDb.get_corpus(question_id)
            
            return chinese, english, 'submedium', question_id
        
        elif len(self.user_info_dict['finish_id']['ease']) != 0:
            question_id = self.user_info_dict['finish_id']['ease'].pop(0)
            chinese, english = corpusDb.get_corpus(question_id)
            
            return chinese, english, 'ease', question_id

        return None, None, '没有可复习的题目', None
    
    def __insert_question(self, question_id, answer, complexity):
        """将题号及回答按复杂度插入字典

        Args:
            question_id (str): 题号
            answer (str): 回答
            complexity (str): 复杂度
        """
        # 插入复杂度排列的字典
        self.user_info_dict['finish_id'][complexity].append(question_id)
        # 插入书写历史
        if question_id not in self.user_info_dict['finish_history']:
            self.user_info_dict['finish_history'][question_id] = [answer]
        else:
            self.user_info_dict['finish_history'][question_id].append(answer)
    
    def insert_question(self, question_id, answer, complexity=None, move_level=None):
        """回答/复习问题后插入user_info
        如果指定复杂度，复杂度需要在函数外降级确定；
        如果不指定，则需要给出前后升降的级数
        Args:
            question_id (str): 题号
            answer (str): 回答
            complexity (str, optional): 目标复杂度；当move_level指定时为当前复杂度. Defaults to None.
            move_level (int, optional): 前后升降级的级数. Defaults to None.
        """
        if move_level is None:
            self.__insert_question(question_id, answer, complexity)
        elif move_level is not None:
            now_index = complexities.index(complexity)
            now_index += move_level
            now_index = max(0, min(5, now_index))
            complexity_new = complexities[now_index]
            
            self.__insert_question(question_id, answer, complexity_new)
        
    def get_history(self, question_id=None):
        """得到答题历史
        
        Args:
            question_id (str, optional): 如果非空，则返回指定题目id的历史. Defaults to None.

        Returns:
            list/dict: 当question_id指定时，返回list，否则返回dict
        """
        if question_id is not None:
            if question_id in self.user_info_dict['finish_history']:
                return self.user_info_dict['finish_history'][question_id]
            else:
                return None
        else:
            return self.user_info_dict['finish_history']
    
    def get_review_list(self, complexity=None):
        """得到按复杂度排列的字典

        Args:
            complexity (str, optional): 复杂度. Defaults to None.

        Returns:
            dict/None: 返回按复杂度排列的字典，如果指定复杂度，但关键字错误，则返回None
        """
        if complexity is not None:
            if complexity not in complexities:
                return None
            return self.user_info_dict['finish_id'][complexity]
        else:
            return self.user_info_dict['finish_id']
    
    def write_dict(self):
        """将user_info字典写入json文件
        """
        userInfoDb.write_dict(self.__user_id, self.user_info_dict)
    
    # TODO 升降级    
    
    # TODO 得到用户在某项上的历史回答
    
    # TODO 艾宾浩斯
    # TODO 得到用户
    # TODO 学习列表：根据艾宾浩斯等方式得到
    # TODO 学习任务，每日多少多少等
    
    # TODO 代码结束时，断开与数据库的连接
