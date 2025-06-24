import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="keras")

import json

# Load intents from JSON file
JSON_PATH = os.path.join(os.path.dirname(__file__), "full_banking_intents.json")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
intents = data["intents"]

def find_response_from_json(intent_tag):
    for intent in intents:
        if intent["tag"].lower() == intent_tag.lower():
            return intent["response"]
    return "Sorry, I didn't understand that."

from model import predict_intent
from keras.models import load_model

# Load the model from the specified path
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'astra_banking_model.h5')
model = load_model(MODEL_PATH)

def main():
    print("Welcome to Astra Banking Bot! (type 'quit' to exit)")
    while True:
        message = input("You: ")
        if message.lower() == 'quit':
            print("Bot: Goodbye!")
            break
        intent = predict_intent(message)
        response = find_response_from_json(intent) if intent else "Sorry, I didn't understand that."
        print(f"Bot: {response}")

if __name__ == '__main__':
    main()
