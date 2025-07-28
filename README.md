# Instagram AI Comment Replier (Final Version)

This is a lightweight Flask-based web application that uses a user-uploaded `instaloader` session to fetch comments, generates reply suggestions with the Google Generative Language API, and allows the user to post the reply directly to Instagram using the Meta Graph API.

## Features

-   **Secure Session Handling**: Uses a session file created locally by the user and uploaded via the browser. The file is deleted from the server immediately after use.
-   **AI-Powered Suggestions**: Generates replies using Google's Gemma model via their API.
-   **One-Click Replies**: Allows posting the suggested reply to Instagram with a single button click.
-   **Lightweight**: Optimized for low-memory environments like Render.com's free tier.

## How it works

1.  **Create Session (One-time setup):** The user runs `instaloader --login=YOUR_USERNAME` on their computer to create a session file.
2.  **Upload & Fetch**: In the web app, the user uploads their session file and provides their username and the video shortcode. The app loads the session to fetch comments.
3.  **Generate Suggestions**: The app sends each comment to the Google API to get a reply suggestion based on a fixed system prompt within the code.
4.  **Review & Reply**: The user reviews the suggestions. If they like a suggestion, they click the "Reply" button.
5.  **Post Reply**: The app sends a request to the Meta Graph API to post the text as a reply to the specific comment on Instagram.

## How to Use

### Step 1: Create Your Instagram Session File

On your local computer, run the following command in your terminal. You need to have `instaloader` installed (`pip install instaloader`).

```bash
instaloader --login=YOUR_INSTAGRAM_USERNAME
```

Enter your password when prompted. This will create a file named after your username (e.g., `your_instagram_username`) in your current directory. This is the file you will upload to the web app.

### Step 2: Set Up Environment Variables

You need API keys for both Google and Meta (Facebook).

1.  Create a `.env` file for local use: `cp .env.example .env`.
2.  Add your keys to the file:
    *   `GOOGLE_API_KEY`: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   `META_GRAPH_API_TOKEN`: This is a User Access Token from a Facebook App with the necessary permissions (`instagram_manage_comments`). See [Meta's documentation](https://developers.facebook.com/docs/graph-api/overview) for how to get this.

### Step 3: Run or Deploy

*   **Local Use**: Run `flask run` and open the app in your browser.
*   **Deployment on Render.com**:
    1.  Deploy your repository.
    2.  Set the build command: `pip install -r requirements.txt`.
    3.  Set the start command: `gunicorn main:app`.
    4.  In the "Environment" tab, add your `GOOGLE_API_KEY` and `META_GRAPH_API_TOKEN` as environment variables.
