import sys
import os

# app klasörünün PYTHONPATH'e eklenmesini sağlıyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.analyzers.engine import AnalysisEngine

def test_syntax_error():
    engine = AnalysisEngine()
    bad_code = "def wrong_syntax() print('hello')"
    
    report = engine.analyze_code(bad_code, "bad.py")
    
    assert report.total_issues == 1
    assert report.issues[0].message.startswith("Sözdizimi hatası")

def test_srp_violation_long_function():
    engine = AnalysisEngine()
    
    # 50 satırdan uzun bir fonksiyon simülasyonu
    long_func_code = "def long_function():\n"
    for i in range(60):
        long_func_code += f"    x_{i} = {i}\n"
        
    report = engine.analyze_code(long_func_code, "long.py")
    
    # En az bir hata bulunmalı ve bu uzunlukla ilgili olmalı
    assert report.total_issues >= 1
    assert any("çok uzun" in issue.message for issue in report.issues)

def test_security_violation_eval():
    engine = AnalysisEngine()
    
    eval_code = "user_input = '1+1'\nresult = eval(user_input)"
    report = engine.analyze_code(eval_code, "eval_test.py")
    
    assert report.total_issues >= 1
    assert any("Tehlikeli fonksiyon" in issue.message for issue in report.issues)
    
def test_security_violation_hardcoded_secret():
    engine = AnalysisEngine()
    
    secret_code = "API_KEY = 'sk-1234567890abcdef'"
    report = engine.analyze_code(secret_code, "secret.py")
    
    assert report.total_issues >= 1
    assert any("hardcoded gizli bilgi" in issue.message for issue in report.issues)

def test_clean_code():
    engine = AnalysisEngine()
    
    clean_code = '''
def calculate_sum(a: int, b: int) -> int:
    return a + b
'''
    report = engine.analyze_code(clean_code, "clean.py")
    assert report.total_issues == 0
