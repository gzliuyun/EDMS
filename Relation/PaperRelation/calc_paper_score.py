# -*- coding: utf-8 -*-

import string

MAX_NUM = 100
MIN_YEAR = "1990"
MAX_YEAR = "2089"

# 一作加分系数
IS_A1_SCORE = [0, 80, 20, 20, 20]
# 二作加分系数
IS_A2_SCORE = [100, 0, 20, 20, 20]
# 三作加分系数
IS_A3_SCORE = [100, 80, 0, 20, 20]
# 四作加分系数
IS_A4_SCORE = [100, 80, 20, 0, 20]
# 五作加分系数
IS_A5_SCORE = [100, 80, 20, 20, 0]

class PaperRelationScore():
    coid = None
    score = None
    year = None

    def __init__(self, _c, _y, _s):
        self.coid = _c
        self.year = _y
        self.score = _s

    def __eq__(self, other):
        if isinstance(other, PaperRelationScore):
            return ((self.coid == other.coid) and (self.year == other.year))
        else:
            return False

    def __hash__(self):
        return hash(str(self.coid) + " " + str(self.year))


class PaperRelationYear():
    coid = None
    cork = None
    year = None
    # def __str__(self):
    #     str1 = "coid: " + self.coid
    #     str2 = "cork: " + str(self.cork)
    #     str3 = "year " + self.year
    #     return str1+" "+str2+" "+str3


# 统计从1990年到2089年的关系得分
def calc_paper_score(record):
    return _test_calc_paper_score(record)


# PRS测试用计分函数
def _test_calc_paper_score(record):
    pry1_list = get_pry_list(record['is_a1_coid'], record['is_a1_cork'], record['is_a1_date'])
    pry2_list = get_pry_list(record['is_a2_coid'], record['is_a2_cork'], record['is_a2_date'])
    pry3_list = get_pry_list(record['is_a3_coid'], record['is_a3_cork'], record['is_a3_date'])
    pry4_list = get_pry_list(record['is_a4_coid'], record['is_a4_cork'], record['is_a4_date'])
    pry5_list = get_pry_list(record['is_a5_coid'], record['is_a5_cork'], record['is_a5_date'])

    # 该学者为一作
    # print("*******************该学者为一作*******************")
    prs1set = set()
    if pry1_list != None:
        for pry1 in pry1_list:
            tmp = PaperRelationScore(pry1.coid, pry1.year, IS_A1_SCORE[pry1.cork-1])
            if tmp in prs1set:
                tmp.score = updatescore(tmp, prs1set)
                prs1set.remove(tmp)
            prs1set.add(tmp)

        # for prs1 in prs1set:
        #     print(prs1.coid)
        #     print(prs1.year)
        #     print(prs1.score)

    # 该学者为二作
    # print("*******************该学者为二作*******************")
    prs2set = set()
    if pry2_list != None:
        for pry2 in pry2_list:
            tmp = PaperRelationScore(pry2.coid, pry2.year, IS_A2_SCORE[pry2.cork-1])
            if tmp in prs2set:
                tmp.score = updatescore(tmp, prs2set)
                prs2set.remove(tmp)
            prs2set.add(tmp)

        # for prs2 in prs2set:
        #     print(prs2.coid)
        #     print(prs2.year)
        #     print(prs2.score)

    # 该学者为三作
    # print("*******************该学者为三作*******************")
    prs3set = set()
    if pry3_list != None:
        for pry3 in pry3_list:
            tmp = PaperRelationScore(pry3.coid, pry3.year, IS_A3_SCORE[pry3.cork-1])
            if tmp in prs3set:
                tmp.score = updatescore(tmp, prs3set)
                prs3set.remove(tmp)
            prs3set.add(tmp)

        # for prs3 in prs3set:
        #     print(prs3.coid)
        #     print(prs3.year)
        #     print(prs3.score)

    # 该学者为四作
    # print("*******************该学者为四作*******************")
    prs4set = set()
    if pry4_list != None:
        for pry4 in pry4_list:
            tmp = PaperRelationScore(pry4.coid, pry4.year, IS_A4_SCORE[pry4.cork-1])
            if tmp in prs4set:
                tmp.score = updatescore(tmp, prs4set)
                prs4set.remove(tmp)
            prs4set.add(tmp)

        # for prs4 in prs4set:
        #     print(prs4.coid)
        #     print(prs4.year)
        #     print(prs4.score)

    # 该学者为五作
    # print("*******************该学者为五作*******************")
    prs5set = set()
    if pry5_list != None:
        for pry5 in pry5_list:
            tmp = PaperRelationScore(pry5.coid, pry5.year, IS_A5_SCORE[pry5.cork-1])
            if tmp in prs5set:
                tmp.score = updatescore(tmp, prs5set)
                prs5set.remove(tmp)
            prs5set.add(tmp)

        # for prs5 in prs5set:
        #     print(prs5.coid)
        #     print(prs5.year)
        #     print(prs5.score)

    prsset = set()
    for prs1 in prs1set:
        tmp = prs1
        if tmp in prsset:
            tmp.score = updatescore(tmp, prsset)
            prsset.remove(tmp)
        prsset.add(tmp)
    for prs2 in prs2set:
        tmp = prs2
        if tmp in prsset:
            tmp.score = updatescore(tmp, prsset)
            prsset.remove(tmp)
        prsset.add(tmp)
    for prs3 in prs3set:
        tmp = prs3
        if tmp in prsset:
            tmp.score = updatescore(tmp, prsset)
            prsset.remove(tmp)
        prsset.add(tmp)
    for prs4 in prs4set:
        tmp = prs4
        if tmp in prsset:
            tmp.score = updatescore(tmp, prsset)
            prsset.remove(tmp)
        prsset.add(tmp)
    for prs5 in prs5set:
        tmp = prs5
        if tmp in prsset:
            tmp.score = updatescore(tmp, prsset)
            prsset.remove(tmp)
        prsset.add(tmp)

    for prs in prsset:
        print(prs.coid, prs.year, prs.score)
    return prsset

