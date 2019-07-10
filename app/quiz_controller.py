# quiz_controller.py
from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db, quiz_or_test_list

def quiz_controller(learning_session_id=None):
	learning_session = LearningSession.query.filter_by(id = learning_session_id).first()
	subject = learning_session.subject.first()
	last_question = False
	global quiz_or_test_list
	if len(quiz_or_test_list):
		current_question = quiz_or_test_list.pop()
		if len(quiz_or_test_list) == 0:
			# this is the last question of the quiz
			last_question = True
	elif not last_question:
		# this query will get the notes of a particular subject in bin_1
		quiz_or_test_list = random.choices(db.session.query(Note).\
															join(Note.bin_1).\
															filter(Note.subject == subject).all(), k=5)
		current_question = quiz_or_test_list.pop()
	print(current_question, last_question)
	return(render_template('quiz.html', learning_session=learning_session,\
										 subject=subject, \
										 question = current_question, \
										 last_question=last_question))

