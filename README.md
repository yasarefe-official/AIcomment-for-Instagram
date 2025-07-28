# Instagram AI Comment Suggester (Google API Edition)

This is a lightweight Flask-based web application that uses your Instagram credentials to fetch comments from a video post and then generates reply suggestions using the Google Generative Language API.

This version is optimized for low-memory environments like Render.com's free tier, as it does not load heavy models locally.

## How it works

1.  **User Input**: The user provides their Instagram username, password, the shortcode of the video post, and a system prompt to guide the AI's tone and style.
2.  **Login & Fetch**: The application uses `instaloader` to log in to Instagram with the provided credentials and fetches all comments from the specified video.
3.  **Generate AI Suggestions**: For each comment, a request is sent to the Google Generative Language API (with the Gemma model) to generate a reply suggestion. This requires a Google API Key.
4.  **Display Results**: The web UI lists each comment along with its AI-generated reply suggestion.

## App Structure

*   `/`: GET - Displays the HTML form for user input.
*   `/process_video`: POST - Logs in, fetches comments, generates suggestions via API, and returns them as a JSON response.

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
3.  **Set up environment variables**:
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and add your Google API Key. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```
4.  **Run the application**:
    ```bash
    flask run
    ```

### Deployment on Render.com

1.  Create a new Web Service on Render.com and connect your GitHub repository.
2.  Set the build command to `pip install -r requirements.txt`.
3.  Set the start command to `gunicorn main:app`.
4.  In the Render.com dashboard, go to "Environment" and add a new environment variable:
    *   **Key**: `GOOGLE_API_KEY`
    *   **Value**: `your_google_api_key_here`
5.  This lightweight version should deploy smoothly on Render's free tier.
