# -*- coding: utf-8 -*-

# 获取总和学术关系分数超过500的最高核心专家
# 若无满足对象，返回自己
PAPER_RELATION_SCORE_THRESHOLD = 500
def getCore(record, cursor):
    print(record)
    ex_id = record['id']
    coid_list = record['coid_list'].lstrip("['").rstrip("']").split("', '")
    year_list = record['year_list'].lstrip("['").rstrip("']").split("', '")
    score_list = record['score_list'].lstrip("['").rstrip("']").split(", ")
    c_len = len(coid_list)
    y_len = len(year_list)
    s_len = len(score_list)

    # print(coid_list)
    # # print(year_list)
    # print(score_list)

    if coid_list[0] == '' or c_len != y_len or c_len != s_len:
        return ex_id

    tot_len = c_len

    coid_set = set()
    for coid in coid_list:
        coid_set.add(coid)

    c_set_len = 0
    coid_dict = dict()
    for coid in coid_set:
        c_set_len += 1
        coid_dict[coid] = c_set_len

    tot_score_list = [0 for i in range(c_set_len)]
    for i in range(tot_len):
        id = coid_dict[coid_list[i]]
        # print(score_list[i])
        tot_score_list[id-1] += int(score_list[i])

    maxs = 0
    maxs_id = -1
    for i in range(c_set_len):
        if tot_score_list[i] >= maxs:
            maxs = tot_score_list[i]
            maxs_id = i

    if maxs < PAPER_RELATION_SCORE_THRESHOLD:
        return ex_id

    for i,j in coid_dict.items():
        if j == maxs_id:
            sql = 'SELECT * FROM paper_relation_score WHERE id = ' + maxs_id
            print(sql)
            next_record = cursor.execute(sql)
            print("********")
            print(next_record)
            print("--------")
            # return getCore(next_record, cursor)

    return ex_id

if __name__ == "__main__":
    pass