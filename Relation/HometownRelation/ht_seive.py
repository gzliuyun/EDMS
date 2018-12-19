# -*- coding: utf-8 -*-

import jieba
import logging
import jieba.posseg as psg

jieba.setLogLevel(logging.INFO)
jieba.load_userdict('integrated_ht_dict.txt')

from ht_dict import ht_dict
from  ht_dict import  MAX_HT_NUM
from ht_list import ht_list

def do_cal_similarity(str1, str2):

    # print(str1, str2)

    len1 = len(str1)
    len2 = len(str2)
    if (len1 == 0 or len2 == 0):
        return 0
    # print(str1, str2)

    ans = [([0] * (len2 + 1)) for i in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                ans[i][j] = ans[i - 1][j - 1] + 1
            else:
                ans[i][j] = max(ans[i][j - 1], ans[i - 1][j])
    lcs = ans[len1][len2]

    return (lcs / min(len1, len2))* 10 + lcs/len1 + lcs/len2

def illegibility_match(row):
    ret = ''
    maxs = 0.0
    maxid = -1

    for i in range(MAX_HT_NUM):
        tmps = do_cal_similarity(row, ht_list[i])
        if (tmps > maxs):
            maxs = tmps
            maxid = i

    if (maxid >= 0):
        # return ht_list[maxid]
        return maxid
    else:
        return -1

# 模式1：山东高唐人
def ht_seive1(row):
    tmp = list(psg.cut(row))
    tlen = len(tmp)
    for i in range(tlen):
        if (tmp[i].flag == "ns" and i < tlen-1 and tmp[i+1].word == "人"):
            matchid = illegibility_match(tmp[i].word)
            if (matchid >= 0):
                tmpht = ht_list[matchid]
                tmpht_id = ht_dict[tmpht]
                print(tmpht, tmpht_id)

def ht_seive(row):
    ht_seive1(row)

if __name__ == "__main__":
    test1 = "男，1974年4月生，山东高唐人，中共党员，讲师。" \
           "个人简历：1992·9－1996·7 山东大学哲学系本科生" \
           "1996·9－1999·7 山东大学哲学系马克思主义哲学专业硕士生1999·7－2002·8 " \
           "山东聊城大学政法学院哲学教研室教师2002·9－2006·7 北京大学哲学系外国哲学专业博士生 " \
           "2006年8月到人民大学马克思主义学院任教，2006年9月被评为讲师。 " \
           "主要教授课程： 马克思主义基本原理概论、思想道德修养与法律基础、哲学专业外语、西方哲学基本问题研究。 " \
           "研究方向： 国外马克思主义、比较哲学 科研项目： 人民大学2006年度科研基金项目：“国外马克思主义对现代性的态度”。" \
           "主要科研成果（2006年以来）：“中国古代哲理思想的诗化表达”，《烟台大学学报》2007年第1期 " \
           "联系方式：E-mail: zhangxiaohua1974@sina.com"

    ht_seive(test1)