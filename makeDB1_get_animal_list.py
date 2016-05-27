import urllib.request
import urllib.parse
import re
import sqlite3
import time


def search_list_page(page_num):
    url = "http://www.tokyo-zoo.net/encyclopedia/keyword_search_list?&page={}".format(page_num)
    post_data = {
        'keyword': '%',
        'type': 'and'
    }
    encoded_post_data = urllib.parse.urlencode(post_data).encode(encoding='ascii')

    with urllib.request.urlopen(url=url, data=encoded_post_data) as f:  # POST
        html = f.read().decode('utf-8')

    pattern = re.compile(
        r'\s*<tr>'
        r'\s*<td bgcolor="#D7EAF2"><FONT CLASS="txtM" COLOR="#176A8D">(?P<order>.*)</FONT></td>'
        r'\s*<td bgcolor="#D7EAF2"><FONT CLASS="txtM" COLOR="#176A8D">(?P<family>.*)</FONT></td>'
        r'\s*<td bgcolor="#D7EAF2"><a href="javascript:speciesDetail\((?P<id>[0-9]*)\)" CLASS="txtM">(?P<species>.*)</a></td>'
        r'\s*</tr>'
    )

    ms = list(pattern.finditer(html))  # findallだとMatchオブジェクトが返ってこない
    for m in ms:
        sql = "INSERT OR REPLACE INTO animals(id, name, taxonomy_order, taxonomy_family) VALUES(?,?,?,?)"
        cur.execute(sql, (m.group("id"), m.group("species"), m.group("order"), m.group("family")))
    return len(ms)


def get_all_search_list():
    total_cnt = 0
    page_num = 1
    while True:
        print(page_num)
        cnt = search_list_page(page_num)
        total_cnt += cnt
        if cnt != 20:
            break
        page_num += 1
        time.sleep(0.5)
    return total_cnt


conn = sqlite3.connect("./animal.db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS animals("
    "id INT PRIMARY KEY, name TEXT,taxonomy_order TEXT, taxonomy_family TEXT,"
    "zoo TEXT, habitat TEXT, size TEXT,feed TEXT, description TEXT,"
    "img_url TEXT, cry_url TEXT, movie_url TEXT)")


total_cnt = get_all_search_list()
print("[*] TOTAL COUNT: {}".format(total_cnt))


conn.commit()
conn.close()
