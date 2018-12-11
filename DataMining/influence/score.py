#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 16:35
# @Author  : zyk


def cal_score(include,citation):
    score1 = 1
    if include != '' and include != '普通刊':
        score1 = 2
    inclu_list = include.split('、')
    for i in inclu_list:
        if i == 'BDHX':
            score1 = 3
    for i in inclu_list:
        if i in ['CSSCI','CSCD']:
            score1 = 4
    for i in inclu_list:
        if i in ['EI','SCI']:
            score1 = 5
    score2 = 0
    cita = int(citation)
    if cita >0:
        score2 = 1
    if cita >= 5:
        score2 = 2
    if cita >= 30 :
        score2 = 3
    if cita >= 80:
        score2 = 4
    if cita >= 200:
        score2 = 5
    return score1+score2