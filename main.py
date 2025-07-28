import os
from flask import Flask, render_template, request, jsonify
import instaloader
from transformers import pipeline
import torch

app = Flask(__name__)

# Hugging Face modelini yükle
hf_token = os.getenv("HUGGING_FACE_TOKEN")
if not hf_token:
    raise ValueError("Hugging Face token not found. Please set the HUGGING_FACE_TOKEN environment variable.")

generator = pipeline("text-generation", model="google/gemma-2b-it", torch_dtype=torch.bfloat16, token=hf_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    shortcode = data.get('shortcode')
    system_prompt = data.get('system_prompt')

    if not all([username, password, shortcode, system_prompt]):
        return jsonify({'error': 'All fields are required.'}), 400

    try:
        L = instaloader.Instaloader()
        L.login(username, password)

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        comments = list(post.get_comments())

        results = []
        for comment in comments:
            prompt = f"{system_prompt}\n###\nComment: \"{comment.text}\"\n###\nReply:"
            outputs = generator(prompt, max_new_tokens=30, num_return_sequences=1)
            reply_text = outputs[0]['generated_text'].split("Reply:")[1].strip()

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
