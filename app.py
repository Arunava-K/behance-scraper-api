from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def scrape_behance_projects(username):
    url = f"https://www.behance.net/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch Behance page"}, response.status_code

        soup = BeautifulSoup(response.text, "html.parser")
        projects = []

        for a in soup.select('a.qa-project-cover-link')[:6]:  # Limit to 6 projects
            project_url = "https://www.behance.net" + a.get('href')
            title = a.get('title', 'Untitled')
            img = a.select_one('img')
            image_url = img.get('src') if img else None

            projects.append({
                "title": title,
                "url": project_url,
                "image": image_url
            })

        return projects

    except Exception as e:
        return {"error": str(e)}

@app.route('/scrape')
def scrape():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "No username provided"}), 400

    print("Username received:", username)
    result = scrape_behance_projects(username)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
