import json
import random
import nltk
from nltk.tokenize import word_tokenize
import re

with open('intents.json') as file:
    intents = json.load(file)

# Preprocess the intents
nltk.download('punkt')  # Download the tokenizer
processed_intents = [
    {
        "intent": intent["intent"],
        "patterns": [word.lower() for word in word_tokenize(" ".join(intent["patterns"]))]
    }
    for intent in intents
]

# Define a function to recognize intents
def recognize_intent(user_input):
    user_input = user_input.lower()
    matched_intents = []
    for intent in processed_intents:
        for pattern in intent["patterns"]:
            escaped_pattern = re.escape(pattern)
            if re.search(r'\b{}\b'.format(escaped_pattern), user_input):
                matched_intents.append(intent["intent"])
    return matched_intents

# Define a function to generate responses based on intents
def generate_response(user_input):
    matched_intents = recognize_intent(user_input)
    if matched_intents:
        intent = random.choice(matched_intents)
        for intent_data in intents:
            if intent_data["intent"] == intent:
                responses = intent_data["responses"]
                return random.choice(responses)
    return "I'm sorry, I didn't understand that."

# Chatbot interaction loop
while True:
    user_input = input("User: ")
    response = generate_response(user_input)
    print("Chatbot:", response)
