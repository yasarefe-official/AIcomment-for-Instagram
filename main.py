import os
from flask import Flask, render_template, request, jsonify
import instaloader
import requests as req
from transformers import pipeline
import torch

app = Flask(__name__)

# Hugging Face modelini yükle
generator = pipeline("text-generation", model="google/gemma-2b-it", torch_dtype=torch.bfloat16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    shortcode = data.get('shortcode')
    system_prompt = data.get('system_prompt')

    if not shortcode or not system_prompt:
        return jsonify({'error': 'Shortcode and system prompt are required.'}), 400

    try:
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = list(post.get_comments())

        results = []
        for comment in comments:
            prompt = f"{system_prompt}\n###\nComment: \"{comment.text}\"\n###\nReply:"
            outputs = generator(prompt, max_new_tokens=30, num_return_sequences=1)
            reply_text = outputs[0]['generated_text'].split("Reply:")[1].strip()

            results.append({
                'comment_id': comment.id,
                'comment_text': comment.text,
                'suggested_reply': reply_text
            })

        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reply', methods=['POST'])
def reply():
    data = request.json
    comment_id = data.get('comment_id')
    reply_text = data.get('reply_text')
    access_token = os.getenv('META_GRAPH_API_TOKEN')

    if not comment_id or not reply_text or not access_token:
        return jsonify({'error': 'Comment ID, reply text, and access token are required.'}), 400

    url = f"https://graph.facebook.com/v20.0/{comment_id}/replies"
    params = {
        'message': reply_text,
        'access_token': access_token
    }

    try:
        response = req.post(url, params=params)
        response.raise_for_status()
        return jsonify({'status': 'success', 'message': 'Reply sent successfully.'})
    except req.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
