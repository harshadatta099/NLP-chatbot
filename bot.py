import json
import random
import nltk
from nltk.tokenize import word_tokenize
import re

# Load intents from intents.json file
def load_intents(file_path):
    with open(file_path) as file:
        intents = json.load(file)
    return intents

# Preprocess the intents
def preprocess_intents(intents):
    processed_intents = []
    for intent in intents:
        processed_intent = {
            "intent": intent["intent"],
            "patterns": [word.lower() for word in word_tokenize(" ".join(intent["patterns"]))]
        }
        processed_intents.append(processed_intent)
    return processed_intents

# Download NLTK tokenizer if not already downloaded
def download_tokenizer():
    nltk.download('punkt')

# Recognize intents based on user input
def recognize_intent(user_input, processed_intents):
    user_input = user_input.lower()
    matched_intents = []
    for intent in processed_intents:
        for pattern in intent["patterns"]:
            escaped_pattern = re.escape(pattern)
            if re.search(r'\b{}\b'.format(escaped_pattern), user_input):
                matched_intents.append(intent["intent"])
    return matched_intents

# Generate response based on recognized intent
def generate_response(intent, intents):
    intent_data = next((i for i in intents if i["intent"] == intent), None)
    if intent_data:
        responses = intent_data["responses"]
        return random.choice(responses)
    return "I'm sorry, I didn't understand that."

# Chatbot interaction loop
def chat():
    intents = load_intents('intents.json')
    processed_intents = preprocess_intents(intents)
    download_tokenizer()
    
    while True:
        user_input = input("User: ")
        matched_intents = recognize_intent(user_input, processed_intents)
        if matched_intents:
            intent = random.choice(matched_intents)
            response = generate_response(intent, intents)
            print("Chatbot:", response)
        else:
            print("Chatbot: I'm sorry, I didn't understand that.")

# Run the chatbot
if __name__ == "__main__":
    chat()
