from flask import Flask, request, jsonify
from scraper import scrape_behance_projects

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Behance Scraper API running."

@app.route("/scrape-behance", methods=["GET"])
def scrape():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    try:
        data = scrape_behance_projects(username)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
