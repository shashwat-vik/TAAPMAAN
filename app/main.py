from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# GLOBALS
#########################
# DIGIT 1 IN LPAT IMPLIES THAT ITS NOT USED AT ALL
TEAM_STATS = {
    'A': {'SCORE':0, 'LPAT':'1111'},
    'B': {'SCORE':0, 'LPAT':'1111'},
    'C': {'SCORE':75, 'LPAT':'1111'}
}
CURR_STATS = {'TEAM':None, 'TOPIC':None, 'LEVEL':None}
#########################


@app.route("/front")
def front():
    return render_template("front.html")

@app.route("/score")
def score():
    return render_template("score.html")

@app.route("/topics/<TEAM>", methods=['GET', 'POST'])
def topics(TEAM):
    global TEAM_STATS, CURR_STATS
    if request.method == 'GET':     # COMING BY USER
        CURR_STATS['TEAM'] = TEAM           # UPDATE LOCALLY FIRST
        data = {
                'TEAM':CURR_STATS['TEAM'],
                'CURR_SCORE':TEAM_STATS[TEAM]['SCORE']
                }
        return render_template("topics.html", data=data)

    else:                           # COME BY AJAX FROM QUESTION PAGE
        NEW_SCORE, LPAT = request.form['NEW_SCORE'], request.form['LPAT']
        TEAM = CURR_STATS['TEAM']
        TEAM_STATS[TEAM]['SCORE'], TEAM_STATS[TEAM]['LPAT'] = NEW_SCORE, LPAT
        print("UPDATED", request.form)
        return "UPDATED"

@app.route("/levels/<TEAM>/<TOPIC>")
def levels(TEAM, TOPIC):
    global CURR_STATS
    # UPDATE AGAIN JUST TO KEEP THINGS IN SYNC UNTIL NOT EVERYTHING IS VERIFIED.
    CURR_STATS['TEAM'], CURR_STATS['TOPIC'] = TEAM, TOPIC
    data = {
            'TEAM':CURR_STATS['TEAM'],
            'TOPIC':CURR_STATS['TOPIC']
            }
    return render_template("levels.html", data=data)

@app.route("/question/<TEAM>/<TOPIC>/<LEVEL>")
def question(TEAM, TOPIC, LEVEL):
    global CURR_STATS
    CURR_STATS['TEAM'], CURR_STATS['TOPIC'], CURR_STATS['LEVEL'] = TEAM, TOPIC, LEVEL
    data = {
            'TEAM':CURR_STATS['TEAM'],
            'TOPIC':CURR_STATS['TOPIC'],
            'LEVEL':CURR_STATS['LEVEL'],
            'CURR_SCORE':TEAM_STATS[TEAM]['SCORE'],
            'LPAT':TEAM_STATS[TEAM]['LPAT'],
            'NEXTP':url_for('topics', TEAM=CURR_STATS['TEAM'])
            }
    return render_template("question2.html", data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
