# Personal Assistant - AI-Powered Productivity App

A Streamlit-based personal assistant web application that helps users manage their memos, tasks, calendar events, and interact with an AI chat companion.

## Features

- 🔐 **User Authentication**: Secure sign-up and sign-in using Firebase Authentication
- 📝 **Memos**: Capture and organize quick notes and ideas
- 💬 **Chat Companion**: AI-powered assistant that answers questions about your schedule, tasks, and memos
- 📅 **Calendar**: Schedule and manage events with date/time tracking
- ✅ **Task Organizer**: Create and track tasks with priority levels

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Authentication**: Firebase (Pyrebase)
- **State Management**: Streamlit Session State

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Chatbot-Realtime.git
cd Chatbot-Realtime
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\.venv\Scripts\Activate.ps1
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure Firebase:
   - Update `Client/firebase_config.py` with your Firebase project credentials
   - Or use environment variables for better security

## Running the Application

1. Navigate to the Client directory:
```bash
cd Client
```

2. Run the Streamlit app:
```bash
streamlit run main.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
Chatbot-Realtime/
├── Client/
│   ├── main.py              # Main application entry point
│   ├── sign_in_page.py      # Sign-in functionality
│   ├── sign_up_page.py      # Sign-up functionality
│   └── firebase_config.py   # Firebase configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## Usage

1. **Sign Up**: Create a new account with email and password (minimum 6 characters)
2. **Sign In**: Log in with your credentials
3. **Dashboard**: View quick overview of your tasks, events, and memos
4. **Memos**: Add and manage your notes
5. **Chat**: Ask questions about your schedule, tasks, or memos
6. **Calendar**: Schedule events and view your upcoming schedule
7. **Organize**: Create tasks with priorities and track completion

## Deployment

This app can be deployed to:
- Streamlit Community Cloud
- Heroku
- AWS/GCP/Azure
- Any platform that supports Python applications

## Future Enhancements

- [ ] Persistent data storage with Firestore
- [ ] Email notifications for events
- [ ] Task reminders
- [ ] Data export functionality
- [ ] Enhanced AI chat capabilities

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome!

