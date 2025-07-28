import os
import tempfile
from flask import Flask, render_template, request, jsonify
import instaloader
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Sabit sistem prompt'u. UI'dan alınmayacak.
SYSTEM_PROMPT = "You are a helpful assistant. Generate a friendly and concise reply to the following comment. The reply must be a maximum of 30 words."

def generate_reply_with_google_api(comment_text):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found.")


    url = "https://generativelanguage.googleapis.com/v1beta/models/gemma-3-1b-it:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }

    prompt_text = f"{system_prompt}\n###\nComment: \"{comment_text}\"\n###\nReply:"

    data = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"maxOutputTokens": 40} # Kelime sayısı için token'ı biraz daha yüksek tutalım
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

    if not all([file, username, shortcode]):
        return jsonify({'error': 'Username, shortcode, and a session file are required.'}), 400

    temp_dir = tempfile.gettempdir()
    temp_filepath = os.path.join(temp_dir, secure_filename(file.filename))
    file.save(temp_filepath)

    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(username, temp_filepath)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = list(post.get_comments())

        results = []
        for comment in comments:
            reply_text = generate_reply_with_google_api(comment.text)

            results.append({
                'comment_id': comment.id,
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

@app.route('/reply', methods=['POST'])
def reply():
    data = request.json
    comment_id = data.get('comment_id')
    reply_text = data.get('reply_text')
    access_token = os.getenv('META_GRAPH_API_TOKEN')

    if not all([comment_id, reply_text, access_token]):
        return jsonify({'error': 'Comment ID, reply text, and Meta API token are required.'}), 400

    url = f"https://graph.facebook.com/v20.0/{comment_id}/replies"
    params = {'message': reply_text, 'access_token': access_token}

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        return jsonify({'status': 'success', 'message': 'Reply sent successfully.'})
    except requests.exceptions.RequestException as e:
        error_info = e.response.json() if e.response else str(e)
        return jsonify({'status': 'error', 'message': error_info}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
