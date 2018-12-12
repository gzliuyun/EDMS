# -*- coding: utf-8 -*-

from school_list import school_list
from school_list import MAX_NUM

schoolmate = [set()*MAX_NUM]

def get_relation():

    pass

def test():
    schoolmate[0].add(0)
    schoolmate[23].add(12)
    schoolmate[23].add(13)

    for i in range(30):
        print(schoolmate[i])


if __name__ == "__main__":
    test()
    pass