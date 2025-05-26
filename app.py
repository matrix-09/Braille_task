from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches
from utils import normalize_braille_sequence
from braille_model import BrailleBERTModel
import time
from utils import find_closest_braille_sequence, get_common_error_patterns
from werkzeug.middleware.proxy_fix import ProxyFix
app = Flask(__name__)

# Load key mapping
with open('key_map.json', 'r') as f:
    key_map = json.load(f)

# Load dictionary
with open('dictionary.txt', 'r') as f:
    dictionary = [word.strip().lower() for word in f.readlines()]

# Initialize BERT model
bert_model = BrailleBERTModel()

# Track user input history for learning
user_history = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_braille():
    data = request.json
    sequence = data.get('sequence', '')
    user_id = data.get('user_id', 'default')
    
    # Normalize the sequence
    normalized = normalize_braille_sequence(sequence)
    
    # Get the corresponding character - try exact match first
    char = key_map.get(normalized, '?')
    
    # If no exact match, try to find closest valid sequence
    if char == '?':
        closest_seq = find_closest_braille_sequence(sequence, key_map)
        if closest_seq:
            char = key_map[closest_seq]
            
            # Check common error patterns
            common_errors = get_common_error_patterns()
            if sequence in common_errors:
                char = key_map.get(common_errors[sequence], char)
    
    # Update user history
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append((sequence, normalized, char, time.time()))
    
    return jsonify({'char': char, 'was_corrected': char != key_map.get(normalized, '?')})

@app.route('/suggest', methods=['POST'])
def suggest_words():
    data = request.json
    current_word = data.get('word', '').lower()
    user_id = data.get('user_id', 'default')
    
    # Get basic suggestions based on edit distance
    basic_suggestions = get_close_matches(current_word, dictionary, n=5, cutoff=0.6)
    
    # Get BERT-based contextual suggestions
    bert_suggestions = bert_model.predict(current_word, user_history.get(user_id, []))
    
    # Combine and deduplicate suggestions
    all_suggestions = list(dict.fromkeys(basic_suggestions + bert_suggestions[:3]))
    
    return jsonify({'suggestions': all_suggestions[:5]})

@app.route('/learn', methods=['POST'])
def learn_from_correction():
    data = request.json
    original_word = data.get('original', '').lower()
    corrected_word = data.get('corrected', '').lower()
    user_id = data.get('user_id', 'default')
    
    # Update BERT model with correction
    bert_model.update_model(original_word, corrected_word, user_id)
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.run(host='0.0.0.0', port=10000)