from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# GLOBALS
#########################
# DIGIT 1 IN *PAT IMPLIES THAT ITS NOT USED AT ALL
TEAM_STATS = {
    'A': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'},
    'B': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'},
    'C': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'},
    'D': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'},
    'E': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'},
    'F': {'SCORE':0, 'LPAT':'1111', 'TOPICS_PAT':'1111111111'}
}
CURR_STATS = {'TEAM':None, 'TOPIC':None, 'LEVEL':None}

TOPIC_MAPPING = {
                'TH1':0,
                'TH2':1,
                'TH3':2,
                'BE':3,
                'GK':4,
                'FM':5,
                'IAQ':6,
                'AV':7,
                'WT':8,
                'EQ':9
                }
#########################

def update_topics_used(TEAM, TOPIC):
    global TEAM_STATS
    TOPICS_PAT = TEAM_STATS[TEAM]['TOPICS_PAT']
    temp = [i for i in TOPICS_PAT]
    temp[TOPIC_MAPPING[TOPIC]] = '0'
    TEAM_STATS[TEAM]['TOPICS_PAT'] = ''.join(temp)

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
                'CURR_SCORE':TEAM_STATS[TEAM]['SCORE'],
                'TOPICS_PAT':TEAM_STATS[TEAM]['TOPICS_PAT']
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
    update_topics_used(TEAM, TOPIC)
    data = {
            'TEAM':CURR_STATS['TEAM'],
            'TOPIC':CURR_STATS['TOPIC']
            }
    return render_template("levels.html", data=data)

@app.route("/question/<TEAM>/<TOPIC>/<LEVEL>")
def question(TEAM, TOPIC, LEVEL):
    global CURR_STATS
    CURR_STATS['TEAM'], CURR_STATS['TOPIC'], CURR_STATS['LEVEL'] = TEAM, TOPIC, LEVEL
    NEXTP = None

    #########################
    # NEXT PAGE LINK HANDLING
    topics_over=True
    TOPICS_PAT = TEAM_STATS[TEAM]['TOPICS_PAT']
    for i in TOPICS_PAT:
        if i == '1':
            topics_over=False
    if topics_over: NEXTP = url_for('score')
    else: NEXTP = url_for('topics', TEAM=CURR_STATS['TEAM'])
    ##########################

    data = {
            'TEAM':CURR_STATS['TEAM'],
            'TOPIC':CURR_STATS['TOPIC'],
            'LEVEL':CURR_STATS['LEVEL'],
            'CURR_SCORE':TEAM_STATS[TEAM]['SCORE'],
            'LPAT':TEAM_STATS[TEAM]['LPAT'],
            'NEXTP':NEXTP,
            'AJAXPOST_URL':url_for('topics', TEAM=TEAM)
            }
    return render_template("question2.html", data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
