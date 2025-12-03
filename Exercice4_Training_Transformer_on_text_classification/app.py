from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline

app = Flask(__name__)

# Load model once at startup (no API needed)
emotion_classifier = pipeline("text-classification", 
                             model="SamLowe/roberta-base-go_emotions",
                             return_all_scores=True)

@app.route('/')
def index():
    html = """<html><body><h1>Emotion Classification</h1>
    <form action="/predict" method="post">
    <textarea name="text" rows="4" cols="50" placeholder="Enter text here..."></textarea><br>
    <button type="submit">Classify</button></form></body></html>"""
    return render_template_string(html)

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Use local pipeline instead of API
    result = emotion_classifier(text)
    return jsonify(result)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API endpoint"""
    data = request.get_json()
    text = data.get('text', '') if data else ''
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = emotion_classifier(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)