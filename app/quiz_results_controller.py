# quiz_results_controller.py
from flask import render_template, url_for, redirect, request, jsonify
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
from app import db, quiz_or_test_list

def quiz_results_controller(learning_session_id):
	session = LearningSession.query.filter_by(id = learning_session_id).first()
	correct_answers = 'This should actually be a number pulled from Quiz object'
	return(render_template('quiz_results.html', title='Quiz Resluts', session=session, correct_answers=correct_answers))

def record_quiz_answer(correct):
	last_question = request.args.get('last_question', type=bool)
	# print(request.args.get('last_question', type=bool))
	question_id = request.args.get('question_id', type=int)
	session_id = request.args.get('session_id', type=int)
	note =  Note.query.filter_by(id=question_id).first()

	# if correct:
	# 	# save new answer to answers for this note
	# 	# move question to next bin up
	# else:
	# 	# move question to bin 1


	if last_question:
		# print('last question = ',last_question)
		return jsonify(result=url_for('quiz_results', learning_session_id = session_id))
	else:
		# print('last question = False',last_question)
		return jsonify(result=url_for('quiz', learning_session_id = session_id))