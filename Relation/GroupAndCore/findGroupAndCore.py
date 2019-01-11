# -*- coding: utf-8 -*-

def getCore(record):
    id = record['id']
    coid_list = record['coid_list'].lsrip('[').rstrip(']')
    year_list = record['year_list'].lsrip('[').rstrip(']')
    score_list = record['score_list'].lsrip('[').rstrip(']')

    print(id)
    print(coid_list)


if __name__ == "__main__":
    test = "{'id': '100000000000014', 'coid_list': "['100000008129206', '100000011581132', '100000008129206', '100000008368013', '100000011581132', '100000008129206']", 'year_list': "['2004', '2005', '2005', '2006', '2006', '2006']", 'score_list': '[100, 1380, 160, 100, 100, 80]'}"
    getCore(test)