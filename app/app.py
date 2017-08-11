import os
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
CURR_STATS = {'TEAM':None, 'TOPIC':None, 'LEVEL':None, 'DOUBLE_HALF':None}

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
    data = {
        'A':TEAM_STATS['A']['SCORE'],
        'B':TEAM_STATS['B']['SCORE'],
        'C':TEAM_STATS['C']['SCORE'],
        'D':TEAM_STATS['D']['SCORE'],
        'E':TEAM_STATS['E']['SCORE'],
        'F':TEAM_STATS['F']['SCORE'],
    }
    return render_template("score.html", data=data)

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

    else:                           # COMING BY AJAX FROM QUESTION PAGE
        NEW_SCORE, LPAT = request.form['NEW_SCORE'], request.form['LPAT']
        TEAM = CURR_STATS['TEAM']
        TEAM_STATS[TEAM]['SCORE'], TEAM_STATS[TEAM]['LPAT'] = NEW_SCORE, LPAT
        print("UPDATED", request.form)
        return "UPDATED"

@app.route("/levels/<TEAM>/<TOPIC>", methods=['GET', 'POST'])
def levels(TEAM, TOPIC):
    global CURR_STATS
    if request.method == 'GET':
        # UPDATE AGAIN JUST TO KEEP THINGS IN SYNC UNTIL NOT EVERYTHING IS VERIFIED.
        CURR_STATS['TEAM'], CURR_STATS['TOPIC'] = TEAM, TOPIC
        update_topics_used(TEAM, TOPIC)
        data = {
                'TEAM':CURR_STATS['TEAM'],
                'TOPIC':CURR_STATS['TOPIC'],
                'NEXTP':url_for('question', TEAM=TEAM, TOPIC=TOPIC, LEVEL=-1),
                'AJAXPOST_URL':url_for('levels', TEAM=TEAM, TOPIC=TOPIC)
                }
        if TOPIC in ('AV','EQ'):
            return render_template("level_0.html", data=data)
        else:
            return render_template("levels.html", data=data)
    else:
        DOUBLE_HALF = request.form['DOUBLE_HALF']
        print("DOUBLE_HALF:",DOUBLE_HALF)
        CURR_STATS['DOUBLE_HALF']=DOUBLE_HALF
        return "UPDATED"

def get_question_data(TEAM, TOPIC, LEVEL):
    if TOPIC in ('AV','EQ') or (TOPIC == 'GK' and LEVEL == '3'):
        # GET APPROPRIATE QUE FILE PATH (I KNOW IT MESSY, AND NON-PYTHONIC)
        if TOPIC == 'GK':
            path = os.path.join(os.getcwd(),'app','static','questions',TEAM, TOPIC,'DATA.txt')
        else:
            path = os.path.join(os.getcwd(),'app','static','questions','ALTER',TOPIC,'DATA.txt')
        with open(path, 'r') as f:
            raw = f.read().strip()
        raw = raw.split("\n")
        # GET APPROPRIATE MEDIA PATH
        MEDIA, TYPE = None, None
        if TOPIC == 'AV':
            text_data = [eval(i.strip()) for i in raw][ord(TEAM)-65]
            MEDIA, TYPE = url_for('static', filename="questions/ALTER/AV/video/{0}".format(text_data[1])), 'VID'
        elif TOPIC == 'EQ':
            text_data = [eval(i.strip()) for i in raw][ord(TEAM)-65]
            MEDIA, TYPE = url_for('static', filename="questions/ALTER/EQ/images/{0}".format(text_data[1])), 'IMG'
        elif TOPIC == 'GK':
            text_data = [eval(i.strip()) for i in raw][int(LEVEL)-1]
            MEDIA, TYPE = url_for('static', filename="questions/{0}/GK/{1}".format(TEAM, text_data[1])), 'IMG'
        data = {
                'QUE':text_data[0],
                'MEDIA':MEDIA,
                'TYPE':TYPE,
                'ANS':text_data[2]
                }
        #print(data)
        return data
    else:
        path = os.path.join(os.getcwd(),'app','static','questions',TEAM, TOPIC,'DATA.txt')
        print(path)
        with open(path, 'r') as f:
            raw = f.read().strip()
        raw = raw.split("\n")
        text_data = [eval(i.strip()) for i in raw][int(LEVEL)-1]
        data = {
                'QUE':text_data[0],
                'OPT1':text_data[1],
                'OPT2':text_data[2],
                'OPT3':text_data[3],
                'OPT4':text_data[4],
                'ANS':text_data[5]
                }
        #print(data)
        return data

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

    print(TEAM)
    print(TEAM_STATS[TEAM])
    ##########################

    data = {
            'TEAM':CURR_STATS['TEAM'],
            'TOPIC':CURR_STATS['TOPIC'],
            'LEVEL':CURR_STATS['LEVEL'],
            'CURR_SCORE':TEAM_STATS[TEAM]['SCORE'],
            'LPAT':TEAM_STATS[TEAM]['LPAT'],
            'NEXTP':NEXTP,
            'AJAXPOST_URL':url_for('topics', TEAM=TEAM),
            'DOUBLE_HALF':CURR_STATS['DOUBLE_HALF']
            }
    que_data = get_question_data(TEAM, TOPIC, LEVEL)
    data.update(que_data)

    if TOPIC in ('AV','EQ') or (TOPIC == 'GK' and LEVEL == '3'):
        return render_template("question2.html", data=data)
    else:
        return render_template("question1.html", data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
