# -*- coding:utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import types
import cJuman

TEXT_ENCODING = "utf-8"
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

class juman:
	
	def __init__(self):
		cJuman.init(['-B', '-e2'])

	def extractKeyWords(self, txt, category):
		self.keywordList = []
		node = self.parse(txt)
		print node
		wordsList = []
		categoryList = []
		wikiword = ""
		wordsList = node.split("\n")
		for i in range(len(wordsList)):
			if "カテゴリ" in wordsList[i]:
				self.categoryParse(wordsList[i],category, 0)
					
			elif "Wikipedia上位語:" in wordsList[i]:
				self.wikiWordsParse(wordsList[i],category)
		if len(self.keywordList) != 0:
			return self.keywordList[0]
		else:
			return "0"

	def parse(self, txt):
		node = cJuman.parse_opt([txt], cJuman.SKIP_NO_RESULT)
		return node

	def categoryParse(self, jumantxt, category, wikiflag):
		categorylist = []
		if "カテゴリ" in jumantxt:
			categorylist = jumantxt.split("カテゴリ:")
			categorylist = categorylist[1].split("\"")
			if categorylist[0] == category:
				categorylist = jumantxt.split(" ")
				if not category in categorylist[0]:
					if wikiflag == 0:
						self.keywordList.append(categorylist[0])
					elif wikiflag == 1:
						self.wikiList.append(categorylist[0])
	def wikiWordsParse(self, jumantxt,category):
		self.wikiList = []
		categorylist = []
		wikilist = []
		wikiword = ""
		if "Wikipedia上位語:" in jumantxt:
			categorylist = jumantxt.split("Wikipedia上位語:")
			categorylist = categorylist[1].split("\"")
			categoryList = categorylist[0].split("/")
			wikiword = categorylist[0]
			wikiword = self.parse(wikiword)
			self.categoryParse(wikiword,category,1)
			if len(self.wikiList) != 0:
				categorylist = jumantxt.split(" ")
				if not category in categorylist[0]:
					self.keywordList.append(categorylist[0])

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def hello():
	return "Hello World"

@app.route('/morph/<string:txt>')
def index(txt):
	txt = txt.encode(TEXT_ENCODING)
        category = "動物"
        message = j.extractKeyWords(txt,category)
        return message

@app.route("/<name>")
def search(name):
    conn = sqlite3.connect("./animal.db")
    conn.row_factory = dict_factory
    sql = "SELECT * FROM animals WHERE name LIKE ?"
    cur = conn.cursor()
    cur.execute(sql, ['%' + name + '%'])
    res = cur.fetchall()
    # return '\n'.join(str(res))
    dic = {}
    for i, d in enumerate(res):
        dic[i] = d
    return jsonify(dic)


if __name__ == "__main__":
    j = juman()
    app.run(host='0.0.0.0', debug=False)
