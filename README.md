# HUFS Course Catalog Chatbot

HUFS Course Catalog Chatbot is a conversational assistant designed to provide information about course registration, graduation requirements, major-specific details, and academic policies at Hankuk University of Foreign Studies (HUFS).

## Features

- **Conversational AI:** Powered by OpenAI's GPT model for natural language understanding.
- **Hybrid Search System:** Combines semantic and keyword-based search for precise information retrieval.
- **Contextual Responses:** Utilizes relevant data to generate step-by-step answers in Korean.
- **User-Friendly Interface:** Simple web-based chat interface built with HTML, CSS, and JavaScript.

## How It Works

1. Users ask questions about course registration, graduation, or other academic policies.
2. The chatbot processes the query using hybrid search algorithms.
3. The chatbot fetches and formats the answer using relevant course catalog data.
4. Results are displayed in the chat interface.

## Technologies Used

- **Backend:** Python, Flask
- **AI Model:** OpenAI GPT, `jhgan/ko-sbert-nli` for semantic embeddings
- **Frontend:** HTML, CSS, JavaScript
- **Data Management:** JSON-based course catalog data
- **Libraries:**
  - `flask`
  - `flask-cors`
  - `sentence-transformers`
  - `rank-bm25`
  - `numpy`
  - `python-dotenv`

## Project Structure

```
E:.
│   .env                # Environment variables
│   .gitignore          # Ignored files
│   LICENSE             # License information
│   README.md           # Project documentation
│
├───Eval                # Evaluation scripts and datasets
│       eval_code.py
│       main.py
│       processed_data.json
│
├───server              # Backend server
│       server.py
│       utils.py
│       search.py
│
├───static              # Frontend resources
│       index.html
│       style.css
│       script.js
│       bot-avatar.png
│       user-avatar.png
│
└───__pycache__         # Python compiled files (ignored in .gitignore)
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/HufsCourseCatalogChat.git
   cd HufsCourseCatalogChat
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On macOS/Linux
   venv\Scripts\activate       # On Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

5. Start the Flask server:
   ```bash
   python server/server.py
   ```

6. Open the chat interface:
   - Navigate to `http://127.0.0.1:1954` in your browser.

## Usage

- **Ask Questions:** Enter your query in the input box, and click "Send" to get a response.
- **Supported Queries:** Course registration schedules, graduation requirements, and major-related questions.

## Contributing

Contributions are welcome! Please follow the guidelines in `CONTRIBUTING.md`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.