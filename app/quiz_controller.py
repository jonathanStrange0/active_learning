# quiz_controller.py
from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db

def quiz_controller(learning_session_id=None):
	session = LearningSession.query.filter_by(id = learning_session_id).first()
	subject = session.subject.first().subject

	# this query will get the notes of a particular subject in bin_1
	# db.session.query(Note).join(Note.bin_1).filter(Note.subject == subject).all()

	return(render_template('quiz.html', session=session, subject=subject))
