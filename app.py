from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

def load_data():
    try:
        with open("budget_data.json", "r") as f:
            return json.load(f)
    except:
        return {"balance": 0, "transaction": []}
    
def save_data(data):
    with open("budget_data.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    data = load_data()
    return render_template("index.html", balance=data["balance"], transactions=data["transactions"])

@app.route("/add", methods=["POST"])
def add():
    data = load_data()
    amount = float(request.form["amount"])
    description = request.form["description"]
    transaction_type = request.form["type"]
    if transaction_type == "income":
       data["balance"] += amount
       data["transactions"].append({"type": "income", "amount": amount, "description": description})
    elif transaction_type == "expense":
        if amount > data["balance"]:
            return redirect("/")
        data["balance"] -= amount
        data["transactions"].append({"type": "expense", "amount": amount, "description": description})

    save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    