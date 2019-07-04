# results_controller.py
from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db

def results_controller(learning_session_id = None):
	session = LearningSession.query.filter_by(id = learning_session_id).first()
	session_duration = session.end_time - session.start_time

	return(render_template('session_results.html', \
		session = session, \
		num_notes=len(session.notes.all()), \
		session_duration=session_duration))
