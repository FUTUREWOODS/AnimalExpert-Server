# -*- coding: utf-8 -*-
from flask import Flask, jsonify, Response
import json
import sqlite3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def jsonp(data, callback="f"):
    return Response(
        "{}({});".format(callback, json.dumps(data)),
        mimetype="text/javascript"
    )


@app.route("/getAnimalname")
def animal_name_search():
    conn = sqlite3.connect("./animal.db")
    cur = conn.execute('SELECT name FROM animals')
    r = cur.fetchall()
    keyword = ""
    for i in range(len(r)):
        keyword += r[i][0] + ";"
    return keyword


@app.route("/<name>")
def search(name):
    conn = sqlite3.connect("./animal.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = "SELECT * FROM animals WHERE name LIKE ?"
    cur.execute(sql, ['%' + name + '%'])
    res = cur.fetchall()
    dic = {}
    for i, d in enumerate(res):
        dic[i] = d
    return jsonify(dic)


@app.route("/autocomplete/")
@app.route("/autocomplete/<name>")
def autocomplete(name=""):
    conn = sqlite3.connect("./animal.db")
    cur = conn.cursor()
    sql = "SELECT name FROM animals WHERE name LIKE ? LIMIT 5"
    cur.execute(sql, ['%' + name + '%'])
    res = cur.fetchall()

    arr=[row[0] for row in res]
    return jsonp(arr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
