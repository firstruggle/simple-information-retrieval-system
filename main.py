import functools

import numpy
import os
import jieba


path = './doc/'

# 创建停用词列表
def StopWordsList():
    stopwords = [line.strip() for line in open('chinsesstoptxt.txt', encoding='UTF-8').readlines()]
    return stopwords


# 对句子进行中文分词
# 输入一个字串，输出以空格分隔的字串
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词

    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = StopWordsList()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    print("分词成功")
    return outstr


IdxTxt = []  # get txt through idx


# 通过文档文件夹读取文档生成文档字典
def construct_doc(path):
    docu_set = dict()
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    i = 1
    for file in files:  # 遍历文件夹
        if not file.endswith(".txt"):
            continue
        position = path + file  # 构造绝对路径，"\\"，其中一个'\'为转义符
        print(position)
        with open(position, "r", encoding='utf-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            ret = seg_depart(data)
            # print(ret)
            docu_set[i] = ret
            IdxTxt.append(file)
            i += 1

    return docu_set  # key:int value:string


Matrix = []
for i in range(30000):  # 30000words * 200docs
    Matrix.append([0] * 200)

StrIdx = dict()  # dict: through str get idx

W2 = [0] * 200  # IntArray, each doc's w^2 to calculate cos


# 通过文档字典生成倒排索引
def reverse_idx(docu_set):
    all_words = []
    for i in docu_set.values():
        cut = i.split()  # 返回列表,每个单词字串
        all_words.extend(cut)

    set_all_words = set(all_words)  # 去重
    # 预处理每个单词对应的序号方便之后查找
    size = 1
    for x in set_all_words:
        StrIdx[x] = size
        size += 1

    for i in docu_set.keys():  # 处理出某词在某文档中出现过几次，这个二维数组
        strs = docu_set[i].split()
        for str in strs:
            idx = StrIdx[str]
            Matrix[idx][i] += 1
        strs = set(strs)
        for str in strs:
            idx = StrIdx[str]
            v = Matrix[idx][i]
            W2[i] += v * v

    # invert_index = dict()  # 倒排索引
    # for b in set_all_words:  # 对出现的每个单词，分别计算
    #     temp = dict()
    #     for j in docu_set.keys():  # 针对每一个文档分别计算
    #         count = 0
    #         field = docu_set[j]
    #         split_field = field.split()  # 这个文档的所有单词的列表。
    #
    #         for k in split_field:
    #             if k == b:
    #                 if count == 0:
    #                     temp[j] = 1
    #                     count += 1
    #                 else:
    #                     temp[j] += 1
    #
    #     invert_index[b] = temp

def to_do():
    InputStr = input()
    InputStr = seg_depart(InputStr).split()
    print(InputStr)

    # calc cos
    W = []
    for i in range(200):
        W.append({"id": i, "score": 0})
    Pvalue = 0
    for str in InputStr:
        if str in StrIdx:
            Pvalue += 1
            idx = StrIdx[str]
            for j in range(200):
                W[j]['score'] += Matrix[idx][j]

    if Pvalue == 0:
        print("无相关内容")
        exit(0)
    for i in range(200):
        if W2[i] != 0:
            W[i]['score'] = W[i]['score'] / ((W2[i] * Pvalue) ** 0.5)
        else:
            W[i]['score'] = 0

    print(W)

    def cmp(w1, w2):
        return w2['score'] - w1['score']

    W.sort(key=functools.cmp_to_key(cmp))
    print(W)
    filename = IdxTxt[W[0]['id'] - 1]
    with open(path + filename, "r") as fp:
        url = fp.readline()
        title = fp.readline()
        print(url)
        print(title)


if __name__ == "__main__":
    docu_set = construct_doc(path)
    reverse_idx(docu_set)
    for z in range(10):
        to_do()
