import nltk
from nltk.corpus import names
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('names')

# Sample dataset: Male and female names
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]
all_names = male_names + female_names

# Split data into features (names) and labels (gender)
X, y = zip(*all_names)

# Vectorize the names using a bag-of-words model
vectorizer = CountVectorizer(analyzer='char')
X_vectorized = vectorizer.fit_transform(X)

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_vectorized, y)

def predict_gender(name):
    name_vectorized = vectorizer.transform([name.lower()])
    prediction = classifier.predict(name_vectorized)
    return prediction[0]

if __name__ == "__main__":
    print("Welcome to Name Gender Classifier!")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("Enter a name: ")

        if user_input.lower() == 'quit':
            break

        # Make prediction
        prediction = predict_gender(user_input)
        print(f"Predicted gender: {prediction}")

        # Ask for feedback and update the classifier
        feedback = input("Was the prediction accurate? (y/n): ").lower()

        if feedback == 'y':
            # If the prediction was accurate, continue to the next name
            continue
        elif feedback == 'n':
            # If the prediction was incorrect, ask for the correct gender
            correct_gender = input("Enter the correct gender (m/f): ").lower()

            # Preprocess names and remove duplicates
            unique_names = set()
            new_names = []
            for name, gender in all_names:
                if name.lower() not in unique_names:
                    unique_names.add(name.lower())
                    new_names.append((name.lower(), gender))

            # Add the corrected name to the training dataset
            new_names.append((user_input.lower(), correct_gender))
            X, y = zip(*new_names)

            # Retrain the classifier with the updated dataset
            X_vectorized = vectorizer.transform(X)
            classifier.fit(X_vectorized, y)
            print("Thank you for the feedback. The classifier has been updated.")
        else:
            print("Invalid feedback. Please enter 'y' or 'n'.")
