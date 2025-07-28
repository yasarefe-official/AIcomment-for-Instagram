# Instagram Comment Replier

This is a Flask-based web application for managing the process of replying to Instagram video comments.

## How it works

1.  **User Input**: The user provides an Instagram video shortcode (e.g., "Ck3Xb9zA7yL") and a custom system prompt that defines the tone, style, and rules for the replies.
2.  **Fetch Comments**: The application uses `instaloader` to fetch all comments from the specified video.
3.  **Generate AI Replies**: For each comment, a prompt is sent to the Hugging Face Gemma model (`google/gemma-2b-it`) to generate a reply of up to 30 tokens.
4.  **Display Replies**: The web UI lists each comment with its suggested AI-generated reply.
5.  **Manual Sending**: The user can click a "Reply" button to post the suggested reply to the corresponding comment using the Meta Graph API.

## App Structure

*   `/`: GET - Displays the HTML form for user input.
*   `/process_video`: POST - Processes the video, fetches comments, generates replies, and returns a JSON response.
*   `/reply`: POST - Sends a reply to a specific comment.

## Deployment on Render.com

This application is designed for easy deployment on Render.com.

### Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/instagram-comment-replier.git
    cd instagram-comment-replier
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
    Open the `.env` file and add your Meta Graph API token:
    ```
    META_GRAPH_API_TOKEN=your_meta_graph_api_token_here
    ```
4.  **Run the application locally**:
    ```bash
    flask run
    ```

### Deployment

1.  Create a new Web Service on Render.com and connect your GitHub repository.
2.  Set the build command to `pip install -r requirements.txt`.
3.  Set the start command to `gunicorn main:app`.
4.  Add your `META_GRAPH_API_TOKEN` as an environment variable in the Render.com dashboard.

## Constraints

*   Only works for Instagram video comments.
*   Replies are limited to a maximum of 20 words.
*   The system prompt fully determines the tone and style of the replies; no rules are hard-coded in the application.
