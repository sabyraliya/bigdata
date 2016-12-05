from bs4 import BeautifulSoup
import xlwt
import urllib2
from datetime import datetime

def read():
    URL = 'http://vesti.kz'
    page = urllib2.urlopen(URL).read()
    return page

def read2(link):
    URL = 'http://vesti.kz' + link
    page = urllib2.urlopen(URL).read()
    return page

page_source = read()

soup = BeautifulSoup(page_source, 'html.parser')

divs = soup.findAll('div', { "class" : "event-list" })

div = divs[0]

news_list = (div.find_all('li'))

def get_link_title(li):
    href = li.find('a').get('href')
    title = li.find('span', { "class" : "event-link-title" }).string.encode('utf-8')
    return href, title

def get_user_text(div):
    href = div.find('a', { "class" : "comment-user" })
    img = href.find('img')
    user = img["title"]
    comment = div.find("div", { "class" : "comment-text" } )
    text = comment.string
    return user, text

def f(s):
    if not s:
        return "NONE"
    return s.encode("utf-8")

def write_excel(filename, link_titles, title_to_comments):
    wb = xlwt.Workbook(encoding="UTF-8")
    ws = wb.add_sheet("Vesti.kz", cell_overwrite_ok=True)
    ws.write(0, 0, "Links")
    ws.write(0, 1, "Titles")
    ws.write(0, 2, "Comments")
    row = 1
    for (link, title) in link_titles:
        ws.write(row, 0, link)
        ws.write(row, 1, title)
        comments = title_to_comments[title]
        for comment in comments:
            print " "
            print comment
            print " "
            s = f(comment.get("user", "NONE")) + ": " + f(comment.get("text", "NONE"))
            ws.write(row, 2, s)
            row += 1
    wb.save(filename)

link_titles = []
title_to_comments = {}

for li in news_list:
    href, title = get_link_title(li)
    comments = read2(href)
    comments_soup = BeautifulSoup(comments, 'html.parser')
    comments = comments_soup.find_all('div', { "class" : "comment" } )
    link_titles.append((href, title))
    comments1 = []
    for comment in comments:
        user, text = get_user_text(comment)
        comments1.append({"user" : user, "text" : text})
    title_to_comments[title] = comments1

write_excel("vesti.xls", link_titles, title_to_comments)

