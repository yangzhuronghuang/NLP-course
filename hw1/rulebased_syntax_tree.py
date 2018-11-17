#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 04:17:58 2018

@author: yangzhuronghuang
"""
import random

grammar = """
sentence = adj noun verb adj noun2
adj = adj_single 和 adj_single 的 | null
adj_single = 漂亮|蓝色|好看
adv = 安静地|静静地
noun = 猫|女人|男人
verb = adv 看着 | adv 坐着
noun2 = 桌子|皮球
"""

def build_grammar(grammar_str, split='='):
    grammar_pattern = {}
    for line in grammar_str.split('\n'):
        if not line: continue
        stmt, expr = line.split(split)
        grammar_pattern[stmt.strip()] = [e.split() for e in expr.split('|')]
    return grammar_pattern

def generate(grammar_pattern, target):
    if target not in grammar_pattern: return target
    expr = random.choice(grammar_pattern[target])
    tokens=[generate(grammar_pattern, e) for e in expr]
    return ''.join([t for t in tokens if t!= 'null'])



