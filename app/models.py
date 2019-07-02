from app import db

class LearningSession(db.Model):
    __tablename__ = 'learning_session'
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    subject = db.relationship('Subject', backref='learning_session', lazy='dynamic')
    notes = db.relationship('Note', backref='learning_session', lazy='dynamic')

    def __repr__(self):
        return '<Learning Session: {}>'.format(self.id)

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(64), unique = True)
    question = db.Column(db.String(128), index = True, unique = True)
    
    answer = db.relationship('Answer', backref='note', lazy='dynamic')

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    learning_session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'))

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

    note = db.relationship('Note', backref='subject', lazy='dynamic')
    learning_session_id = db.Column(db.Integer, db.ForeignKey('learning_session.id'))

    def __repr__(self):
        return '<Subject: {}>'.format(self.subject)

