# -*- coding: utf-8 -*-

import re
from school_list import school_list

MAX_NUM = 2233

noise = [
    '大学',
    '专科学校',
    '学院',
    '高等',
    '重点',
    '实验室',
    '国家',
    '院',
    '系',
    '校区',
    '中心',
    '省',
    '市',
    '区',
    '级',
    '研究所',
    '与',
    '[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。？、~@#￥%……&*（）]+'
]


def do_cal_similarity(str1, str2):

    # print(str1, str2)

    news1 = do_remove_noise(str1)
    news2 = do_remove_noise(str2)

    len1 = len(news1)
    len2 = len(news2)
    if (len1 == 0 or len2 == 0):
        return 0
    # print(news1, news2)

    ans = [([0] * (len2 + 1)) for i in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if news1[i - 1] == news2[j - 1]:
                ans[i][j] = ans[i - 1][j - 1] + 1
            else:
                ans[i][j] = max(ans[i][j - 1], ans[i - 1][j])
    lcs = ans[len1][len2]

    return lcs / min(len1, len2)


def do_remove_noise(str):
    ret = str
    for n in noise:
        ret = re.sub(n, "", ret)
    return ret

def get_school_name(row):
    ret = ''
    maxs = 0.0
    maxid = -1

    for i in range(MAX_NUM):
        tmps = do_cal_similarity(row, school_list[i])
        if (tmps > maxs):
            maxs = tmps
            maxid = i

    if (maxid >= 0):
        # return school_list[maxid]
        return maxid
    else:
        return -1

if __name__ == "__main__":

    test = "月毕业于华北水利水电学院"

    tmp = get_school_name(test)

    print(tmp)