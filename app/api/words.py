from flask import Blueprint, jsonify, request
import random

from app.data import get_words_data

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/words', methods=['GET'])
def list_words():
    words = get_words_data()
    return jsonify(words)


@api_bp.route('/words/<int:word_id>', methods=['GET'])
def get_word(word_id):
    words = get_words_data()
    word = next((w for w in words if w.get('id') == word_id), None)
    if not word:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(word)


@api_bp.route('/quiz', methods=['GET'])
def get_quiz():
    words = get_words_data()
    chosen = random.choice(words)
    chars = list(chosen['word'])
    random.shuffle(chars)
    scrambled = ''.join(chars)
    return jsonify({'id': chosen['id'], 'scrambled': scrambled, 'meaning': chosen['meaning']})


@api_bp.route('/check', methods=['POST'])
def check_answer():
    data = request.get_json() or {}
    user_answer = data.get('answer', '').strip().lower()
    word_id = data.get('id')

    words = get_words_data()
    correct = next((w for w in words if w.get('id') == word_id), None)
    if not correct:
        return jsonify({'error': 'Word not found'}), 404

    if user_answer == correct['word'].lower():
        return jsonify({'is_correct': True, 'message': 'Chính xác! Bạn thật tuyệt vời!'})
    return jsonify({'is_correct': False, 'message': f"Sai rồi. Đáp án đúng là: {correct['word']}"})
