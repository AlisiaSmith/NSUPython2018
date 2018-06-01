# -*- coding: utf-8 -*-
import re
import sys
from time import time, sleep

from bs4 import BeautifulSoup
from urllib import parse
# from urllib import request
from io import StringIO
from requests import get

SUITABLE_URLS = ("https://ru.wikipedia.org/wiki/%D0%A4%D0%B8%D0%BB%D0%BE%D1%81%D0%BE%D1%84%D0%B8%D1%8F",
                 "https://en.wikipedia.org/wiki/Philosophy")
DELAY_BETWEEN_REQUESTS = 0.5


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def check_url(text):
    parsed_result = parse.urlparse(text)
    # print(parsed_result)
    if not 'wikipedia' in parsed_result.netloc:
        raise ValueError('bad url')
    return parsed_result.scheme, parsed_result.netloc, parsed_result.path


def is_suitable_url(url):
    text_url = str(url)
    for i in range(len(SUITABLE_URLS)):
        # print(text_url + " vs \n" + SUITABLE_URLS[i])
        if text_url == SUITABLE_URLS[i]:
            return True
    return False


def relieve_text_from_brackets(text):
    array_of_open_brackets = [0, 0, 0]
    open_symbols = ('(', '[', '{')
    close_symbols = (')', ']', '}')
    count_of_open_blocks = 0
    out = StringIO()
    for symbol in text:
        if symbol == '<':
            count_of_open_blocks += 1

        if symbol == '>':
            count_of_open_blocks -= 1

        if count_of_open_blocks > 0 and all(bracket == 0 for bracket in array_of_open_brackets):
            out.write(symbol)
            continue

        try:
            index = open_symbols.index(symbol)
            array_of_open_brackets[index] += 1
        except ValueError:
            pass

        try:
            index = close_symbols.index(symbol)
            array_of_open_brackets[index] -= 1
            continue
        except ValueError:
            pass

        if all(bracket == 0 for bracket in array_of_open_brackets):
            out.write(symbol)

    return out.getvalue()


def is_correct_link(tag):
    #uprint(tag)
    if tag.name is not 'a':
        return False
    #if tag.has_attr('class'):
    #    print(tag['class'] == ['new'])
    if tag.has_attr('class') and tag['class'] == ['new']:
        return False
    if not tag.has_attr('href') or not tag['href'].startswith('/'):
        return False
    return True


def find_all_blocks(main_block, *param, **param2):
    #print(found)
    #if found is None:
    #    print("End of search: not found!")
    #    sys.exit(-1)
    found = main_block.find(param, **param2)
    while found is not None:
        yield found
        found = found.find_next(param, **param2)


def find_all_link(block, tag):
    link = block.find(tag)
    while link is not None:
        yield link
        link = block.find_next(tag)


def find_first_link_on_page(request):
    soup = BeautifulSoup(request.text, "lxml")
    main_block = soup.find('div', attrs={'class': 'mw-parser-output'})
    # for main_block in soup.find_all('div', attrs={'class': 'mw-parser-output'}):
    # for div in main_block.find_all("div", {'class': 'thumb tright'}):
    #    div.decompose()
    for block in find_all_blocks(main_block, ['p', 'dd', 'ul'], recursive=False):
        #uprint(block)
        block = BeautifulSoup(relieve_text_from_brackets(str(block)), 'lxml')
        if block is None:
            continue
        for link in find_all_link(block, is_correct_link):
            #uprint(link)
            return link


def check_time(last_time_connect):
    time_to_sleep = last_time_connect + DELAY_BETWEEN_REQUESTS - time()
    if time_to_sleep > 0:
        #print("sleep")
        sleep(time_to_sleep)
    return


def main(scheme, netloc, path, mode):
    visited_URLs = list()
    last_time_connect = time()
    if is_suitable_url(scheme + '://' + netloc + path):
        print("You entered wanted link!")
        return
    while True:
        req = get(scheme + '://' + netloc + path)
        check_time(last_time_connect)
        last_time_connect = time()
        link = find_first_link_on_page(req)
        if link is None:
            print("End of search: on article '%s' have no external links" % title)
            break
        # print(link)
        path = link['href']
        url = scheme + '://' + netloc + path
        title = link['title']
        if mode == 0:
            print(title, url)
        else:
            print(title)
        #print(time())
        if visited_URLs.count(path) != 0:
            print("End of search: search is cycled")
            break
        if is_suitable_url(url):
            print("End of search: found!")
            break
        # print(is_suitable_url(url))
        visited_URLs.append(path)
    return


if len(sys.argv) < 2:
    mode = 0
    print("You entered bad url, it's should contains 'wikipedia' url's"
          "wiki.py URL - standard mode"
          "wiki.py URL 0 - standard mode"
          "wiki.py URL 1 - mode without URLs names")
    sys.exit(-1)
mode = 0
if len(sys.argv) > 2:
    try:
        mode = int(sys.argv[2])
        if mode > 1 or mode < 0:
            mode = 0
    except ValueError:
        mode = 0
try:
    scheme, netloc, path = check_url(sys.argv[1])
    main(scheme, netloc, path, mode)
except ValueError as error:
    print(error, file=sys.stderr)
except KeyboardInterrupt:
    print("You sent interrupt command, bye!")
    sys.exit(0)
