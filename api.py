from flask import Flask, render_template, jsonify, url_for, redirect, request
import random
import json
import markdown
import requests

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
def explore():
    return render_template("captcha.html")

@app.route("/captcha-check/<string:forward>", methods=["GET", "POST"])
def captcha(forward):
    if request.method == "GET":
        return redirect(url_for(forward))
    
    token = request.form.get("capycap-token")

    # Verify captcha with CapyCap API
    response = requests.post('https://capycap.ai/api/captcha/verify', 
                           headers={'Content-Type': 'application/json'},
                           json={
                               'token': token,
                               'sitekey': 'capy_live_9zEf9l3e9neg4CgqkB50lR0ahnqUAanC'
                           })
    
    result = response.json()
    success = result.get('success', False)
    
    if not success:
        return jsonify({'error': 'Captcha verification failed'}), 400
    return render_template(f"{forward}.html")
    
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