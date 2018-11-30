#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:48:50 2018

@author: yangzhuronghuang
"""

import urllib.request
import re
import time
from bs4 import BeautifulSoup
from collections import defaultdict
import networkx as nx


def download(url, num_retries = 2, user_agent = "baiduspider"):
    print ('Downloading:'+url)
    headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
                          'referer': 'http://baidu.com'}
    request = urllib.request.Request(url, headers = headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib2.URLError as e:
        print ('Download error:'+e.reason)
        html = None
        if num_retries >0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                #recursively retry 5XX HTTP errors
                return download(url, num_retries-1)
    time.sleep(1)
    return html

def get_links(html):
    source = download(html)
    soup = BeautifulSoup(source)
    htmls = []
    tab_re = soup.find_all('table')[1]
    pre = 'https://baike.baidu.com'
    for link in tab_re.find_all('a',href = True):
        htmls.append(pre+link['href'])
    return htmls

def get_list_of_stations(html, no_table = 1):
    source = download(html)
    soup = BeautifulSoup(source)
    result = []
    tab_re = soup.find_all('table')[no_table]
    for link in tab_re.find_all('a',href = True):
        if(re.search('站',link.get_text()) != None):
            result.append(link.get_text())
    return result

def draw_stations(html):
    htmls = get_links(html)
    station_lists = []
    for url in htmls:
        station_lists.append(get_list_of_stations(url))
    #modify the station lists
    station_lists[0] = station_lists[0][3:]
    station_lists[1].append(station_lists[1][0])
    station_lists[2] = get_list_of_stations('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%814%E5%8F%B7%E7%BA%BF',2)
    temp_list4 = station_lists[4][3:-6]
    temp_list4.append(station_lists[4][-5])
    station_lists[4] = temp_list4+station_lists[4][-3:]
    station_lists[5] = station_lists[5][:-4]+station_lists[5][-3:-2]
    station_lists[6] = get_list_of_stations('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%818%E5%8F%B7%E7%BA%BF',2)
    station_lists[6] = station_lists[6][:18]
    station_lists[7] = station_lists[7][:2]+station_lists[7][3:8]+station_lists[7][9:13]+station_lists[7][14:]
    del station_lists[7][8]
    station_lists[9] = station_lists[9][:4]+station_lists[9][5:11]+station_lists[9][12:]
    del station_lists[9][5]
    station_lists[10] = get_list_of_stations('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%8114%E5%8F%B7%E7%BA%BF',2)
    station_lists[11] = station_lists[10][7:]
    station_lists[10] = station_lists[10][:6]
    station_lists[10] = ['张郭庄站']+station_lists[10]
    station_lists[11] = [station_lists[11][0]]+station_lists[11][2:8]+station_lists[11][9:16]+station_lists[11][17:]
    station_lists[-5] = station_lists[-5][-10:]
    station_lists[-4] = station_lists[-4][:-1]
    station_lists[-3] = station_lists[-3][:10]+station_lists[-3][11:]
    station_lists[-2] = station_lists[-2][1:]
    station_lists[-1] = station_lists[-1][1:-2]
    return station_lists

list1 = draw_stations('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485')
d = defaultdict(list)

for list2 in list1:
    for s in range(len(list2)):
        if(s == 0):
            d[list2[s]].append(list2[s+1])
        elif (s == len(list2)-1):
            d[list2[s]].append(list2[s-1])
        else:
            d[list2[s]].append(list2[s-1])
            d[list2[s]].append(list2[s+1])
            
sgraph = nx.Graph(d)
nx.draw(sgraph, with_labels = True, node_size = 2)
            
def get_successors(frontier, graph):
    return graph[frontier]
             
def sort_paths(paths, func, beam):
    return sorted(paths, key =func)[:beam]
def min_distance_station(paths):
    return sort_paths(paths, lambda p:(len(p)), beam = 10)


def search_destination(graph, start, get_succsssors, goal, strategy_func):
    paths = [[start]]
    seen = set()
    chosen_paths = []
    while paths:
        path = paths.pop(0)
        frontier = path[-1]
        if frontier in seen: continue
            
        for city in get_succsssors(frontier, graph):
            if city in path: continue # remove the loop
            new_path = path + [city]
            paths.append(new_path)
            if city == goal: return new_path
        
        paths = strategy_func(paths)
        seen.add(frontier)
    return chosen_paths



    