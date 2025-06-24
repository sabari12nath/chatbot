import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="keras")

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import string
import re

# Load intents from JSON file
json_path = os.path.join(os.path.dirname(__file__), "full_banking_intents.json")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
intents = data["intents"]

# --- Improved Preprocessing: Lowercase, strip, remove punctuation, collapse whitespace, and remove stopwords ---
# Use the same preprocessing for both training and inference (no stopword removal, just lowercase, punctuation removal, whitespace normalization).
def preprocess_text(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text

all_patterns = [preprocess_text(p) for intent in intents for p in intent["patterns"]]
all_tags = [intent["tag"] for intent in intents for _ in intent["patterns"]]

# --- Tokenization and Padding ---
tokenizer = Tokenizer(num_words=2000, oov_token="<OOV>")
tokenizer.fit_on_texts(all_patterns)
X = tokenizer.texts_to_sequences(all_patterns)
X = pad_sequences(X, maxlen=15)
tag_set = sorted(set(all_tags))
tag_to_index = {tag: idx for idx, tag in enumerate(tag_set)}
index_to_tag = {idx: tag for tag, idx in tag_to_index.items()}
y = np.array([tag_to_index[tag] for tag in all_tags])

# --- Model: Add Embedding and more neurons for better learning ---
model = Sequential([
    Embedding(input_dim=2000, output_dim=16, input_length=15),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(len(tag_to_index), activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=300, verbose=0)
model.save("astra_banking_model.h5")

# --- Ensure tag_to_response is correct and responses are mapped properly ---
tag_to_response = {}
for intent in intents:
    tag_to_response[intent["tag"].lower()] = intent["response"]

class AstraBotModel:
    def __init__(self):
        self.tokenizer = tokenizer
        self.model = model
        self.tag_to_index = tag_to_index
        self.index_to_tag = index_to_tag
        self.tag_to_response = tag_to_response

    def predict_intent(self, message):
        processed = preprocess_text(message)
        seq = self.tokenizer.texts_to_sequences([processed])
        padded = pad_sequences(seq, maxlen=15)
        pred = self.model.predict(padded, verbose=0)
        tag_idx = int(np.argmax(pred))
        confidence = float(np.max(pred))
        # Lower threshold to 0.15 for better matching on short/ambiguous queries
        if confidence < 0.15:
            return None
        return self.index_to_tag[tag_idx].lower()

    def get_response(self, intent):
        if intent is None:
            return "Sorry, I didn't understand that. Could you rephrase?"
        return self.tag_to_response.get(intent.lower(), "Sorry, I didn't understand that.")

astra_bot = AstraBotModel()

def predict_intent(message):
    return astra_bot.predict_intent(message)

def get_response(intent):
    return astra_bot.get_response(intent)

def train_model(epochs=300):
    model.fit(X, y, epochs=epochs, verbose=1)
    print("Model training complete.")

if __name__ == '__main__':
    print("Training the model with current intents data...")
    train_model()
