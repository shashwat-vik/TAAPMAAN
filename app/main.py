from flask import Flask, render_template

app = Flask(__name__)

@app.route("/front")
def front():
    return render_template("front.html")

@app.route("/question")
def question():
    return render_template("question2.html")

@app.route("/score")
def score():
    return render_template("score.html")

@app.route("/levels")
def levels():
    return render_template("levels.html")

@app.route("/topics")
def topics():
    return render_template("topics.html")

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
