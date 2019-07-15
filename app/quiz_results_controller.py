# quiz_results_controller.py
from flask import render_template, url_for, redirect, request, jsonify
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
from app import db, quiz_or_test_list

def quiz_results_controller(learning_session_id):
	session = LearningSession.query.filter_by(id = learning_session_id).first()
	correct_answers = 'This should actually be a number pulled from Quiz object'
	return(render_template('quiz_results.html', title='Quiz Resluts', session=session, correct_answers=correct_answers))

