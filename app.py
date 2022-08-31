from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_debugtoolbar import DebugToolbarExtension

# key names will　be stored in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"
# ？？Why do we need to do this？？

# responses = []

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc-ze'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_survey_info():
    """First page of Survey"""
    # title = survey.title
    # instruction = survey.instructions
    # Surveyの一つ一つのKeyごとに、Variableを作って、render Template にパスするより、surveyのオブジェクト自体をvariableとしてパスすることで、survey.title, survery.instructionsにtemplate上でアクセスできる。
    return render_template('survey-main.html', survey = survey)

@app.route('/session-login', methods=['POST'])
#？？？ we set the methods to post because we need to send session data？？？？
def create_session():
    session['responses'] = []
    return redirect('/questions/0')

questions = survey.questions
track_num = 0

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    global track_num
    if question_num ==len(questions):
        return render_template ('thankyou.html')
    elif question_num == track_num:
        question = questions[question_num]
        
        # track_num += 1
        return render_template('questions.html', question = question)

    elif question_num != track_num:
        flash('You are trying to access an invalid question')
        return redirect(url_for('show_question', question_num = track_num))

# springboard answer
# @app.route('/questions/<int:qid') <--URL variable name is kept short
# def show_question(qid):
#     """Display current question"""
#     responses = session.get(RESPONSES_KEY) <--getting a list that contains answers with get method of dict

#     if (responses is None): session.getで値が見当たらなかった場合、Noneとなる。 if there is no item with the key of RESPONSES_KEY
#         return redirect ('/') -->go back to homepage
    
#     if (len(response) == len(survey.questions)): --> answered all questions
#         return redirect ('/complete') 

#     if (len(response) != qid):  --> qidと返答の数が同じじゃなかったら、Userが自分で勝手に数字をタイプした可能性があるので、Redirectする
#         flash (f'invalid question id: {qid}.')
#         return redirect (f'/questions/{len(responses)}')

#     上記の内容に当てはまらない場合は、通常通り質問を表示する
#     question = questions[qid]
#         return render_template('questions.html', question = question)


@app.route('/answer')
def handle_answer():
    global track_num
    responses = session['responses']
    responses.append(request.args.get('responses'))
    session['responses'] = responses
    if track_num == len(questions):
        return render_template ('thankyou.html')
    else:
        track_num += 1
        return redirect (url_for('show_question', question_num = track_num))

# springboard answer
# @app.route('/answer')
# def handle_answer():
#     ==get answers from session and assign that to variable named responses
#     responses = session['responses']
#     ==add answer that is filled out by user to responses list
#     responses.append(request.args.get('responses'))
#     == assign newly changed(new item added) responses list to session with the key of "responses"
#     session['responses'] = responses
#     ==check if length of responses is same as the number of questions in survey
#     if (len(responses) == len(survey.questions)):
#         return redirect('/complete')
#     else:
#         return redirect (f'/questions/{len(responses)}')




# springboard answer
# @app.route('/complete')
# def completed():
#     return render_template('thankyou.html')