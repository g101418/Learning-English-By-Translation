'''
@Author: Gao S
@Date: 2020-07-10 21:54:11
@LastEditTime: 2020-07-12 20:31:05
@Description: 交互式命令行的实现
@FilePath: /English-Translation/interaction.py
'''
from transitions import Machine
from enum import Enum
from cmd import Cmd

from user_info import UserInfo
from database import userIdDb

import logging
logging.basicConfig(level=logging.WARNING)

class InteractionState(Enum):
    start = 0
    finish = 1
    login = 2
    register = 3
    study = 4
    learnnew = 5
    review = 6
    answer = 7
    skip = 8
    
class InteractionMachine(Machine):
    def __init__(self):
        
        transitions = [['login', InteractionState.start, InteractionState.login],
                       ['register', InteractionState.start, InteractionState.register],
                       ['study', InteractionState.login, InteractionState.study],
                       ['study', InteractionState.register, InteractionState.study],
                       ['learnnew', InteractionState.study, InteractionState.learnnew],
                       ['review', InteractionState.study, InteractionState.review],
                       ['answer', InteractionState.learnnew, InteractionState.answer],
                       ['answer', InteractionState.review, InteractionState.answer],
                       ['skip', InteractionState.learnnew, InteractionState.skip],
                       ['skip', InteractionState.review, InteractionState.skip],
                       ['study', InteractionState.answer, InteractionState.study],
                       ['study', InteractionState.skip, InteractionState.study],
                       ['exit', InteractionState.login, InteractionState.start],
                       ['exit', InteractionState.register, InteractionState.start],
                       ['exit', InteractionState.start, InteractionState.finish],
                       ['exit', InteractionState.study, InteractionState.finish]
                    #    ['error', InteractionState.learnnew, InteractionState.study],
                    #    ['error', InteractionState.review, InteractionState.study]
                       ]
        
        Machine.__init__(self, 
                         states=InteractionState, 
                         initial=InteractionState.start, 
                         transitions=transitions)
    
class Interaction(Cmd):
    intro = "欢迎来到Learning-English-By-Translation.\n请登录(login)/注册(register): "
    prompt = 'Translater >'
    __interactionMachine = InteractionMachine()
    userInfo = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        if self.userInfo:
            self.userInfo.write_dict()
    
    # ----- 基本命令 -----
    def do_login(self, arg):
        "登录: login"
        if self.__interactionMachine.is_start() == True:
            user_id = input('请输入用户名: ')
            user_password = input('请输入密码: ')
            check_bool, check_msg = userIdDb.login(user_id, user_password)
            if check_bool == False:
                print(check_msg)
                return
            else:
                print('登录成功')
                self.userInfo = UserInfo(user_id)
                self.__interactionMachine.login()
                self.__interactionMachine.study()
                self.print_cur_cmd()
        else:
            print('不能登录')
            self.print_cur_cmd()
    
    def do_register(self, arg):
        "注册: register"
        if self.__interactionMachine.is_start() == True:
            user_id = input('请输入用户名: ')
            user_password = input('请输入密码: ')
            check_bool, check_msg = userIdDb.register(user_id, user_password)
            if check_bool == False:
                print(check_msg)
                return
            else:
                print('注册成功')
                self.userInfo = UserInfo(user_id)
                self.__interactionMachine.register()
                self.__interactionMachine.study()
                self.print_cur_cmd()
        else:
            print('不能注册')
            self.print_cur_cmd()
    
    def do_new(self, arg):
        "开始新题目: new"
        if self.__interactionMachine.is_study() == True:
            chinese, english, question_id = self.userInfo.get_new_question()
            
            if chinese is None:
                print('全部学习完毕')
                return
                # self.__interactionMachine.error()
            
            print('-------------------------------')
            print('中文为：'+chinese)
            
            self.__chinese = chinese
            self.__english = english
            self.__question_id = question_id
            
            self.__interactionMachine.learnnew()
            self.print_cur_cmd()
        else:
            print('不能学习新题目')
            self.print_cur_cmd()
    
    def do_review(self, arg):
        "复习旧题目: review"
        if self.__interactionMachine.is_study() == True:
            chinese, english, complexity, question_id = self.userInfo.get_review_question()
            
            if chinese is None:
                print('全部复习完毕')
                return
                # self.__interactionMachine.error()
            
            print('-------------------------------')
            print('中文为：'+chinese)
            
            self.__chinese = chinese
            self.__english = english
            self.__question_id = question_id
            self.__complexity = complexity
            
            self.__interactionMachine.review()
            self.print_cur_cmd()
        else:
            print('不能复习旧题目')
            self.print_cur_cmd()
                
    def do_answer(self, arg):
        "回答题目: answer"
        if self.__interactionMachine.is_learnnew() == True or self.__interactionMachine.is_review() == True:
            answer = input('请输入英文翻译: ')
            print('-------------------------------')
            print('英文为：'+self.__english)
            
            if self.__interactionMachine.is_learnnew() == True:
                complexity = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')
                while complexity not in ['complex', 'medium', 'ease']:
                    complexity = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')
                
                self.userInfo.insert_question(self.__question_id, answer, complexity)
            else:
                move_level = input('您觉得难度应该如何调整(-2~3整数, 数字越大越容易): ')
                while move_level not in ['-2', '-1', '0', '1', '2', '3']:
                    move_level = input('您觉得难度应该如何调整(-2~3整数, 数字越大越容易): ')
            
                self.userInfo.insert_question(self.__question_id, answer, self.__complexity, move_level=int(move_level))
            self.__interactionMachine.answer()
            self.__interactionMachine.study()
            self.print_cur_cmd()
        else:
            print('不能回答问题')
            self.print_cur_cmd()
    
    def do_skip(self, arg):
        "跳过题目: skip"
        if self.__interactionMachine.is_learnnew() == True or self.__interactionMachine.is_review() == True:
            if self.__interactionMachine.is_learnnew() == True:
                self.userInfo.insert_skip(self.__question_id)
            else:
                self.userInfo.insert_skip(self.__question_id, self.__complexity)     
                
            self.__interactionMachine.skip()           
            self.__interactionMachine.study()
            self.print_cur_cmd()
        else:
            print('不能跳过')
            self.print_cur_cmd()
    
    def do_exit(self, arg):
        "退出: exit"
        if self.__interactionMachine.is_study() == True or self.__interactionMachine.is_start() == True:
            print('退出系统')
            return True
        else:
            print('不可退出')
            self.print_cur_cmd()
            
    # ----- 高级处理 -----
    def parse_cmd(self, cmd):
        pass
    
    # def preloop(self):
    #     print('请登录(login)/注册(register): ')
    
    def emptyline(self):
        pass
    
    def default(self, line):
        print('命令错误')
        self.print_cur_cmd()
        
    def print_cur_cmd(self):
        if self.__interactionMachine.is_start():
            print('请登录(login)/注册(register)/退出(exit)')
        elif self.__interactionMachine.is_study():
            print('请选择学习新题目(new)/复习(review)/退出(exit)')
        elif self.__interactionMachine.is_learnnew():
            print('请选择回答(answer)/跳过(skip)')
        elif self.__interactionMachine.is_review():
            print('请选择回答(answer)/跳过(skip)')
        
if __name__ == '__main__':
    with Interaction() as interaction:
        interaction.cmdloop()