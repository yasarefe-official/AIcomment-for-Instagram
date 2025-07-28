import os
import tempfile
from flask import Flask, render_template, request, jsonify
import instaloader
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

MAIN_SYSTEM_PROMPT = "You are a helpful social media assistant. Your goal is to generate a friendly and concise reply to the following comment. The reply must be a maximum of 30 words and must adhere to the user's instructions."

def generate_reply_with_google_api(user_system_prompt, comment_text):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found.")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemma-2b-it:generateContent"
    headers = {'Content-Type': 'application/json', 'X-goog-api-key': api_key}

    final_prompt = (
        f"{MAIN_SYSTEM_PROMPT}\n\n"
        f"User's instructions for tone and style: '{user_system_prompt}'\n\n"
        f"###\nComment: \"{comment_text}\"\n###\nReply:"
    )
    data = {
        "contents": [{"parts": [{"text": final_prompt}]}],
        "generationConfig": {"maxOutputTokens": 40}
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except (KeyError, IndexError):
        return "Could not generate a reply."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'session_file' not in request.files:
        return jsonify({'error': 'No session file part.'}), 400

    file = request.files['session_file']
    username = request.form.get('username')
    shortcode = request.form.get('shortcode')
    user_system_prompt = request.form.get('user_system_prompt')

    if not all([file, username, shortcode, user_system_prompt]):
        return jsonify({'error': 'All fields and a session file are required.'}), 400

    temp_dir = tempfile.gettempdir()
    temp_filepath = os.path.join(temp_dir, secure_filename(file.filename))
    file.save(temp_filepath)

    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(username, temp_filepath)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = list(post.get_comments())

        if not comments:
            return jsonify({'results': [], 'message': 'No comments found for this post.'})

        results = []
        for comment in comments:
            reply_text = generate_reply_with_google_api(user_system_prompt, comment.text)

            results.append({
                'comment_text': comment.text,
                'owner': comment.owner.username,
                'suggested_reply': reply_text
            })

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
