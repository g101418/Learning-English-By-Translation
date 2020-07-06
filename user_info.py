'''
@Author: Gao S
@Date: 2020-07-06 17:22:08
@LastEditTime: 2020-07-06 21:18:06
@Description: 
@FilePath: /English-Translation/user_info.py
'''

from database import userInfoDb, userIdDb, corpusDb

class UserInfo(object):
    def __init__(self, user_id):
        """初始化
        调用前确保已经登录
        Args:
            user_id (str): 用户名/id
        """
        super().__init__()
        self.__user_id = user_id
        self.user_info_dict, _ = userInfoDb.get_dict(self.__user_id)
        if 'finish_id' not in self.user_info_dict:
            self.user_info_dict['finish_id'] = {'complex':[], 
                                                'subcomplex':[], 
                                                'medium':[], 
                                                'submedium':[], 
                                                'ease':[], 
                                                'permanent':[]}
        if 'finish_history' not in self.user_info_dict:
            self.user_info_dict['finish_history'] = {}
    
    # TODO 得到corpus的题目数
    
    def __get_all_question_id(self):
        """得到所有做过的题目id

        Returns:
            list: 所有做过的题目id
        """
        return list(self.user_info_dict['finish_history'].keys())
        
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
    
    def insert_question(self, question_id, complexity, answer):
        """回答新问题后插入user_info
        复杂度需要在函数外降级确定
        Args:
            question_id (str): 题目id
            complexity (str): 复杂度
            answer (str): 用户答案
        """
        # TODO 错误处理
        # 插入复杂度排列的字典
        self.user_info_dict['finish_id'][complexity].append(question_id)
        # 插入书写历史
        if question_id not in self.user_info_dict['finish_history']:
            self.user_info_dict['finish_history'][question_id] = [answer]
        else:
            self.user_info_dict['finish_history'][question_id].append(answer)
    
    def write_dict(self):
        userInfoDb.write_dict(self.__user_id, self.user_info_dict)
        
        
    # TODO 得到用户在某项上的历史回答
    
    # TODO 艾宾浩斯
    # TODO 得到用户
    # TODO 学习列表：根据艾宾浩斯等方式得到
    # TODO 学习任务，每日多少多少等
