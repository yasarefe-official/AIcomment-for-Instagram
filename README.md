# Instagram AI Comment Suggester (Session-Based)

This is a lightweight Flask-based web application that uses a pre-saved `instaloader` session to fetch comments from a video post and then generates reply suggestions using the Google Generative Language API.

This version avoids `instaloader` checkpoint errors by using a session file instead of logging in with a password directly in the app.

## How it works

1.  **Create Session (One-time setup):** The user runs a local script (`create_session.py`) to log in to Instagram and create a session file. This file securely stores the login state.
2.  **User Input**: In the web app, the user provides their Instagram username (so the app can find the correct session file), the shortcode of the video post, and a system prompt for the AI.
3.  **Load Session & Fetch**: The application uses `instaloader` to load the pre-saved session and fetches all comments from the specified video.
4.  **Generate AI Suggestions**: For each comment, a request is sent to the Google Generative Language API to generate a reply suggestion.
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
    Enter your Instagram username and password when prompted. This will create a file named after your username (e.g., `your_insta_user`) in the project directory. This is your session file.

### Step 2: Set Up Environment Variables

1.  Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your Google API Key. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```

### Step 3: Run the Application

*   **Local Use**: Run `flask run`. The app will use the session file you created.
*   **Deployment on Render.com**:
    1.  Deploy your repository to Render.
    2.  **Important:** You must upload your generated session file to the root of your project on Render. You might need to use a different deployment method or include the session file in your git repository if you want to use it on Render. **Be aware of the security risk of committing session files to git.**
    3.  Set the build command to `pip install -r requirements.txt` and the start command to `gunicorn main:app`.
    4.  Add your `GOOGLE_API_KEY` as an environment variable in the Render dashboard.
