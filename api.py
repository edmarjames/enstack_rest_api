import random
import re

from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)

class LetterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(10), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    strokes = db.Column(db.Integer, nullable=False)
    vowel = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"{self.letter} - {self.value} - {self.strokes} - {self.vowel}"

letter_args = reqparse.RequestParser()
letter_args.add_argument("letter", type=str, required=True, help="Letter cannot be blank")
letter_args.add_argument("value", type=int, required=True, help="Value cannot be blank")
letter_args.add_argument("strokes", type=int, required=True, help="Strokes cannot be blank")
letter_args.add_argument("vowel", type=bool, required=True, help="Vowel status must be specified")

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, required=True, help="Username is required")
login_args.add_argument("password", type=str, required=True, help="Password is required")

letterFields = {
    "id": fields.Integer,
    "letter": fields.String,
    "value": fields.Integer,
    "strokes": fields.Integer,
    "vowel": fields.Boolean,
}


def fisher_yates_shuffle(letters):
    n = len(letters)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        letters[i], letters[j] = letters[j], letters[i]
    return letters


class Login(Resource):
    def post(self):
        args = login_args.parse_args()

        username = args["username"]
        password = args["password"]

        if len(username) < 4:
            abort(400, message="Username must be at least 4 characters")

        if not re.search(r"a.*b.*c", username):
            abort(400, message="Invalid username")

        if password != username[::-1]:
            abort(400, message="Password is not equal to the reverse of username")

        return jsonify({"message": "Login successful"})


class Letters(Resource):
    def get(self):
        letters = LetterModel.query.order_by(LetterModel.value).all()

        if not letters:
            abort(404, message="No letters found in the database")

        return jsonify({"letters": [letter.letter for letter in letters]})


class Letter(Resource):
    @marshal_with(letterFields)
    def get(self, letter):
        letter = LetterModel.query.filter_by(letter=letter).first()

        if not letter:
            abort(404, message="Letter not found")

        return letter


class AddLetter(Resource):
    def post(self):
        args = letter_args.parse_args()

        existing_letter = LetterModel.query.filter(LetterModel.letter.ilike(args["letter"])).first()
        if existing_letter:
            return {"status": 1}, 400

        existing_value = LetterModel.query.filter_by(value=args["value"]).first()
        if existing_value:
            return {"status": 1}, 400

        if args["value"] == args["strokes"]:
            return {"status": 1}, 400

        letter = LetterModel(
            letter=args["letter"],
            value=args["value"],
            strokes=args["strokes"],
            vowel=args["vowel"]
        )
        db.session.add(letter)
        db.session.commit()
        return {"status": 0}, 201


class ShuffleLetters(Resource):
    def get(self):
        letters = [letter.letter
                   for letter in LetterModel.query.options(load_only(LetterModel.letter)).all()]

        if not letters:
            abort(404, message="No letters found in the database")

        shuffled_letters = fisher_yates_shuffle(letters)
        return jsonify({"shuffled_letters": "".join(shuffled_letters)})


class FilterLetters(Resource):
    def get(self, val):
        letters = LetterModel.query.filter(LetterModel.value <= val).order_by(LetterModel.id).all()

        if not letters:
            abort(404, message="No letters found in the database")

        return jsonify({"letters": [letter.letter for letter in letters]})


api.add_resource(Letters, "/api/letters")
api.add_resource(Letter, "/api/letter/<string:letter>")
api.add_resource(AddLetter, "/api/letter/add")
api.add_resource(ShuffleLetters, "/api/letter/shuffle")
api.add_resource(FilterLetters, "/api/letter/filter/<int:val>")
api.add_resource(Login, "/api/login")


@app.route("/")
def home():
    return "<h1>Flask REST API</h1>"

if __name__ == "__main__":
    app.run(debug=True)