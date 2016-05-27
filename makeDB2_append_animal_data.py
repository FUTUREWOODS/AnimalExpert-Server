import urllib.request
import urllib.error
from html.parser import HTMLParser
import re
import time
import sqlite3


class Animal():
    def __init__(self):
        # 代入されない可能性があるものについて初期化(for sql placeholder)
        #id,nameはNoneとならない
        self.zoo = None
        self.habitat = None
        self.size = None
        self.feed = None
        self.description = None
        self.img = None
        self.cry = None
        self.movie = None

    def getVal(self):
        d = self.__dict__
        return d


class MyHTMLParser(HTMLParser):
    def __init__(self, animal):
        super().__init__()
        self.animal = animal

        # 名称・生息地・体の大きさ・えさ・特徴のテーブルのパースのため
        self.hasDataToBeHandled = False
        self.datatype = None

    def handle_starttag(self, tag, attrs):
        # img & movie
        if tag == "a" and attrs[0][0] == "href":
            if re.match(r"javascript:openWin.*", attrs[0][1]):  # img
                try:
                    img = re.search(r"'(.*\.jpg)'", attrs[0][1]).group(1)
                except AttributeError as e:  # http://www.tokyo-zoo.net/encyclopedia/species_detail?species_code=384 画像の拡張子がない！！
                    print("ID: {0} CORRUPT IMG HREF! TRY ALTERNATIVE PATTERN! ({1})".format(id, e))
                    img = re.search(r"javascript:openWin\('([^']*)'", attrs[0][1]).group(1)
                if img:
                    self.animal.img = "http://www.tokyo-zoo.net/Encyclopedia/LSpecies/" + img
            elif re.match(r"javascript:openMovieWin.*", attrs[0][1]):  # movie
                try:
                    movie = re.search(r"'(.*/index\.html)'", attrs[0][1]).group(1)
                    self.animal.movie = "http://www.tokyo-zoo.net/movie/mov_book/" + movie
                except AttributeError as e:
                    print("ID: {0} CORRUPT MOVIE HREF!".format(id, e))

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
                if data == "飼育園館":
                    self.datatype = 'zoo'
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


conn = sqlite3.connect("./animal.db")
cur = conn.cursor()

sql = "SELECT id FROM animals"
cur.execute(sql)
ids = map(lambda x: x[0], cur.fetchall())

for id in ids:
    print(id)

    animal = get_data(id)
    if not animal:
        continue

    sql = "UPDATE animals SET " \
          "name=:name," \
          "zoo=:zoo," \
          "habitat=:habitat," \
          "size=:size," \
          "feed=:feed," \
          "description=:description," \
          "img_url=:img," \
          "cry_url=:cry," \
          "movie_url=:movie " \
          "WHERE id = :id"
    cur.execute(sql, animal.getVal())
    time.sleep(0.5)

conn.commit()
conn.close()
