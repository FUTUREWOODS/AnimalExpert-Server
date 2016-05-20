import urllib.request
import urllib.error
from html.parser import HTMLParser
import re
import time
import sqlite3


class Animal():
    # __slots__ = ['id', 'name', 'habitat', "size", "feed", "description", 'img', "cry"]
    # TODO: namedtuple使えばよくね？

    # XXX: deprecated
    def __str__(self):
        return """\
ID: {0.id}
名前: {0.name}
画像URL: {0.img}
生息地: {0.habitat}
体の大きさ: {0.size}
えさ: {0.feed}
特徴: {0.description}
""".format(self)

    def getVal(self):
        d = self.__dict__
        return (d["id"], d["name"], d.get("habitat"), d.get("size"), d.get("feed"), d.get("description"), d.get("img"),
                d.get("cry"))


class MyHTMLParser(HTMLParser):
    def __init__(self, animal):
        super().__init__()
        self.animal = animal

        # 名称・生息地・体の大きさ・えさ・特徴のテーブルのパースのため
        self.hasDataToBeHandled = False
        self.datatype = None

    def handle_starttag(self, tag, attrs):
        # img
        if tag == "a" and attrs[0][0] == "href" and re.match(r"javascript:openWin.*", attrs[0][1]):
            try:
                img = re.search(r"'(.*\.jpg)'", attrs[0][1]).group(1)
            except AttributeError as e:  # http://www.tokyo-zoo.net/encyclopedia/species_detail?species_code=384 画像の拡張子がない！！
                print("ID: {0} CORRUPT DATA! TRY ALTERNATIVE PATTERN! ({1})".format(id, e))
                img = re.search(r"javascript:openWin\('([^']*)'", attrs[0][1]).group(1)
            self.animal.img = "http://www.tokyo-zoo.net/Encyclopedia/LSpecies/" + img

        # cry
        if tag == "embed" and attrs[0][0] == "src":
            cry = re.match(r"\.\./(Encyclopedia/Cry/.*.mov)", attrs[0][1]).group(1)
            if not cry:
                return
            self.animal.cry = "http://www.tokyo-zoo.net/" + cry

        # その他. handle_dataで処理
        if tag == "font":
            self.hasDataToBeHandled = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.hasDataToBeHandled:
            # print(data)
            if not self.datatype is None:
                setattr(self.animal, self.datatype, data)
                self.datatype = None
            else:
                if data == "名称":
                    self.datatype = 'name'
                elif data == "生息地":
                    self.datatype = 'habitat'
                elif data == "体の大きさ":
                    self.datatype = 'size'
                elif data == "えさ":
                    self.datatype = 'feed'
                elif data == "特徴":
                    self.datatype = 'description'
        self.hasDataToBeHandled = False


def get_url(id):
    return "http://www.tokyo-zoo.net/encyclopedia/species_detail?species_code=" + str(id)


def get_data(id):
    try:
        with urllib.request.urlopen(get_url(id)) as f:
            html = f.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print("ID: {0} ERROR OCCUERED! ({1})".format(id, e))
        return None

    animal = Animal()
    animal.id = id

    parser = MyHTMLParser(animal)
    parser.feed(html)

    return animal


conn = sqlite3.connect("/tmp/animal.db")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS animals(id INT PRIMARY KEY, name TEXT, habitat TEXT, size TEXT,feed TEXT, description TEXT, img_url TEXT, cry_url TEXT)")

for id in range(0, 385): #XXX: 適宜変更
    print(id)

    animal = get_data(id)
    if not animal:
        continue

    sql = "INSERT OR REPLACE INTO animals VALUES (?,?,?,?,?,?,?,?)"
    cur.execute(sql, animal.getVal())
    conn.commit()

    time.sleep(3)

conn.close()
