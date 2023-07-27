import re
import random

# Sample list of offensive words (you can add more if needed)
offensive_words = ["badword1", "badword2", "badword3"]

# Sample list of cute replacement words (you can add more if needed)
cute_words = ["rainbows", "flowers", "kittens", "cupcakes", "butterflies"]

def replace_offensive_words(sentence):
    # Tokenize the sentence
    words = sentence.split()

    # Initialize a new sentence to store the modified version
    new_sentence = []

    for word in words:
        # Check if the word is an offensive word
        if word.lower() in offensive_words:
            # Replace the offensive word with a random cute word
            cute_word = random.choice(cute_words)
            new_sentence.append(cute_word)
        else:
            # Keep the original word
            new_sentence.append(word)

    # Combine the words back into a sentence
    new_sentence = " ".join(new_sentence)

    return new_sentence

if __name__ == "__main__":
    print("Welcome to Cute Words Replacement!")
    
    while True:
        user_input = input("Enter a sentence: ")

        if user_input.lower() == 'quit':
            break

        # Replace offensive words with cute words
        modified_sentence = replace_offensive_words(user_input)

        print("Modified sentence:")
        print(modified_sentence)

        # Ask for user feedback
        feedback = input("Are there any additional offensive words? (yes/no): ").lower()

        if feedback == 'yes':
            # If the user provides additional offensive words for replacement
            word_to_replace = input("Enter the word to replace: ").lower()
            cute_word = input("Enter the cute word to replace with: ")
            
            # Add the word to the offensive_words list and its replacement to cute_words list
            offensive_words.append(word_to_replace)
            cute_words.append(cute_word)

        elif feedback == 'no':
            # If no additional offensive words, continue to the next sentence
            continue
        else:
            print("Invalid feedback. Please enter 'yes' or 'no'.")

# Save the updated lists of offensive and cute words for future runs (optional)
# You can use pickle, JSON, or other methods to save and load the lists.
