# Instagram AI Comment Suggester (Secure Session Upload)

This is a lightweight Flask-based web application that uses a user-uploaded `instaloader` session to fetch comments from a video post and then generates reply suggestions using the Google Generative Language API.

This version uses a secure method where the session file is uploaded directly through the browser and is never stored permanently on the server or in a git repository.

## How it works

1.  **Create Session (One-time setup on your computer):** The user runs a local script (`create_session.py`) to log in to Instagram. This creates a session file on their computer.
2.  **Upload Session & Provide Info**: In the web app, the user provides their Instagram username, the video shortcode, a system prompt for the AI, and uploads the session file created in the first step.
3.  **Load Session & Fetch**: The application backend receives the session file, loads it into `instaloader`, and immediately fetches the comments. The session file is deleted from the server right after use.
4.  **Generate AI Suggestions**: For each comment, a request is sent to the Google Generative Language API.
5.  **Display Results**: The web UI lists each comment along with its AI-generated reply suggestion.

## How to Use

### Step 1: Create Your Instagram Session File

You must do this once on your local machine.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/instagram-ai-comment-suggester.git
    cd instagram-ai-comment-suggester
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the session creation script**:
    ```bash
    python create_session.py
    ```
    Enter your Instagram username and password. This will create a file named after your username (e.g., `your_insta_user`) in the project directory. This is the file you will upload to the web app.

### Step 2: Set Up Environment Variables (for deployment)

If deploying to a service like Render, you will need to set your Google API Key.

1.  Create a `.env` file for local use: `cp .env.example .env` and add your key.
2.  For Render, go to "Environment" and add a new environment variable:
    *   **Key**: `GOOGLE_API_KEY`
    *   **Value**: `your_google_api_key_here` (Get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Step 3: Run the Application

1.  Run locally with `flask run`.
2.  Open the web page, fill in the fields, and select your session file in the file upload input.
3.  Click "Fetch & Generate Suggestions".
