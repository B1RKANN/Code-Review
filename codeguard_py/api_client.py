import requests
from typing import Dict, Any
import os

BACKEND_URL = "http://127.0.0.1:8000/api/v1/analyze"

def analyze_file(file_path: str) -> Dict[str, Any]:
    """
    Belirtilen dosyayı okuyup backend'e gönderir ve analiz sonucunu döndürür.
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(f"{BACKEND_URL}/analyze-file", files=files)
            
        if response.status_code == 200:
            print(f"API Success: {response.status_code} for {file_path}")
            return response.json()
        else:
            err_msg = response.text.encode('utf-8', 'replace').decode('utf-8')
            print(f"API Error ({response.status_code}): {err_msg} for {file_path}")
            return None
    except Exception as e:
        print(f"Connection Error: {e} for {file_path}")
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
        
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        
        if response.status_code == 200:
            return response.json().get("reply", "Yanıt alınamadı.")
        else:
            print(f"Chat API Error ({response.status_code}): {response.text}")
            return f"<p>Sunucu Hatası ({response.status_code}): {response.text}</p>"
    except Exception as e:
        print(f"Chat Connection Error: {e}")
        return f"<p>Bağlantı Hatası: {e}</p>"
