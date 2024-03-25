from flask import *
import requests
import uuid
from flask_session import Session
import database
import datetime
import main

def makeid():
    userid = str(uuid.uuid1())
    return userid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/', methods = ('GET','POST'))
def index():
    session['userid'] = makeid()
    return render_template('index.html')

@app.route('/true', methods = ('GET','POST'))
def home():
    uid = session.get('userid')
    # get the current time
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    # create a user object and submit it to the database
    user1 = database.createuser(time, uid)
    database.upsert_item(database.ucontainer, user1)
    if request.method == 'POST':
        # get question
        question = request.form['question']
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        # made a unique id for both question and answer
        qid = makeid()
        aid = makeid()
        # query the CHAT-GPT API
        answer = main.query(question)
        # make a question object
        question1 = database.createquestion(question, uid, time, qid)
        # create it in the database
        database.upsert_item(database.qcontainer, question1)
        # make an answer object
        answer1 = database.createanswer(answer, uid, time, aid)
        # create it in the database
        database.upsert_item(database.acontainer, answer1)
        # read all item from the qcontainer and acontainer
        qdb = database.read_all(database.qcontainer, uid)
        adb = database.read_all(database.acontainer, uid)
        length = len(qdb)
        return render_template('intro.html', qdb= qdb, adb = adb, length = length)
    return render_template('intro.html')

@app.route('/false', methods = ('GET','POST'))
def false():
    if request.method == 'POST':
        session['userid'] = None
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
