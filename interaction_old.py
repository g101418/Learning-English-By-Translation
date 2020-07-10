'''
@Author: Gao S
@Date: 2020-07-06 20:28:43
@LastEditTime: 2020-07-10 22:39:42
@Description: 
@FilePath: /English-Translation/interaction_.py
'''

from user_info import UserInfo
from database import userIdDb

from user_info import complexities

if __name__ == '__main__':
    # 用户登录
    cmd = input('请登录(login)/注册(register): ')
    while cmd not in ['login', 'register']:
        cmd = input('请登录(login)/注册(register): ')
    
    if cmd == 'login':
        text = input('请输入用户名和密码，以空格分隔: ')
        user_id, user_password = text.split(' ')[:2]
        # TODO 异常处理
        check_bool, check_msg = userIdDb.login(user_id, user_password)
        while check_bool == False:
            print(check_msg)
            text = input('请输入用户名和密码，以空格分隔: ')
            user_id, user_password = text.split(' ')[:2]
            check_bool, check_msg = userIdDb.login(user_id, user_password)
        print(check_msg)
        
    elif cmd == 'register':
        text = input('请输入用户名和密码，以空格分隔: ')
        user_id, user_password = text.split(' ')[:2]
        # TODO 异常处理
        check_bool, check_msg = userIdDb.register(user_id, user_password)
        while check_bool == False:
            print(check_msg)
            text = input('请输入用户名和密码，以空格分隔: ')
            user_id, user_password = text.split(' ')[:2]
            check_bool, check_msg = userIdDb.register(user_id, user_password)
        print(check_msg)
        
    # userInfo = UserInfo(user_id)
    
    with UserInfo(user_id) as userInfo:
        
        while True:
            cmd = input('请选择要做新的题目(new)/复习(review): ')
            if cmd == 'exit':
                break
            while cmd not in ['new', 'review']:
                cmd = input('请选择要做新的题目(new)/复习(review): ')
            
            if cmd == 'new':
                chinese, english, question_id = userInfo.get_new_question()
                
                if chinese is None:
                    print('全部学习完毕')
                    continue
                
                print('中文为：'+chinese)
                answer = input('请输入英文翻译: ')
                print('英文为：'+english)
                
                complexity = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')
                while complexity not in ['complex', 'medium', 'ease']:
                    complexity = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')
                    
                userInfo.insert_question(question_id, answer, complexity)
            elif cmd == 'review':
                chinese, english, complexity, question_id = userInfo.get_review_question()
                
                if chinese is None:
                    print('全部复习完毕')
                    continue
                
                print('中文为：'+chinese)
                answer = input('请输入英文翻译: ')
                print('英文为：'+english)
                
                complexity_new = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')
                while complexity_new not in ['complex', 'medium', 'ease']:
                    complexity_new = input('您觉得难度是复杂(complex)/中等(medium)/简单(ease): ')

                now_index = complexities.index(complexity)
                if complexity_new == 'complex':
                    complexity_new = complexity
                elif complexity_new == 'medium':
                    now_index += 1
                    now_index = min(5, now_index)
                    complexity_new = complexities[now_index]
                elif complexity_new == 'ease':
                    now_index += 2
                    now_index = min(5, now_index)
                    complexity_new = complexities[now_index]
                
                # print(complexity_new)
                
            
                userInfo.insert_question(question_id, answer, complexity_new)
            
    
    
    # gaoshijie 123456