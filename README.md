# Email Classification System

This project implements an email classification system that can categorize emails into different classes using sentence embeddings. 
The original system was modified to load classification categories from a file rather than using hardcoded values, and an API endpoint was added to allow dynamic addition of new classification categories.

### Key Changes

1. Dynamic Class Loading: Classification categories are now loaded from a JSON file rather than being hardcoded in the code.
2. API for Adding Classes: Added an endpoint that allows users to add new classification categories via API calls.
3. Real-time Updates: Modified the classification system to reload classes with each request, ensuring it always uses the most current set of classes.

### Modified Files

- analyze.py: Added file-based class loading and improved embedding functions
- app.py: Added a new API endpoint for adding classification categories
- classes.json: New file that stores available classification categories


## Setup and Installation

#### Clone the repository
git clone https://github.com/Matt-Baxter/mlops_sentiment_lab.git

cd mlops_sentiment_lab

#### Create and activate virtual environment
python -m venv venv

source venv/bin/activate

#### Install dependencies
pip install -r requirements.txt

#### Run the server
python app.py

## Usage Examples

#### Adding a New Classification Category
curl -X POST -H "Content-Type: application/json" \
  -d '{"class_name": "Technology"}' \
  http://localhost:3000/api/v1/add_class/

#### Classifying Text
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "The new software release includes AI features"}' \
  http://localhost:3000/api/v1/classify/

#### Using the Web Interface

You can also access the classification endpoint through a browser:
copy: http://localhost:3000/api/v1/classify-email/?text="Please submit your assignment by Friday"


#### Notes
- The classification system uses sentence embeddings to determine the similarity between input text and class names
- New classes are immediately available for classification after being added via the API
- For a production environment, the system would benefit from training data for each class to improve accuracy


This project was created as part of MLOps Homework 2, which required modifying an existing email classification system to use file-based class storage and allow dynamic addition of classification categories.