import os
from flask import Flask, render_template, request, jsonify
import instaloader
import requests

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

    # Google API'sinin beklediği format ile prompt'u birleştiriyoruz.
    # Sistemin rolünü ve kullanıcı girdisini ayrı ayrı belirtmek genellikle daha iyi sonuç verir.
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
    response.raise_for_status() # Hata durumunda exception fırlat

    # API cevabından metni ayıkla
    # Cevap formatı: response.json()['candidates'][0]['content']['parts'][0]['text']
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except (KeyError, IndexError) as e:
        # API'den beklenen format gelmezse, hatayı logla veya bir varsayılan döndür
        print(f"Error parsing Google API response: {e}")
        return "Sorry, I couldn't generate a reply."


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
