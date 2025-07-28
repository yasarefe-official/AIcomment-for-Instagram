import os
import tempfile
import json
import sys
from flask import Flask, render_template, request, Response
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
        return Response("Session file is required.", status=400)

    file = request.files['session_file']
    username = request.form.get('username')
    shortcode = request.form.get('shortcode')
    user_system_prompt = request.form.get('user_system_prompt')

    if not all([file, username, shortcode, user_system_prompt]):
        return Response("All fields and a session file are required.", status=400)

    temp_dir = tempfile.gettempdir()
    temp_filepath = os.path.join(temp_dir, secure_filename(file.filename))
    file.save(temp_filepath)

    def event_stream():
        # Helper to print to stderr for Render logs
        def log_to_stderr(message):
            print(message, file=sys.stderr)

        try:
            log_to_stderr("--- Starting event_stream ---")
            L = instaloader.Instaloader()
            L.load_session_from_file(username, temp_filepath)
            log_to_stderr(f"Session loaded for user: {username}")

            post = instaloader.Post.from_shortcode(L.context, shortcode)
            log_to_stderr(f"Post found with shortcode: {shortcode}")

            yield f"data: {json.dumps({'type': 'info', 'message': 'Fetching comments...'})}\n\n"

            comments = list(post.get_comments())
            total_comments = len(comments)
            log_to_stderr(f"Found {total_comments} comments.") # **** ÖNEMLİ LOG ****

            if total_comments == 0:
                yield f"data: {json.dumps({'type': 'info', 'message': 'No comments found for this post.'})}\n\n"
                yield f"data: {json.dumps({'type': 'done', 'message': 'Processing complete.'})}\n\n"
                return

            yield f"data: {json.dumps({'type': 'status', 'total_comments': total_comments})}\n\n"

            generated_count = 0
            for i, comment in enumerate(comments):
                log_to_stderr(f"Processing comment {i+1}/{total_comments}")
                yield f"data: {json.dumps({'type': 'status', 'comments_fetched': i + 1})}\n\n"

                try:
                    reply_text = generate_reply_with_google_api(user_system_prompt, comment.text)
                    generated_count += 1
                    log_to_stderr(f"Generated reply for comment {i+1}")

                    result = {
                        'comment_text': comment.text,
                        'owner': comment.owner.username,
                        'suggested_reply': reply_text
                    }
                    yield f"data: {json.dumps({'type': 'new_reply', 'data': result, 'replies_generated': generated_count})}\n\n"

                except Exception as api_error:
                    log_to_stderr(f"API Error for comment {i+1}: {api_error}")
                    yield f"data: {json.dumps({'type': 'error', 'message': f'Could not process comment by {comment.owner.username}: {api_error}'})}\n\n"

            log_to_stderr("--- Finished processing all comments ---")
            yield f"data: {json.dumps({'type': 'done', 'message': 'Processing complete.'})}\n\n"

        except Exception as e:
            log_to_stderr(f"--- FATAL ERROR in event_stream: {e} ---")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
                log_to_stderr("--- Temporary session file deleted ---")

    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
