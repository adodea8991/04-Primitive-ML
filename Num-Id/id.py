import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Create a drawing canvas
class DrawingCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.setup_canvas()
        self.bind_events()
        self.drawing = False

    def setup_canvas(self):
        self.configure(bg="white", width=280, height=280)
        self.image = Image.new("L", (280, 280), "white")
        self.draw = ImageDraw.Draw(self.image)

    def bind_events(self):
        self.bind("<Button-1>", self.start_drawing)
        self.bind("<B1-Motion>", self.draw_on_canvas)
        self.bind("<ButtonRelease-1>", self.reset_drawing)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw_on_canvas(self, event):
        if self.drawing:
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            self.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=5)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill="black", width=5)
            self.last_x = event.x
            self.last_y = event.y

    def reset_drawing(self, event):
        self.drawing = False

    def clear_canvas(self):
        self.delete("all")
        self.image = Image.new("L", (280, 280), "white")
        self.draw = ImageDraw.Draw(self.image)

    def get_image_array(self):
        return np.array(self.image.resize((8, 8)))

# The main application
class HandwritingRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Recognition")
        self.canvas = DrawingCanvas(root)
        self.canvas.pack(padx=10, pady=10)
        self.recognize_button = tk.Button(root, text="Recognize", command=self.recognize_number)
        self.recognize_button.pack(pady=5)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(pady=5)
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

    def clear_canvas(self):
        self.canvas.clear_canvas()
        self.result_label.config(text="")

    def recognize_number(self):
        image_array = self.canvas.get_image_array().flatten()
        # Preprocess the image (normalize and reduce dimensions)
        image_data = image_array.reshape(1, -1) / 255.0

        # Load the digits dataset as a placeholder for the recognizer
        digits = datasets.load_digits()
        X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2)

        # Apply PCA to reduce dimensions to 64 (same as the training data)
        pca = PCA(n_components=64)
        X_train_pca = pca.fit_transform(X_train)
        image_data_pca = pca.transform(image_data)

        # Train the classifier (Support Vector Machine in this case)
        classifier = SVC(kernel='rbf', C=1.0)
        classifier.fit(X_train_pca, y_train)

        # Predict the digit from the user-drawn image
        predicted_digit = classifier.predict(image_data_pca)[0]

        self.result_label.config(text=f"Recognized digit: {predicted_digit}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HandwritingRecognitionApp(root)
    root.mainloop()
