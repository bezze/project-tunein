#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import re

from sys import argv, exit
from subprocess import call
import urllib.request as ur
import urllib.parse as up

UserAgent="Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

PLAYER="mpv"
OPTS="--no-video"

def query_tunein(argv):

    root='https://tunein.com/search/?'
    query = { 'query': argv }
    query_enc = up.urlencode(query) #.encode('utf-8')
    searchReq = ur.Request(root+query_enc) #, data=)
    searchReq.add_header('User-Agent',UserAgent)
    
    soup = bs(ur.urlopen(searchReq), 'html.parser')

    return soup

def get_query(soup):

    re_link=re.compile('.*'+re.escape('guide-item__guideItemLink___3w_uL')+'.*') 
    re_title=re.compile('.*'+re.escape('guide-item__guideItemTitle___VBHQg')+'.*')
    re_subtitle=re.compile('.*'+re.escape('guide-item__guideItemSubtitle___2hQxF')+'.*') 
    get_meta=soup.find_all('a', class_=re_link)

    result_dir={}
    for meta in get_meta:
        try:
            href = meta.get('href')
            link = 'https://tunein.com' + href
            title = meta.find(class_=re_title).string
            subtitle = meta.find(class_=re_subtitle).string
            name = title +' - '+subtitle
            i = len(result_dir) +1 
            result_dir[i]=[name, link]

        except AttributeError:
            pass

    """ Not supported yet """    
    # Get common categories
    # get_common=soup.find_all('a', class_="navigationMenuItem__link___3PXCP")
    # nav_dir={}
    # print('Nav Menu')
    # for common in get_common:
    #     href = common.get('href')
    #     link = 'https://tunein.com' + href
    #     name = 
    #     i = len(result_dir) +1 
    #     result_dir[i]=[name, link]

    return result_dir

def print_results(res_dir):

    print('#\tName')
    for entry in res_dir:
        name, link = res_dir[entry]
        line = "\t".join([str(entry), name])
        print(line)


def get_soup_radio(search_web):

    request = ur.Request(search_web)
    request.add_header('User-Agent',UserAgent)
    raw_page = ur.urlopen(request) #, data=query )
    soup = bs(raw_page, 'html.parser')

    return soup


def get_radio_link(soup):

    get_meta=soup.find_all('meta')
    for meta in get_meta:
        content = meta.get('content')
        if content!=None:
            escaped=re.escape('http://tun.in/') # Escape slashes and dots
            regular=re.compile(escaped+'.*') # Compiling expression. Search for strings starting with 'escaped'
            match=re.match(regular, content) # Actual searching 
            if match: # match returns True if it matchs
                link=match.group(0)

    return link

def main(argv):

    argv = ' '.join(argv)

    soup = query_tunein(argv)

    results=get_query(soup)

    print_results(results)

    try:                                                                             
        selected_radio = input('Enter number: ')
    except KeyboardInterrupt:                                                        
        print('\n')                                                    
        exit()

    soup_radio = get_soup_radio( results[int(selected_radio)][1] )

    link_hash = get_radio_link(soup_radio)

    calls=[PLAYER, OPTS, link_hash]

    call(calls)

if __name__ == "__main__":
    main(argv[1:])
