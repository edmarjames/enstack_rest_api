from flask_restful import fields, reqparse

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