# PRS测试用合并分数函数
def updatescore(tmp, prsset):
    for prs in prsset:
        if tmp.coid == prs.coid and tmp.year == prs.year:
            return tmp.score + prs.score
    return 0


# 将三组字符串形式的id-rk-date数组转化为PaperRelationYear格式的三元组
def get_pry_list(is_ai_coid, is_ai_cork, is_ai_date):
    # 为空
    if len(is_ai_coid) == 2:
        return None

    is_ai_coid_list = trans_is_ai_coid(is_ai_coid)
    is_ai_cork_list = trans_is_ai_cork(is_ai_cork)
    is_ai_year_list = trans_is_ai_date(is_ai_date)

    # print(is_ai_coid_list)
    # print(is_ai_cork_list)
    # print(is_ai_year_list)

    pryi_list = []
    if len(is_ai_year_list) == len(is_ai_cork_list) and \
                    len(is_ai_year_list) == len(is_ai_coid_list):
        leni = len(is_ai_year_list)
        for i in range(leni):
            tmp = PaperRelationYear()
            tmp.coid = is_ai_coid_list[i]
            tmp.cork = is_ai_cork_list[i]
            tmp.year = is_ai_year_list[i]
            pryi_list.append(tmp)
        # print(pryi_list)
        return pryi_list
    else:
        None


# 将string格式的coid列表处理为list格式
def trans_is_ai_coid(raw):
    is_ai_coid = raw.lstrip('[').rstrip(']').replace('\'', '').split(', ')
    # for tmp in is_ai_coid:
    #     print(tmp)
    return is_ai_coid


# 将string格式的cork列表处理为list格式
def trans_is_ai_cork(raw):
    cur = raw.lstrip('[').rstrip(']').split(', ')
    is_ai_cork = []
    for tmp in cur:
        is_ai_cork.append(int(tmp))
    return is_ai_cork


# 将string格式的date列表处理为list格式
def trans_is_ai_date(raw):
    is_ai_date = raw.lstrip('[').rstrip(']').replace('\'', '').split(', ')
    is_ai_year = []
    for tmp in is_ai_date:
        is_ai_year.append(extract_year(tmp))
    return is_ai_year

# 提取date中的年份
def extract_year(date):
    if len(date) >= 4:
        ret = date[0:4]
        if ret >= MIN_YEAR and ret <= MAX_YEAR:
            return ret
        else:
            return 'Null'
    else:
        return 'Null'


if __name__ == "__main__":
    record = {
        'id': '100000000000014',
        'is_a1_coid': "['100000008129206', '100000008129206', '100000008129206']",
        'is_a1_cork': '[2, 2, 2]',
        'is_a1_date': "['2005', '2005', '2006']",
        'is_a2_coid': "['100000008129206', '100000008368013']",
        'is_a2_cork': '[1, 1]',
        'is_a2_date': "['2004', '2006']",
        'is_a3_coid': "['100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132', '100000011581132']",
        'is_a3_cork': '[1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]',
        'is_a3_date': "['2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2005', '2006']",
        'is_a4_coid': '[]',
        'is_a4_cork': '[]',
        'is_a4_date': '[]',
        'is_a5_coid': '[]',
        'is_a5_cork': '[]',
        'is_a5_date': '[]'
    }

    calc_paper_score(record)