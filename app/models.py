from app import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func

class LearningSession(db.Model):
    __tablename__ = 'learning_session'
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    subject = db.relationship('Subject', backref='learning_session', lazy='dynamic')
    notes = db.relationship('Note', backref='learning_session', lazy='dynamic')
    quiz = db.relationship('Quiz', backref='learning_session', lazy='dynamic')

    def __repr__(self):
        return '<Learning Session: {}>'.format(self.id)

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(64), unique = True)
    question = db.Column(db.String(128), index = True, unique = True)
    creataed_on = db.Column(db.DateTime(), default=func.now())

    answer = db.relationship('Answer', backref='note', lazy='dynamic')
    subject = db.relationship('Subject', backref=backref('note', uselist=True, cascade='delete,all'))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    learning_session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'))

    bin_id = db.Column(db.Integer, db.ForeignKey('bin.id'))

    def __repr__(self):
        return '<Q: {}>'.format(self.question)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.String(128))

    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    def __repr__(self):
        return '<A: {}>'.format(self.answer)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(64), unique = True)

    # note = db.relationship('Note', backref='subject', lazy='dynamic')
    learning_session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'))

    def __repr__(self):
        return '<Subject: {}>'.format(self.subject)

class Bin(db.Model):
    __tablename__ = 'bin'
    id = db.Column(db.Integer, primary_key = True)
    bin_name = db.Column(db.String(64), index=True, unique=True)
    notes = db.relationship('Note', backref='bin', lazy='dynamic')

    test = db.relationship('Test', backref='bin', lazy='dynamic')

    def __repr__(self):
        return '<Bin: {}>'.format(self.bin_name)  

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key = True)
    correct_answers = db.Column(db.Integer)

    learning_session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'))

    def __repr__(self):
        return '<Quiz, Correct Answers: {}>'.format(self.correct_answers)

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key = True)
    correct_answers = db.Column(db.Integer)

    bin_id = db.Column(db.Integer, db.ForeignKey('bin.id'))

    def __repr__(self):
        return '<Quiz, Correct Answers: {}>'.format(self.correct_answers)