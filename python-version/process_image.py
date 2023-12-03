import os

import requests
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='src', static_url_path='/')

# Replace 'YOUR_DEFAULT_API_KEY' with the name of the environment variable
DEFAULT_API_KEY = os.environ.get('YOUR_DEFAULT_API_KEY', 'YOUR_DEFAULT_API_KEY')


@app.route('/')
def index():
    """Return the index.html page."""
    return app.send_static_file('index.html')

system_prompt = "What emotion are you observing in the image? Ignore the lighting, blurriniess, and conditions in the background. Use the emotion to inform your response to the user's question. In your response, tell the user what emotion you are detecting in the image before providing a response. Your recommendation and suggestion should help the guide the user to their goal while also detecting the emotion you are detecting in the image."
@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    base64_image = data.get('image', '')
    user_text = data.get('user_text', '')

    if base64_image and user_text:
        api_key = DEFAULT_API_KEY
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return jsonify({'error': 'Failed to process the image.'}), 500
        return response.content

    else:
        return jsonify({'error': 'No image data or user text received.'}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
