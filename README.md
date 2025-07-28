# Real-Time Instagram AI Suggester

This is a dynamic web application that fetches Instagram comments and generates AI-powered reply suggestions, showing the entire process to the user in real-time.

## Core Features

-   **Real-Time Progress**: The UI updates live as comments are fetched and replies are generated, using Server-Sent Events (SSE) for a dynamic user experience.
-   **Hierarchical Prompts**: A two-level prompt system provides both robust control and user flexibility.
    1.  **Main System Prompt (Backend)**: Defines the core rules for the AI (e.g., "be a helpful assistant, max 30 words").
    2.  **User System Prompt (Frontend)**: Allows the user to specify the tone and style for each batch (e.g., "be funny and use emojis").
-   **Secure Session Handling**: Avoids checkpoint errors by using a session file created locally by the user and uploaded securely via the browser. The file is deleted from the server immediately after use.
-   **Lightweight & Deployable**: Optimized for low-memory environments like Render.com's free tier.

## How to Use

### Step 1: Create Your Instagram Session File

On your local computer, run the following command in your terminal. You need to have `instaloader` installed (`pip install instaloader`).

```bash
instaloader --login=YOUR_INSTAGRAM_USERNAME
```

Enter your password when prompted. This will create a file named after your username (e.g., `your_instagram_username`). This is the file you will upload.

### Step 2: Set Up Environment Variables

You need a Google API key to generate AI suggestions.

1.  Create a `.env` file for local use: `cp .env.example .env`.
2.  Add your key to the file:
    *   `GOOGLE_API_KEY`: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Step 3: Run or Deploy

*   **Local Use**: Run `flask run`.
*   **Deployment on Render.com**:
    *   Set the build command: `pip install -r requirements.txt`.
    *   Set the start command: `gunicorn main:app`.
    *   In the "Environment" tab, add your `GOOGLE_API_KEY` as an environment variable.

### Step 4: Use the Web App

1.  Open the application in your browser.
2.  Enter your Instagram username and upload the session file.
3.  Enter the video shortcode and a "Tone & Style Prompt".
4.  Click "Fetch & Generate in Real-Time" and watch the magic happen!
