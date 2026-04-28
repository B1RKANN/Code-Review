import urllib.request
import urllib.parse
import json
import subprocess
import time

print("Starting server...")
proc = subprocess.Popen(["venv/bin/uvicorn", "main:app", "--port", "8005"], cwd="/home/birkan/Desktop/Code-Review/backend")
time.sleep(3)

def test_api(filename, content):
    import urllib.request
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: text/plain\r\n\r\n'
        f'{content}\r\n'
        f'--{boundary}--\r\n'
    ).encode('utf-8')
    
    req = urllib.request.Request("http://127.0.0.1:8005/api/v1/analyze/scores")
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    try:
        with urllib.request.urlopen(req, data=body) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(e.read())
        return None

print("Testing first file...")
print(test_api('business.service.ts', 'const x = 1;'))

print("Testing second file...")
print(test_api('business.service.ts', 'const x = 1; \n// fixed version\n const y = 2;'))

proc.terminate()
