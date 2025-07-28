# Instagram AI Comment Replier (Hierarchical Prompts)

This is the final, advanced version of the application. It uses a hierarchical prompt system for nuanced AI control, secure session handling for Instagram login, and the Meta Graph API for posting replies.

## Core Features

-   **Hierarchical Prompts**: A two-level prompt system provides both robust control and user flexibility.
    1.  **Main System Prompt (Backend)**: Defines the core rules for the AI (e.g., "be a helpful assistant, max 30 words"). This is hard-coded and cannot be changed by the user.
    2.  **User System Prompt (Frontend)**: Allows the user to specify the tone and style for each batch of replies (e.g., "be funny and use emojis" or "reply in French").
-   **Secure Session Handling**: Avoids checkpoint errors by using a session file created locally by the user and uploaded securely via the browser. The file is deleted from the server immediately after use.
-   **AI-Powered Suggestions**: Generates replies using Google's Gemma model via their API.
-   **One-Click Replies**: Allows posting the suggested reply directly to Instagram with a single button click.

## How to Use

### Step 1: Create Your Instagram Session File

On your local computer, run the following command in your terminal. You need to have `instaloader` installed (`pip install instaloader`).

```bash
instaloader --login=YOUR_INSTAGRAM_USERNAME
```

Enter your password when prompted. This will create a file named after your username (e.g., `your_instagram_username`). This is the file you will upload.

### Step 2: Set Up Environment Variables

You need API keys for both Google and Meta (Facebook).

1.  Create a `.env` file for local use: `cp .env.example .env`.
2.  Add your keys to the file:
    *   `GOOGLE_API_KEY`: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   `META_GRAPH_API_TOKEN`: This is a User Access Token from a Facebook App with the `instagram_manage_comments` permission.

### Step 3: Run or Deploy

1.  **Run Locally**: `flask run`.
2.  **Deploy to Render.com**:
    *   Set the build command: `pip install -r requirements.txt`.
    *   Set the start command: `gunicorn main:app`.
    *   In the "Environment" tab, add your `GOOGLE_API_KEY` and `META_GRAPH_API_TOKEN`.

### Step 4: Use the Web App

1.  Open the application in your browser.
2.  Enter your Instagram username.
3.  Upload the session file you created.
4.  Enter the video shortcode.
5.  Provide a "Tone & Style Prompt" to guide the AI for this specific task.
6.  Click "Fetch & Generate Replies".
7.  Review the suggestions and click "Reply" on the ones you like.
