# quiz_controller.py
from flask import render_template, url_for, redirect, request, jsonify
from app.models import Subject, Note, Answer, LearningSession, Bin, Quiz, Test
from datetime import datetime
import random, re
from app import db, quiz_or_test_list

def quiz_controller(learning_session_id=None, quiz_id = None):
	if quiz_id is not None:
		print('quiz id is not none?')
		quiz = Quiz.query.filter_by(id = quiz_id)
	else:
		quiz = Quiz(correct_answers = 0)
		db.session.commit()
	print(quiz, quiz.id)
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
		bin1 = Bin.query.filter_by(bin_name = "Bin 1").first()
		questions = db.session.query(Note).join(Note.bin).filter(Note.subject == subject, Note.bin == bin1).all()
		if len(questions) >= 5: # Don't crash if there aren't 5 questions to ask...
			quiz_or_test_list = random.sample(questions, k=5)
		else:
			quiz_or_test_list = random.sample(questions, k=len(questions))

		current_question = quiz_or_test_list.pop()
	print(current_question, last_question)
	return(render_template('quiz.html', learning_session=learning_session,\
										 subject=subject, \
										 question = current_question, \
										 last_question=last_question, \
										 quiz = quiz))


def test_controller(bin_number=1, test_id=None):
	if test_id:
		test = Test.query.filter_by(id = test_id)
	else:
		test = Test()
	fc_bin = Bin.query.filter_by(bin_name = 'Bin ' + str(bin_number)).first()
	print(fc_bin)
	last_question = False
	global quiz_or_test_list
	if len(quiz_or_test_list):
		current_question = quiz_or_test_list.pop()
		if len(quiz_or_test_list) == 0:
			# this is the last question of the quiz
			last_question = True
	elif not last_question:
		# this query will get all the notes of a particular bin 
		questions = db.session.query(Note).join(Note.bin).filter(Note.bin == fc_bin).all()
		if len(questions):
			quiz_or_test_list = random.sample(questions, k=len(questions))
		current_question = quiz_or_test_list.pop()

	print(current_question, last_question)
	return(render_template('test.html', bin=fc_bin,\
										 question = current_question, \
										 last_question=last_question, \
										 test = test))


def record_quiz_answer(correct):
	"""
		if the quiz question is answered correctly, move it into the next bin up

		otherwise, move it back to bin 1

		Also keep track of if this is the last question in the quiz or not.
		If it is, return the quiz_results.html template instead of another question.
	"""
	last_question = request.args.get('last_question', type=bool)
	# print(request.args.get('last_question', type=bool))
	question_id = request.args.get('question_id', type=int)
	session_id = request.args.get('session_id', type=int)
	note =  Note.query.filter_by(id=question_id).first()
	bin_name = note.bin.bin_name
	quiz = Quiz.query.filter_by(id = request.args.get('quiz_id', type=int)).first()
	if correct:
		# save new answer to answers for this note
		# move question to next bin up
		move_note_bin(note, up=True)
		quiz.correct_answers += 1
		print(quiz)
		db.session.commit()
	else:
		# move question to bin 1
		move_note_bin(note, up=False)

	if last_question:
		# print('last question = ',last_question)
		return jsonify(result=url_for('quiz_results', learning_session_id = session_id, quiz = quiz))
	else:
		# print('last question = False',last_question)
		return jsonify(result=url_for('quiz', learning_session_id = session_id, quiz = quiz))

def record_test_answer(correct, test):
	"""
		if the test question is answered correctly, move it into the next bin up

		otherwise, move it back to bin 1

		Also keep track of if this is the last question in the test or not.
		If it is, return the quiz_results.html template instead of another question.
	"""
	last_question = request.args.get('last_question', type=bool)
	question_id = request.args.get('question_id', type=int)
	note =  Note.query.filter_by(id=question_id).first()
	fc_bin = note.bin

	if correct:
		# save new answer to answers for this note
		# move question to next bin up
		move_note_bin(note, up=True)
		test.correct_answers += 1
		db.session.commit()
	else:
		# move question to bin 1
		move_note_bin(note, up=False)

	if last_question:
		# print('last question = ',last_question)
		return jsonify(result=url_for('test_results', bin_id = fc_bin.id, test_id = test.id))
	else:
		# print('last question = False',last_question)
		return jsonify(result=url_for('test', bin_id = fc_bin.id, test_id = test.id))


def move_note_bin(note, up=True):
	"""
		give a note, and if the question needs to be moved into the next 
		bin or not, remove the note from it's current bin, and place it 
		in the next bin.

		if the question was answered incorrectly (up = False), drop the
		note down into bin 1 for further study.
	"""
	bin_name = note.bin.bin_name
	bin_num = int(re.findall(r'(\d+)', bin_name)[0])

	if up: 
		if bin_num == 1:
			bin_1 = note.bin
			bin_1.notes.remove(note)
			bin_2 = Bin.query.filter_by(bin_name = 'Bin 2').first()
			if bin_2:
				bin_2.notes.append(note)
			else:
				bin_2 = Bin(bin_name='Bin 2')
				bin_2.notes.append(note)
		elif bin_num == 2:
			bin_2 = note.bin
			bin_2.notes.remove(note)
			bin_3 = Bin.query.filter_by(bin_name = 'Bin 2').first()
			if bin_3:
				bin_3.notes.append(note)
			else:
				bin_3 = Bin(bin_name='Bin 3')
				bin_3.append(note)
		elif bin_num == 3:
			bin_3 = note.bin
			bin_3.notes.remove(note)
			bin_4 = Bin.query.filter_by(bin_name = 'Bin 4').first()
			if bin_4:
				bin_4.notes.append(note)
			else:
				bin_4 = Bin(bin_name='Bin 4')
				bin_4.append(note)
	else:
		any_bin = note.bin
		any_bin.notes.remove(note)
		bin_1 = Bin.query.filter_by(bin_name = 'Bin 1').first()
		bin_1.notes.append(note)

	db.session.commit()


