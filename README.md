# AI Code Analyzer (CodeGuard)

Hello! Welcome to the AI Code Analyzer project. This is a very useful tool for your Python code. It helps you find errors and write clean code.

This project has three main parts:

1. **Backend:** The brain of the project. It uses FastAPI and Python.
2. **Desktop App (codeguard_py):** A computer program to check your code. It uses PyQt6.
3. **Frontend:** A web page for the project. It uses React and Vite.

---

## What can you do with this project?

- **Check Code:** You can check your Python files. The program finds security problems.
- **See Scores:** You can see your code score (0 to 100).
- **AI Chat:** You can talk to the Artificial Intelligence (AI). You can ask questions about your code.
- **Clean Code:** The program helps you write better and cleaner code.

---

## How to Install and Run

First, you need to download this project to your computer.

### 1. Run the Backend (API)

The backend needs Python and MongoDB. 

```bash
# Go to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
.\venv\Scripts\activate
# For Mac/Linux:
# source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Create .env file from the example
# Copy .env.example and rename it to .env
# (Add your OPENAI_API_KEY in the .env file if you want AI chat)

# Start the server
uvicorn main:app --reload
```
Now, the backend is working at `http://127.0.0.1:8000`.

### 2. Run the Desktop App (CodeGuard)

Keep the backend running. Open a **new** terminal window.

```bash
# Go to the codeguard_py folder
cd codeguard_py

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows:
.\venv\Scripts\activate
# For Mac/Linux:
# source venv/bin/activate

# Install the required packages
pip install PyQt6 requests

# Start the application
python main.py
```
Now, you can see the CodeGuard window on your screen!

### 3. Run the Frontend (Web App)

If you want to see the web page, open a **new** terminal window.

```bash
# Go to the frontend folder
cd frontend

# Install the packages
npm install

# Start the web app
npm run dev
```

---

## Technologies Used

- **Python:** The main programming language.
- **FastAPI:** To make the API fast.
- **PyQt6:** To make the desktop application.
- **React & Vite:** To make the fast web page.
- **MongoDB:** To save data (database).
- **OpenAI:** To chat about the code.

## Notes

- Make sure MongoDB is running on your computer.
- You need an OpenAI API key for the AI chat to work.

Enjoy coding! 🚀
