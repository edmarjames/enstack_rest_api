from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LetterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(10), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    strokes = db.Column(db.Integer, nullable=False)
    vowel = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"{self.letter} - {self.value} - {self.strokes} - {self.vowel}"