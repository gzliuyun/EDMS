# 考虑专家作为第I作者时，合并同年同合作学者的prs
# -*- coding: utf-8 -*-

import string

MAX_NUM = 100
MIN_YEAR = "1990"
MAX_YEAR = "2089"

# 一作加分系数
IS_A1_SCORE = [0, 80, 30, 20, 20]
# 二作加分系数
IS_A2_SCORE = [100, 0, 30, 20, 20]
# 三作加分系数
IS_A3_SCORE = [100, 80, 0, 20, 20]
# 四作加分系数
IS_A4_SCORE = [100, 80, 30, 0, 20]
# 五作加分系数
IS_A5_SCORE = [100, 80, 30, 20, 0]

class PaperRelationScore():
    year = None
    score = None
    coid = None


    def __init__(self, _c, _y, _s):
        self.coid = _c
        self.year = _y
        self.score = _s

    def __eq__(self, other):
        return self.coid == other.coid and \
               self.year == other.year and \
               self.score == other.score

    def __lt__(self, other):
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        if self.year == other.year:
            if self.score > other.score:
                return True
            if self.score < other.score:
                return False
            if self.score == other.score:
                return self.coid < other.coid

# 同一人同一年合并分数，以此为标记
class PaperRelationTag():
    coid = None
    year = None

    def __init__(self, _c, _y):
        self.coid = _c
        self.year = _y

    def __eq__(self, other):
        if isinstance(other, PaperRelationTag):
            return ((self.coid == other.coid) and (self.year == other.year))
        else:
            return False

    def __hash__(self):
        return hash(str(self.coid)+" "+str(self.year))


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

    # print("############一作############")
    prs1_list = get_prsi_list(pry1_list, IS_A1_SCORE)
    # print("############二作############")
    prs2_list = get_prsi_list(pry2_list, IS_A2_SCORE)
    # print("############三作############")
    prs3_list = get_prsi_list(pry3_list, IS_A3_SCORE)
    # print("############四作############")
    prs4_list = get_prsi_list(pry4_list, IS_A4_SCORE)
    # print("############五作############")
    prs5_list = get_prsi_list(pry5_list, IS_A5_SCORE)

    # 合并所有prsi_list
    prs_list = []
    merge_prsi_list(prs_list, prs1_list)
    merge_prsi_list(prs_list, prs2_list)
    merge_prsi_list(prs_list, prs3_list)
    merge_prsi_list(prs_list, prs4_list)
    merge_prsi_list(prs_list, prs5_list)

    # print(len(prs_list))
    prs_list.sort()
    # for prs in prs_list:
    #     print(prs.coid, prs.year, prs.score)
    return prs_list

def get_prsi_list(pryi_list, IS_Ai_SCORE):
    if pryi_list == None:
        return []

    prtiset = set()
    for pryi in pryi_list:
        tmp = PaperRelationTag(pryi.coid, pryi.year)
        if tmp in prtiset:
            prtiset.remove(tmp)
        prtiset.add(tmp)
    prsi_list = []
    for prti in prtiset:
        tmp = PaperRelationScore(prti.coid, prti.year, 0)
        prsi_list.append(tmp)

    leni = len(prsi_list)
    for pryi in pryi_list:
        cur_coid = pryi.coid
        cur_year = pryi.year
        cur_cork = pryi.cork
        for p in range(leni):
            if cur_coid == prsi_list[p].coid and \
                            cur_year == prsi_list[p].year:
                prsi_list[p].score += IS_Ai_SCORE[cur_cork - 1]
                break

    # for prsi in prsi_list:
    #     print(prsi.coid)
    #     print(prsi.year)
    #     print(prsi.score)

    return prsi_list


def merge_prsi_list(prs_list, prsi_list):
    prs_len = len(prs_list)
    for prsi in prsi_list:
        cur_coid = prsi.coid
        cur_year = prsi.year
        cur_score = prsi.score
        tag = -1
        for p in range(prs_len):
            if cur_coid == prs_list[p].coid and \
                            cur_year == prs_list[p].year:
                prs_list[p].score += cur_score
                tag = 1
                break
        if tag == -1:
            prs_list.append(prsi)

    pass

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
            # print("coid "+str(tmp.coid))
            # print("cork "+str(tmp.cork))
            # print("year "+str(tmp.year))
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