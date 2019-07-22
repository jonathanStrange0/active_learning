# test_results_controller.py
from flask import render_template, url_for, redirect, request, jsonify
from app.models import Subject, Note, Answer, LearningSession, Test
from datetime import datetime
from app import db, quiz_or_test_list

def test_results_controller(test_id):
	test = Test.query.filter_by(id = test_id).first()
	correct_answers = 'This should actually be a number pulled from Quiz object'
	return(render_template('test_results.html', title='Test Resluts', test=test, correct_answers=correct_answers))

