from flask import Flask, render_template

app = Flask(__name__)

@app.route("/score")
def score():
    return render_template('score.html')

@app.route("/levels")
def levels():
    return render_template("levels.html")

@app.route("/rounds")
def topics():
    return render_template("rounds.html")

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
