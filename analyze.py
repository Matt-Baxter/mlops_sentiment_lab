from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

sentiment_pipeline = pipeline("sentiment-analysis")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# New code:
import json

def load_classes():
    try:
        with open('classes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default classes if file doesn't exist
        default_classes = ["Work", "Sports", "Food"]
        with open('classes.json', 'w') as f:
            json.dump(default_classes, f)
        return default_classes

# Load classes from file
EMAIL_CLASSES = load_classes()

def get_sentiment(text):
    response = sentiment_pipeline(text)
    return response

# Modified code:
def compute_embeddings(classes = None):
    if classes is None:
        classes = load_classes()
    embeddings = model.encode(classes)
    return zip(classes, embeddings)
    
def classify_email(text):
    # Encode the input text
    text_embedding = model.encode([text])[0]
    
    # Get current classes (reloading to ensure latest classes are used)
    current_classes = load_classes() # new line of code added
    
    # Calculate embeddings and continue with classification
    class_embeddings = compute_embeddings(current_classes)
    
    # Calculate distances and return results
    results = []
    for class_name, class_embedding in class_embeddings:
        # Compute cosine similarity between text and class embedding
        similarity = np.dot(text_embedding, class_embedding) / (np.linalg.norm(text_embedding) * np.linalg.norm(class_embedding))
        results.append({
            "class": class_name,
            "similarity": float(similarity)  # Convert tensor to float for JSON serialization
        })
    
    # Sort by similarity score descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results