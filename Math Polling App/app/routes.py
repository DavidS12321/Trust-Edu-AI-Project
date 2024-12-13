from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .utils import generate_question, adjust_difficulty
import random

main_bp = Blueprint('main', __name__)

# Shared state
@main_bp.before_request
def before_request():

    # initialize session variables
    if 'correct_count' not in session:
        session['correct_count'] = 0
        session['total_count'] = 0
        session['current_difficulty'] = 'easy'
        session['question_count'] = 0
        session['feedback'] = "" 

@main_bp.route('/', methods=['GET', 'POST'])
def home():

    # show results after 10 questions
    if session.get('question_count', 0) >= 10:
        return redirect(url_for('main.results'))

    # Adjust difficulty based on performance before generating a new question
    session['current_difficulty'] = adjust_difficulty(
        session['current_difficulty'], session['correct_count'], session['total_count']
    )

    if request.method == 'POST':

        user_answer = request.form.get('selected-answer')

        correct_answer = session.get('correct_answer')

        correct = (user_answer == correct_answer)

        if correct:
            session['correct_count'] += 1

        session['feedback'] = "Correct!" if correct else "Try again!"

        session['total_count'] += 1
        session['question_count'] += 1 

        print("Question count:", session.get('question_count'))
        print("Correct count:", session.get('correct_count'))
        print("Total count:", session.get('total_count'))


        # generate next question
        return redirect(url_for('main.home'))

    question, correct_answer, options = generate_question(session['current_difficulty'])
    if not question:
        return "Error generating question", 500

    session['correct_answer'] = correct_answer

    # shuffle options to have more variety
    random.shuffle(options)

    return render_template('index.html', question=question, options=options, feedback=session.get('feedback', ''), correct_answer=correct_answer)

@main_bp.route('/submit', methods=['POST'])
def submit_answer():
    user_answer = request.form['selected_answer']
    correct_answer = request.form['correct_answer']

    session['total_count'] += 1
    if user_answer == correct_answer:
        session['correct_count'] += 1

    session['current_difficulty'] = adjust_difficulty(
        session['current_difficulty'], session['correct_count'], session['total_count']
    )

    return redirect(url_for('main.home'))

@main_bp.route('/results')
def results():
    # correct and total counts from the session
    correct_count = session.get('correct_count', 0)
    total_count = session.get('question_count', 0)
    
    if total_count > 0:
        percentage = (correct_count / total_count) * 100
    else:
        percentage = 0

    return render_template('results.html', correct_count=correct_count, total_count=total_count, percentage=percentage)