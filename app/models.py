from app import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(64), unique = True)
    question = db.Column(db.String(128), index = True, unique = True)
    
    answer = db.relationship('Answer', backref='note', lazy='dynamic')

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __repr__(self):
        return '<Q: {}>'.format(self.question)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    answer = db.Column(db.String(128))

    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    def __repr__(self):
        return '<A: {}>'.format(self.answer)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(64), unique = True)
    
    note = db.relationship('Note', backref='subject', lazy='dynamic')
    

    def __repr__(self):
        return '<Subject: {}>'.format(self.subject)