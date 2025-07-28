import os
from flask import Flask, render_template, request, jsonify
import instaloader
import requests

app = Flask(__name__)

def generate_reply_with_google_api(system_prompt, comment_text):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemma-2b-it:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }

    prompt_text = f"{system_prompt}\n###\nComment: \"{comment_text}\"\n###\nReply:"

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 30
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except (KeyError, IndexError) as e:
        print(f"Error parsing Google API response: {e}")
        return "Sorry, I couldn't generate a reply."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    username = data.get('username')
    shortcode = data.get('shortcode')
    system_prompt = data.get('system_prompt')

    if not all([username, shortcode, system_prompt]):
        return jsonify({'error': 'Username, shortcode, and system prompt are required.'}), 400

    try:
        L = instaloader.Instaloader()

        # Checkpoint sorununu önlemek için şifreyle giriş yapmak yerine session dosyasını kullan
        session_file = f"./{username}"
        if not os.path.exists(session_file):
            return jsonify({'error': f'Session file not found for user {username}. Please create it first.'}), 400

        L.load_session_from_file(username, session_file)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = list(post.get_comments())

        results = []
        for comment in comments:
            reply_text = generate_reply_with_google_api(system_prompt, comment.text)

            results.append({
                'comment_text': comment.text,
                'owner': comment.owner.username,
                'suggested_reply': reply_text
            })

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
