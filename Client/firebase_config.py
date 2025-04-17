import pyrebase

firebase_config = {
  "apiKey": "AIzaSyDXtMdjC-C2nNkiPPg_AUv7QuukXo6FAdw",
  "authDomain": "personal-assistant-12bfa.firebaseapp.com",
  "projectId": "personal-assistant-12bfa",
  "storageBucket": "personal-assistant-12bfa.firebasestorage.app",
  "messagingSenderId": "161474846821",
  "appId": "1:161474846821:web:546495cdc40f8731a4268c",
  "measurementId": "G-2TN08DJP8M",
  "databaseURL": "https://personal-assistant-12bfa-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

