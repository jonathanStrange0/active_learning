from flask import render_template, url_for, redirect, request
from app.models import Subject, Note, Answer, LearningSession
from datetime import datetime
import random
from app import db
from app.forms import NoteForm

def note_test():
	session = LearningSession(start_time=datetime.now())
	session.subject.append(subject_selector())
	db.session.commit()
	note_form = NoteForm()
	return(render_template('note.html', title='Add Note', note_form=note_form, session=session))

def suggest_subject():
	all_subjects = Subject.query.all()
	selection_idx = random.randint(0,len(all_subjects) - 1)
	selected_subject = all_subjects[selection_idx]
	return(selected_subject)

def verify_subject(subject):
	try:
		last_two_learning_sessions = LearningSession.query.all()[-2:]
		last_two_subjects = [last_two_learning_sessions[0].subject.all()[0], last_two_learning_sessions[1].subject.all()[0]]
		return([subject] * 2 == last_two_subjects)
	except:
		return False

def subject_selector():
	subject = suggest_subject()
	while verify_subject(subject):
		subject = suggest_subject()
	return(subject)