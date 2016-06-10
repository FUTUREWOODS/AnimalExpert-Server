from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/getAnimalname")
def search():
    conn = sqlite3.connect("./animal.db")
    conn.row_factory = dict_factory
    sql = "SELECT * FROM animals WHERE name LIKE ?"
    cur = conn.cursor()
    cur.execute(sql, [name + ';'])
    res = cur.fetchall()
    print res
    """
    # return '\n'.join(str(res))
    dic = {}
    for i, d in enumerate(res):
        dic[i] = d

    #return jsonify(dic)
    """
    return rec

"""
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
"""

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)
