from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample dataset: Positive and negative movie reviews
reviews = [
    ("I loved the movie. It was great!", "positive"),
    ("The movie was terrible. I hated it.", "negative"),
    ("The acting was superb!", "positive"),
    ("The plot was confusing.", "negative")
]

# Split data into features (review text) and labels (sentiment)
X, y = zip(*reviews)

# Vectorize the reviews using a bag-of-words model
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_vectorized, y)

def predict_sentiment(review):
    review_vectorized = vectorizer.transform([review])
    prediction = classifier.predict(review_vectorized)
    return prediction[0]

if __name__ == "__main__":
    print("Welcome to Sentiment Analysis!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("Enter your review: ")

        if user_input.lower() == 'quit':
            break

        # Make prediction
        prediction = predict_sentiment(user_input)
        print(f"Predicted sentiment: {prediction}")

        # Ask for feedback and update the classifier
        feedback = input("Was the prediction accurate? (yes/no): ").lower()

        if feedback == 'yes':
            # If the prediction was accurate, continue to the next review
            continue
        elif feedback == 'no':
            # If the prediction was incorrect, ask for the correct sentiment
            correct_sentiment = input("Enter the correct sentiment (positive/negative): ").lower()

            # Add the corrected review to the training dataset
            reviews.append((user_input, correct_sentiment))
            X, y = zip(*reviews)

            # Retrain the classifier with the updated dataset
            X_vectorized = vectorizer.fit_transform(X)
            classifier.fit(X_vectorized, y)
            print("Thank you for the feedback. The classifier has been updated.")
        else:
            print("Invalid feedback. Please enter 'yes' or 'no'.")
