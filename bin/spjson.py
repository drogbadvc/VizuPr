# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import sqlite3
from pprint import pprint
import BeautifulSoup

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

print "Creating JSON output on spider.js..."
howmany = int(raw_input("How many nodes? "))

cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url, status, html, nofollow
    FROM Pages JOIN Links ON Pages.id = Links.to_id
    WHERE html IS NOT NULL AND ERROR IS NULL
    GROUP BY id ORDER BY id,inbound''')

fhand = open('public/spider.js','w')
nodes = list()
maxrank = None
minrank = None
for row in cur :
    nodes.append(row)
    rank = row[2]
    #status = row[3]
    if maxrank < rank or maxrank is None : maxrank = rank
    if minrank > rank or minrank is None : minrank = rank
    if len(nodes) > howmany : break

if maxrank == minrank or maxrank is None or minrank is None:
    print "Error : please run sprank.py to start compute page rank"
    quit()

fhand.write('spiderJson = {"nodes":[\n')
count = 0
map = dict()
ranks = dict()
for row in nodes :
    if count > 0 : fhand.write(',\n')
    # print row
    rank = row[2]
    rank = 19 * ( (rank - minrank) / (maxrank - minrank) )
    s = str(row[6])
    soup = BeautifulSoup.BeautifulSoup(s)
    noindex = 0
    title = ''
    description = ''
    h1 = ''
    h2_js = []
    canonical = ''
    if soup.title is not None :
        title = soup.find('title').text
    if soup.meta is not None :
        if soup.find(attrs={"name":"description"}) is not None :
            description = ' '.join(soup.find(attrs={"name":"description"}).get('content').split())
        element = soup.find('meta').get('content')
        if element is not None :
            robots = element.find("noindex")
            if robots > -1 :
                noindex = 1
    if soup.find('link') is not None :
        if soup.find(attrs={"rel":"canonical"}) is not None :
            canonical = soup.find(attrs={"rel":"canonical"}).get('href')
    if soup.find('h1') is not None :
        h1 = soup.find('h1').text
    if soup.findAll('h2') is not None :
        arr_h2 = soup.findAll('h2')
        for h2 in arr_h2 :
            h2_js.append(h2.text)
    fhand.write('{'+'"weight":'+str(row[0])+',"rank":'+str(rank)+',"code":'+str(row[5])+', "robots":"'+str(noindex)+'", "nofollow":"'+str(row[7])+'"' )
    fhand.write(', "h2":{')
    i = 0
    for h2_thread in h2_js :
        i += 1
        fhand.write('"'+str(i)+'": "'+h2_thread+'",')
    fhand.write('},')
    fhand.write('"description":"'+str(description.replace('"','\\"'))+'", "canonical":"'+canonical+'", "title":"'+title.replace('"','\\"')+'", "id":'+str(row[3])+', "h1":"'+h1.replace('"','\\"')+'", "url":"'+row[4]+'"}')
    map[row[3]] = count
    ranks[row[3]] = rank
    count = count + 1
fhand.write('],\n')

cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
fhand.write('"links":[\n')

count = 0
for row in cur :
    # print row
    if row[0] not in map or row[1] not in map : continue
    if count > 0 : fhand.write(',\n')
    rank = ranks[row[0]]
    srank = 19 * ( (rank - minrank) / (maxrank - minrank) ) 
    fhand.write('{"source":'+str(map[row[0]])+',"target":'+str(map[row[1]])+',"value":3}')
    count = count + 1
fhand.write(']};')
fhand.close()
cur.close()

print "Open force.html in a browser to view the Force visualization"
