# Learning-English-By-Translation
通过将中文翻译成英文并加以复习来学习英语

## 使用

### 初始化

```shell
python3 setup_db.py
```

在 setup_db.py 文件中，根据需要调用insert_corpus_many()函数，将语料写入数据库中，格式可参考代码。

> 中英平行语料库可见：https://github.com/brightmart/nlp_chinese_corpus

### 使用

```shell
python3 interaction.py
```

随后根据提醒操作



![运行截图](https://github.com/g101418/Learning-English-By-Translation/blob/master/images/screenshot.png)

## 结构

![user_info结构图](https://github.com/g101418/Learning-English-By-Translation/blob/master/images/user_info_json.png)

用户信息的json文件格式，复习时从最高难度的题目开始，直到复习完毕




![状态转换图](https://github.com/g101418/Learning-English-By-Translation/blob/master/images/state_transition_diagram.png)

在交互式命令行中，有限状态机的设计

## TODO

1. ~~将语料写入数据库~~
2. ~~实现项目数据文件初始化~~
3. 实现复习时暂时跳过
4. Electron实现应用程序
5. 实现网站
6. 。。。