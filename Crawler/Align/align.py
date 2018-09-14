# -*- coding: utf-8 -*-
import re

noise = [
    '学院',
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
    '[\s+\.\!\/_,$%^*()+\"\']+|[+——！，。？、~@#￥%……&*（）]+'
]

def do_cal_similarity(str1, str2):
    news1 = do_remove_noise(str1)
    news2 = do_remove_noise(str2)

    len1 = len(news1)
    len2 = len(news2)

    print(news1, news2)

    ans = [([0] * (len2+1)) for i in range(len1+1)]
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            if news1[i-1] == news2[j-1]:
                ans[i][j] = ans[i-1][j-1]+1
            else:
                ans[i][j] = max(ans[i][j-1], ans[i-1][j])
    lcs = ans[len1][len2]
    return lcs / min(len1, len2)

def do_remove_noise(str):
    ret = str
    for n in noise:
        ret = re.sub(n, "", ret)
    return ret


if __name__ == "__main__":

    str1 = "中山医学院眼科学国家重点实验室"
    str2 = "中山眼科中心"

    str3 = "电子科学与技术学院深圳市激光工程重点实验室"
    str4 = "电子科学与技术学院"

    str5 = "（南校区）电信学院"
    str6 = "电信学院"

    str7 = "材料科学与工程学院化工资源有效利用国家重点实验室"
    str8 = "材料科学与工程学院"

    res = do_cal_similarity(str7, str8)
    print(res)