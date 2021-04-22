from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('cooker', required=True)
parser.add_argument('title', required=True)
parser.add_argument('ingredients', required=True)
parser.add_argument('work_size', required=True)
parser.add_argument('category', required=True, type=int)