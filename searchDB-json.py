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
        	self.category = "動物"
		self.category2 = "亜種"
		self.category3 = "１種"
		self.category4 = "世界最大種"
		self.country = "国"
		self.connectionword = ""
		cJuman.init(['-B', '-e2'])

	def extractKeyWords(self, txt):
		self.keywordList = []
		node = self.parse(txt)
		print node
		wordsList = []
		categoryList = []
		wikiword = ""
		wordsList = node.split("\n")
		for i in range(len(wordsList)):
			self.connectionFlag = 0
			if "カテゴリ" in wordsList[i]:
				self.categoryParse(wordsList[i], 0)
					
			elif "Wikipedia上位語:" in wordsList[i]:
				self.wikiWordsParse(wordsList[i])
			
			elif "地名" in wordsList[i]:
				self.countryParse(wordsList[i])
				print self.connectionword			

			else:
				self.connectionword = ""

		listlen = len(self.keywordList)
		if listlen != 0:
			while True:
				if len(self.keywordList) > 1:
					if self.category in self.keywordList[-1]  or self.category2 in self.keywordList[-1] or self.category3 in self.keywordList[-1] or self.category4 in self.keywordList[-1]:
						self.keywordList.pop()
					else:
						return self.keywordList[-1]
							
				else:
					if self.category in self.keywordList[-1]  or self.category2 in self.keywordList[-1] or self.category3 in self.keywordList[-1] or self.category4 in self.keywordList[-1]:
						return "0"
					else:
						return self.keywordList[-1]
		else:
			return "0"

	def parse(self, txt):
		node = cJuman.parse_opt([txt], cJuman.SKIP_NO_RESULT)
		return node

	def categoryParse(self, jumantxt, wikiflag):
		categorylist = []

		if "カテゴリ" in jumantxt:
			categorylist = jumantxt.split("カテゴリ:")
			if self.category in categorylist[1] :
				if not "植物" in categorylist[1] :
					categorylist = jumantxt.split(" ")
					if not self.category in categorylist[0]:
						if wikiflag == 0:
							self.keywordList.append(self.connectionword + categorylist[0])
						elif wikiflag == 1:
							self.wikiList.append(categorylist[0])
	def wikiWordsParse(self, jumantxt):
		self.wikiList = []
		categorylist = []
		wikilist = []
		wikiword = ""
		if "Wikipedia上位語:" in jumantxt:
			categorylist = jumantxt.split("Wikipedia上位語:")
			categorylist = categorylist[1].split("\"")
			categorylist = categorylist[0].split("/")
			wikiword = categorylist[0]
			if self.category2 in categorylist[0] or self.category3 in categorylist[0] or self.category4 in categorylist[0]:
				categorylist = jumantxt.split(" ")
				self.keywordList.append(self.connectionword + categorylist[0])
				
			else:
				wikiword = self.parse(wikiword)
				self.categoryParse(wikiword,1)
				
				if len(self.wikiList) != 0:
					categorylist = jumantxt.split(" ")
					self.keywordList.append(self.connectionword + categorylist[0])

	def countryParse(self, jumantxt):
		categorylist = []
		if "地名" in jumantxt:
			categorylist = jumantxt.split("地名:")
			if self.country in categorylist[1] :
				categorylist = jumantxt.split(" ")
				self.connectionword = categorylist[0]
		

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
        message = j.extractKeyWords(txt)
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
