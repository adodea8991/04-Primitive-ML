import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier

# Sample dataset: Fake and real news headlines (replace this with your actual data)
headlines = [
    ("New research shows that coffee is good for your health", 0),   # Real news (0)
    ("Aliens have landed on Earth", 1),                              # Fake news (1)
    ("Study finds link between vaccines and autism", 0),             # Real news (0)
    ("President signs new healthcare bill", 0),                     # Real news (0)
]

# Split data into features (headline text) and labels (0 for real, 1 for fake)
X, y = zip(*headlines)

# Vectorize the headlines using TfidfVectorizer
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train the PassiveAggressiveClassifier
classifier = PassiveAggressiveClassifier()
classifier.fit(X_vectorized, y)

def predict_fake_news(headline):
    headline_vectorized = vectorizer.transform([headline])
    prediction = classifier.predict(headline_vectorized)
    return prediction[0]

def update_classifier(headline, feedback):
    feedback_label = 1 if feedback.lower() == 'fake' else 0
    new_data = (headline, feedback_label)

    global X, y
    X = np.append(X, headline)
    y = np.append(y, feedback_label)

    X_vectorized = vectorizer.transform(X)
    classifier.partial_fit(X_vectorized, y)

if __name__ == "__main__":
    print("Welcome to Fake News Detector!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("Enter a headline: ")

        if user_input.lower() == 'quit':
            break

        # Make prediction
        prediction = predict_fake_news(user_input)
        print(f"Predicted: {'Fake' if prediction == 1 else 'Real'}")

        # Ask for feedback and update the classifier
        feedback = input("Was the prediction correct? (yes/no): ").lower()

        if feedback == 'yes':
            # If the prediction was correct, continue to the next headline
            continue
        elif feedback == 'no':
            # If the prediction was incorrect, ask for the correct label
            correct_label = input("Enter the correct label (Real/Fake): ")
            update_classifier(user_input, correct_label)
            print("Thank you for the feedback. The classifier has been updated.")
        else:
            print("Invalid feedback. Please enter 'yes' or 'no'.")
