from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def topics():
    return render_template("zig_zag.html")

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
