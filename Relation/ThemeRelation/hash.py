# -*- coding: utf-8 -*-

HASH_MOD = 5170427
HASH_NUM = 131

def hash_theme_id(theme, id):
    tmp = theme+id
    ret = 0
    for ch in tmp:
        ret = (ret * HASH_NUM + ord(ch)) % HASH_MOD
    return str(ret)

if __name__ == "__main__":
    t1 = hash_theme_id("区域经济", "100000000000014")
    t2 = hash_theme_id("数值模拟", "100000000000027")
    t3 = hash_theme_id("数值模拟", "100000000000027")
    print(t1, t2, t3)