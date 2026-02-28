from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Review Management System is Live 🚀"

if __name__ == "__main__":
    app.run()
    