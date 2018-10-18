# -*- coding: utf-8 -*-

import string

MAX_NUM = 100
MIN_YEAR = "1990"
MAX_YEAR = "2089"

class PaperRelationScore():
    coid = None
    score = None
    year = None
    # def __eq__(self, other):
    #     return self.score == other.score
    # def __gt__(self, other):
    #     return self.score > other.score
    # def __lt__(self, other):
    #     return self.score < other.score

class PaperRelationYear():
    coid = None
    cork = None
    year = None
    # def __eq__(self, other):
    #     return self.year == other.year
    # def __gt__(self, other):
    #     return self.year > other.year
    # def __lt__(self, other):
    #     return self.year < other.year

# 统计从1990年到2089年的关系得分
def calc_paper_score(record):
    return _test_calc_paper_score(record)

def _test_calc_paper_score(record):

    # 该学者为一作
    is_a1_coid_list = trans_is_ai_coid(record['is_a1_coid'])
    is_a1_cork_list = trans_is_ai_cork(record['is_a1_cork'])
    is_a1_year_list = trans_is_ai_date(record['is_a1_date'])

    print(is_a1_coid_list)
    print(is_a1_cork_list)
    print(is_a1_year_list)

    if len(is_a1_year_list) == len(is_a1_cork_list) and \
        len(is_a1_year_list) == len(is_a1_coid_list):
        pass


    # 该学者为二作
    # 该学者为三作
    # 该学者为四作
    # 该学者为五作
    pass

def trans_is_ai_coid(raw):
    is_ai_coid = raw.lstrip('[').rstrip(']').replace('\'','').split(', ')
    # for tmp in is_ai_coid:
    #     print(tmp)
    return is_ai_coid

def trans_is_ai_cork(raw):
    cur = raw.lstrip('[').rstrip(']').split(', ')
    is_ai_cork = []
    for tmp in cur:
        is_ai_cork.append(int(tmp))
    return is_ai_cork

def trans_is_ai_date(raw):
    is_ai_date = raw.lstrip('[').rstrip(']').replace('\'', '').split(', ')
    is_ai_year = []
    for tmp in is_ai_date:
        is_ai_year.append(extract_year(tmp))
    return is_ai_year

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