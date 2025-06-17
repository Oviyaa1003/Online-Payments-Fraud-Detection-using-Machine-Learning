# flask/app.py
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open(r"c:\Users\Ponn Oviyaa\Downloads\online-payments-fraud-detection\training\payments.pkl", "rb"))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/submit', methods=["POST"])
def submit():
    if request.method == "POST":
        features = [
            float(request.form["step"]),
            float(request.form["type"]),
            float(request.form["amount"]),
            float(request.form["oldbalanceOrg"]),
            float(request.form["newbalanceOrig"]),
            float(request.form["oldbalanceDest"]),
            float(request.form["newbalanceDest"])
        ]
        final_input = np.array([features])
        result = model.predict(final_input)[0]

        if result == 1:
            prediction = "⚠️ Fraudulent Transaction Detected"
        else:
            prediction = "✅ Transaction is Legitimate"

        # Always return, and use the correct variable
        return render_template("submit.html", prediction_text=prediction)

    # If not POST, show the form again or an error
    return render_template("predict.html", prediction_text="Please submit the form.")

if __name__ == "__main__":
    app.run(debug=True)
