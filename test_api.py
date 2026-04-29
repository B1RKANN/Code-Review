import requests
import sys

def test():
    file_path = "c:/Users/arda/Desktop/Code-Review/codeguard_py/main.py"
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post("http://127.0.0.1:8000/api/v1/analyze/analyze-file", files=files)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("Response Data Keys:", data.keys())
            print("Score:", data.get("score"))
        else:
            print("Error Response:", response.text)
    except Exception as e:
        print("Exception:", str(e))

if __name__ == "__main__":
    test()
