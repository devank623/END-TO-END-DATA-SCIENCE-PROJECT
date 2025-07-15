import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load data
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df = pd.read_csv(url)

# Features and target
X = df.drop("species", axis=1)
y = df["species"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
from flask import Flask, render_template, request
import numpy as np
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Create app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    inputs = [float(x) for x in request.form.values()]
    prediction = model.predict([np.array(inputs)])
    return render_template("index.html", prediction_text=f"Predicted Species: {prediction[0]}")

if __name__ == "__main__":
    app.run(debug=True)
