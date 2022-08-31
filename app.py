from surveys import satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash, url_for, session
from flask_debugtoolbar import DebugToolbarExtension

# key names will　be stored in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
# RESPONSES_KEY = "responses"


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
# we set the methods to post because we need to send session data
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
        question = questions[question_num].question
        answers = questions[question_num].choices
        # track_num += 1
        return render_template('questions.html', question = question, answers = answers)

    elif question_num != track_num:
        flash('You are trying to access an invalid question')
        return redirect(url_for('show_question', question_num = track_num))


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