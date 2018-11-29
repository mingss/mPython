#!/usr/bin/env python
# -*- coding: utf-8 -*-


import webbrowser
import urllib
import requests
from bs4 import BeautifulSoup as bs
#import argparse
import openpyxl
import openpyxl as op
import datetime

def get_content(file_name):
    #print(file_parse(file_name,'\n\n'))
    urls = []
    titles = []
    for content in file_parse(file_name,'\n\n'):
        #print(content)
        #print(content.split('\n')[1])
        urls.append(content.split('\n')[1])
        titles.append(content.split('\n')[0])

    print(titles,urls)

    return urls,titles

def naver_search_url(search_input, period, start_index=1, sort=0):
    print(search_input)
    base_url = 'https://search.naver.com/search.naver?'

    # &sm=tab_opt
    # &sort=0 0 : 관련도순, 1:최신순 2~: 오래된순
    # &photo=0 유형 - 0 : 전체 , 1: 포토, 2: 동영상, 3: 지면기사, 4: 보도자
    # &field=0 0: 전체, 1:제목
    # &reporter_article=
    # &start=0, 11, 21 ...
    # &pd=6 1 : 1주, 2: 1개월 3: ds,de 기간설정(값없을 경우 디폴트 : 1990-1-1~현재,
    #       4: 1일 5: 1 6: 6개월 7~12: 1~6 시
    param ={
        'where': 'news',
        'query': search_input,
        'sm': 'tab_opt',
        'sort': sort,
        'photo': '0',
        'field': '0',
        'reporter_article': '',
        'pd': period,
        'ds': '',
        'de': '',
        'docid': '',
        'nso': '',
        'mynews': '0',
        'mson': '0',
        'start': start_index,
        'refresh_start': '0',
        'related': '0',
    }
    print(base_url + urllib.parse.urlencode(param))
    url = base_url + urllib.parse.urlencode(param)

    return url

def naver_search_urls(search_inputs, period, start_index=0, sort=0):
    urls = []
    for search_input in search_inputs:
        urls.append(naver_search_url(search_input, period, start_index, sort))
    return urls

def url_call_by_requests_api(url):
    request_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
    }
    resp = requests.get(url=url, headers = request_header)#, params=params)
    rescode = resp.status_code
    print (rescode)
    if (rescode == 200):
        response_body = resp.text
        soup = bs(response_body, "lxml")


        for elements in soup.select('.news .title_desc'):
            print (elements.find('span'))

        #print(soup.find_all({'class': 'title_desc all_my'}))
        newsurls = []
        newstitles = []
        for news in soup.select('.news.section dl dt a'):#print(news['href'])#print(news['title'])
            newsurls.append(news['href'])
            newstitles.append(news['title'])

        return newsurls, newstitles

def open_urls(urls):
    for url in urls:
        open_url(url)

def open_url(url):
    # Open URL in a new tab, if a browser window is already open.
    #webbrowser.open_new_tab(url + 'doc/')
    # Open URL in new window, raising the window if possible.
    webbrowser.open_new(url)

def file_parse(file_name, delimeter):
    f = open(file_name)
    content = f.read()
    return content.split(delimeter)

def print_to_excel(excel_name, urls, titles):
    dt = datetime.datetime.now()
    wb = op.Workbook()
    ws = wb.active
    ws.title = dt.strftime("%Y%m") + u" I&C"


    print(urls, titles)
    cnt = 0
    for url in urls:
        ws.cell(row=cnt+1, column=1).value = '=HYPERLINK("{}", "{}")'.format(url, titles[cnt])
        cnt += 1


    wb.save(excel_name)

if __name__ == '__main__':

    '''parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))'''

    #open_urls(file_parse('url_list.txt', '\n'))
    #open_url(naver_search('신세계아이앤씨',1)[0]) #print(naver_search('신세계아이앤씨',1)[0])
    #print_to_excel('test.xlsx',naver_search('신세계아이앤씨',1)[0],naver_search('신세계아이앤씨',1)[1])
    get_content('sample.txt')
    #open_urls(naver_search_urls(file_parse('search_input_list.txt','\n'),1))
    #url_call_by_requests_api(naver_search_url('신세계아이앤씨',1))

    # this is for campaign job.
    #print_to_excel('campaign.xlsx', file_parse('campaign_page_url.txt','\n'), file_parse('campaign_page_title.txt','\n'))
