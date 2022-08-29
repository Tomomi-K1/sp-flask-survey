from surveys import satisfaction_survey
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension

responses = []

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc-ze'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_survey_info():
    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template('survey-main.html', title = title, instruction = instruction)


questions = satisfaction_survey.questions
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
    responses.append(request.args.get('responses'))
    if track_num == len(questions):
        return render_template ('thankyou.html')
    else:
        track_num += 1
        return redirect (url_for('show_question', question_num = track_num))