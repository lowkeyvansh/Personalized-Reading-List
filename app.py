from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['reading_list']
collection = db['books']

@app.route('/books', methods=['POST'])
def add_book():
    book = request.json
    collection.insert_one(book)
    return jsonify({'msg': 'Book added to reading list'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = list(collection.find({}, {'_id': 0}))
    return jsonify(books)

@app.route('/books/<title>', methods=['PUT'])
def mark_as_read(title):
    collection.update_one({'title': title}, {'$set': {'status': 'Read'}})
    return jsonify({'msg': 'Book marked as read'}), 200

@app.route('/books/<title>', methods=['DELETE'])
def delete_book(title):
    collection.delete_one({'title': title})
    return jsonify({'msg': 'Book deleted from reading list'}), 200

if __name__ == '__main__':
    app.run(debug=True)
