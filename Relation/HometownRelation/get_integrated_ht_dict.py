# -*- coding: utf-8 -*-

from ht_dict import ht_dict
from  ht_dict import  MAX_HT_NUM
from ht_list import ht_list

from ht_suf import ht_suf

import re

def remove_suffix(row):
    ret = row

    for suf in ht_suf:
        ret = re.sub(suf, "", ret)

    if (len(ret) == 1):
        ret = row[:2]
    return ret

if __name__ == "__main__":

    with open("integrated_ht_dict.txt", "w") as f:
        for ht in ht_list:
            tmp = remove_suffix(ht)
            str1 = ht + " 25 ns\n"
            f.write(str1)
            if (tmp != ht and len(tmp) >= 2):
                str2 = tmp + " 25 ns\n"
                f.write(str2)
    f.close()
