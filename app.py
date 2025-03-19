from flask import Flask, request, jsonify, render_template
import json
from analyze import get_sentiment, compute_embeddings, classify_email
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    print("Home page")
    return render_template('index.html')


@app.route("/api/v1/sentiment-analysis/", methods=['POST'])
def analysis():
    if request.is_json:
        data = request.get_json()
        sentiment = get_sentiment(data['text'])
        return jsonify({"message": "Data received", "data": data, "sentiment": sentiment}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/valid-embeddings/", methods=['GET'])
def valid_embeddings():
    embeddings = compute_embeddings()
    formatted_embeddings = []
    for text, vector in embeddings:
        formatted_embeddings.append({
            "text": text,
            "vector": vector.tolist() if hasattr(vector, 'tolist') else vector
        })
    embeddings = formatted_embeddings
    return jsonify({"message": "Valid embeddings fetched", "embeddings": embeddings}), 200


@app.route("/api/v1/classify/", methods=['POST'])
def classify():
    if request.is_json:
        data = request.get_json()
        text = data['text']
        classifications = classify_email(text)
        return jsonify({"message": "Email classified", "classifications": classifications}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/classify-email/", methods=['GET'])
def classify_with_get():
    text = request.args.get('text')
    classifications = classify_email(text)
    return jsonify({"message": "Email classified", "classifications": classifications}), 200
    
# New code:    
# Adding a new endpoint
@app.get("/sentiment/")
def sentiment(text):
    return get_sentiment(text)
    

# New code:    
# Allow users to add new classes via an API
@app.route('/api/v1/add_class/', methods=['POST']) 
def add_class():
    # Get data from request
    data = request.json
    if not data or 'class_name' not in data:
        return jsonify({"error": "No class name provided"}), 400
    
    new_class = data['class_name']
    
    # Load current classes
    try:
        with open('classes.json', 'r') as f:
            classes = json.load(f)
    except FileNotFoundError:
        classes = ["Work", "Sports", "Food"]
    
    # Add the new class if it doesn't exist
    if new_class in classes:
        return jsonify({"message": f"Class '{new_class}' already exists", 
                       "classes": classes}), 200
    
    classes.append(new_class)
    
    # Write updated classes back to file
    with open('classes.json', 'w') as f:
        json.dump(classes, f)
    
    return jsonify({"message": f"Class '{new_class}' added successfully", 
                   "classes": classes}), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)