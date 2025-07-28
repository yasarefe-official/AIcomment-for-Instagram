# Instagram AI Comment Suggester

This is a Flask-based web application that uses your Instagram credentials to fetch comments from a video post and then generates reply suggestions using a Hugging Face AI model.

## How it works

1.  **User Input**: The user provides their Instagram username, password, the shortcode of the video post, and a system prompt to guide the AI's tone and style.
2.  **Login & Fetch**: The application uses `instaloader` to log in to Instagram with the provided credentials and fetches all comments from the specified video.
3.  **Generate AI Suggestions**: For each comment, a prompt is sent to the Hugging Face Gemma model (`google/gemma-2b-it`) to generate a reply suggestion based on the user's system prompt.
4.  **Display Results**: The web UI lists each comment along with its AI-generated reply suggestion. There is no feature to automatically send the replies.

## App Structure

*   `/`: GET - Displays the HTML form for user input.
*   `/process_video`: POST - Logs in, fetches comments, generates suggestions, and returns them as a JSON response.

## How to Use

### Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/instagram-ai-comment-suggester.git
    cd instagram-ai-comment-suggester
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

### Deployment on Render.com

1.  Create a new Web Service on Render.com and connect your GitHub repository.
2.  Set the build command to `pip install -r requirements.txt`.
3.  Set the start command to `gunicorn main:app`.
4.  Be aware of the security implications of handling credentials directly in the application. It is generally recommended for local use.
