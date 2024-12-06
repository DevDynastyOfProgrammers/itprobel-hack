from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import gen_wordsForCloud, generate_wordcloud

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/trigger_function', methods=['GET', 'POST'])
def trigger_function():
    print(request.method)
    wordsForCloud = gen_wordsForCloud()
    wordcloud = generate_wordcloud(wordsForCloud)
    wordcloud.to_file('./static/img/hp_cloud_simple.png')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)