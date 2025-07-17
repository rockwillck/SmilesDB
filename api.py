from flask import Flask, render_template, jsonify, url_for, redirect
import random
import json
import markdown

app = Flask(__name__)

with open("data/smilesData.txt", "r") as f:
    molList = list(map(json.loads, f.readlines()))
    smilesList = list(map(lambda x : x["SMILES"], molList))

with open("CITATIONS.md", "r") as cit:
    citations_html = markdown.markdown(cit.read())

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/docs")
def docs():
    return redirect("https://github.com/rockwillck/SmilesDB/wiki")
@app.route("/api")
def api_docs():
    return redirect("https://github.com/rockwillck/SmilesDB/wiki/API-Documentation")
@app.route("/citations")
def citations():
    return render_template("citations.html")
@app.route("/explore")
def exp():
    return render_template("explore.html")

@app.route("/api/smiles/full")
def smiles_full():
    return jsonify(smilesList)

@app.route("/api/smiles/<string:endpoint>/<int:num>")
def smiles_api(endpoint, num):
    match endpoint:
        case "random":
            return jsonify(random.sample(smilesList, min(num, len(smilesList))))
        case "short":
            return jsonify(smilesList[:num])
        case "long":
            return jsonify(smilesList[-num:])
        case _:
            return "INVALID ENPOINT", 404

@app.route("/api/full")
def full():
    return jsonify(molList)

@app.route("/api/<string:endpoint>/<int:num>")
def api(endpoint, num):
    match endpoint:
        case "random":
            return jsonify(random.sample(molList, min(num, len(smilesList))))
        case "short":
            return jsonify(molList[:num])
        case "long":
            return jsonify(molList[-num:])
        case _:
            return "INVALID ENPOINT", 404
        
@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html") 