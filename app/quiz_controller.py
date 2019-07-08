# quiz_controller.py
from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db

def quiz_controller(learning_session_id=None):
	session = LearningSession.query.filter_by(id = learning_session_id).first()


	return(render_template('quiz.html', session=session))
