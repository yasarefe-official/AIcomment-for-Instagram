import os
import tempfile
from flask import Flask, render_template, request, jsonify
import instaloader
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

def generate_reply_with_google_api(system_prompt, comment_text):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemma-3-1b-it:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }

    prompt_text = f"{system_prompt}\n###\nComment: \"{comment_text}\"\n###\nReply:"

    data = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"maxOutputTokens": 30}
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
    if 'session_file' not in request.files:
        return jsonify({'error': 'No session file part in the request.'}), 400

    file = request.files['session_file']
    username = request.form.get('username')
    shortcode = request.form.get('shortcode')
    system_prompt = request.form.get('system_prompt')

    if not all([file, username, shortcode, system_prompt]):
        return jsonify({'error': 'All fields and a session file are required.'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    # Güvenli bir şekilde geçici bir dosyaya kaydet
    temp_dir = tempfile.gettempdir()
    # Dosya adının, instaloader'ın beklediği gibi kullanıcı adıyla eşleşmesi önemli olabilir.
    # Ancak load_session_from_file(username, filepath) kullandığımız için bu zorunlu değil.
    # Yine de karışıklığı önlemek için güvenli bir ad kullanalım.
    filename = secure_filename(file.filename)
    temp_filepath = os.path.join(temp_dir, filename)

    file.save(temp_filepath)

    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(username, temp_filepath)

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
    finally:
        # İşlem bittiğinde geçici dosyayı sil
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
