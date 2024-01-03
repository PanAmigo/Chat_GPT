import openai
import ast
import traceback
import random
import json

import pyodbc as pyodbc
import pandas as pd

from pprint import pprint
from flask import Flask, request, render_template, jsonify, redirect
from cheroot.wsgi import Server

app = Flask(__name__)

with open('credentials.txt', 'r') as f:
    credentials_content = f.read()
credentials = ast.literal_eval(credentials_content)

openai.api_key = credentials['key']
with pyodbc.connect(credentials['serwer']) as myconn:
    mycursor = myconn.cursor()

with open('config.txt', 'r') as f:
    config_content = f.read()
config = ast.literal_eval(config_content)


@app.route("/chat", methods=["POST"])
def get_ai_response():
    try:
        question = request.json["question"]
        suffix = request.json["suffix"]
        try:
            history_of_conversation = json.loads(
                pd.read_sql_query(f"SELECT message FROM app_chatgpt WHERE url_suffix = '{suffix}'",
                                  myconn)["message"][0])
        except:
            history_of_conversation = []
        history_of_conversation.append({
            "role": "user",
            "content": f"{question}"
        })
        if len(history_of_conversation) > config["max_history"]:
            msg1 = history_of_conversation[-config["max_history"]:]
        else:
            msg1 = history_of_conversation
        response = openai.ChatCompletion.create(
            model=config["model"],
            messages=msg1,
            temperature=config["temperature"],
            max_tokens=config["max_tokens"])
        chat_answer = response.choices[0]
        history_of_conversation.append(chat_answer["message"])
        mycursor.execute(f"UPDATE app_chatgpt SET message = ? where url_suffix = ?",
                         json.dumps(history_of_conversation), suffix)
        myconn.commit()
    except:
        traceback.print_exc()
        return jsonify({"answer": "error"})
    else:
        return jsonify({"answer": chat_answer["message"]["content"]})


@app.route("/")
def index():
    userip = request.remote_addr
    newsuffix = hex(random.randint(1600, 1000000))[2:]
    temp_df = pd.read_sql_query(f"SELECT * FROM app_chatgpt WHERE url_suffix = '{newsuffix}'", myconn)
    if not temp_df.empty:
        while not temp_df.empty:
            newsuffix = hex(random.randint(1600, 1000000))[2:]
            temp_df = pd.read_sql_query(
                f"SELECT COUNT(*) AS ISTNIEJE FROM [app_chatgpt] WHERE url_suffix = '{newsuffix}'", myconn)
    mycursor.execute(f"INSERT into app_chatgpt(ip, url_suffix, model_version) values (?, ?, ?)", userip, newsuffix,
                     config["model"])
    myconn.commit()
    return redirect(f"/{newsuffix}")


@app.route("/<suffix>", methods=["GET"])
def index_view(suffix):
    temp_df = pd.read_sql_query(f"SELECT message FROM app_chatgpt WHERE url_suffix = '{suffix}'", myconn)
    try:
        history = json.loads(temp_df["message"][0])
        if history:
            return render_template("index.html", history=history)
    except IndexError:
        print((traceback.format_exc()))
    except TypeError:
        print((traceback.format_exc()))
    except Exception:
        print((traceback.format_exc()))
    return render_template("index.html")


@app.route("/error_page.html", methods=["GET"])
def error_page():
    return render_template("error_page.html")


if __name__ == '__main__':
    server = Server(bind_addr=(config['HOST'], config['PORT']), wsgi_app=app, numthreads=100)
    server.start()
