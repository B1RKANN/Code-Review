import requests
from typing import Dict, Any, Tuple
import os
import keyring
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api/v1")
SERVICE_NAME = "CodeGuardApp"
TOKEN_KEY = "auth_token"

def get_auth_headers():
    token = keyring.get_password(SERVICE_NAME, TOKEN_KEY)
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login_user(email: str, password: str) -> Tuple[bool, str]:
    try:
        response = requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                keyring.set_password(SERVICE_NAME, TOKEN_KEY, token)
                return True, ""
        err = response.json().get("detail", "Giriş başarısız") if response.content else "Giriş başarısız"
        return False, err
    except Exception as e:
        print(f"Login error: {e}")
        return False, str(e)

def register_user(full_name: str, email: str, password: str) -> Tuple[bool, str]:
    try:
        response = requests.post(f"{BACKEND_URL}/auth/register", json={
            "full_name": full_name,
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                keyring.set_password(SERVICE_NAME, TOKEN_KEY, token)
                return True, ""
        err = response.json().get("detail", "Kayıt başarısız") if response.content else "Kayıt başarısız"
        return False, err
    except Exception as e:
        print(f"Register error: {e}")
        return False, str(e)

def logout_user():
    try:
        keyring.delete_password(SERVICE_NAME, TOKEN_KEY)
    except keyring.errors.PasswordDeleteError:
        pass

def analyze_file(file_path: str) -> Dict[str, Any]:
    """
    Belirtilen dosyayı okuyup backend'e gönderir ve analiz sonucunu döndürür.
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(f"{BACKEND_URL}/analyze/analyze-file", files=files, headers=get_auth_headers())
            
        if response.status_code == 200:
            return response.json()
        else:
            err_msg = response.text.encode('utf-8', 'replace').decode('utf-8')
            print(f"API Error ({response.status_code}): {err_msg}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def chat_about_file(file_path: str, message: str) -> str:
    """
    Belirtilen dosyanın içeriğini okuyup backend'e chat mesajıyla birlikte gönderir.
    """
    try:
        if not file_path or not os.path.exists(file_path):
            source_code = ""
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()

        payload = {
            "message": message,
            "file_path": file_path,
            "source_code": source_code
        }
        
        response = requests.post(f"{BACKEND_URL}/analyze/chat", json=payload, headers=get_auth_headers())
        
        if response.status_code == 200:
            return response.json().get("reply", "Yanıt alınamadı.")
        else:
            print(f"Chat API Error ({response.status_code}): {response.text}")
            return f"<p>Sunucu Hatası ({response.status_code}): {response.text}</p>"
    except Exception as e:
        print(f"Chat Connection Error: {e}")
        return f"<p>Bağlantı Hatası: {e}</p>"
