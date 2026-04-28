"""Mock veri — proje, dosya ağacı, skorlar, bulgular, kod örnekleri."""

PROJECT = {
    "name": "fastapi-payments",
    "path": "~/projects/fastapi-payments",
    "python": "3.12.2",
    "venv": ".venv (active)",
    "pkg": "poetry · 47 deps",
    "branch": "feat/webhook-retry",
    "commit": "a4f2c91",
}

# Tree: list of dict { type, name, open?, children?, score?, lines?, severity? }
FILE_TREE = [
    {"type": "folder", "name": "app", "open": True, "children": [
        {"type": "folder", "name": "api", "open": True, "children": [
            {"type": "file", "name": "__init__.py", "score": 98, "lines": 12},
            {"type": "file", "name": "webhooks.py", "score": 62, "lines": 184, "severity": "bad"},
            {"type": "file", "name": "payments.py", "score": 81, "lines": 142, "severity": "warn"},
            {"type": "file", "name": "auth.py", "score": 74, "lines": 96, "severity": "warn"},
        ]},
        {"type": "folder", "name": "core", "open": True, "children": [
            {"type": "file", "name": "config.py", "score": 88, "lines": 54},
            {"type": "file", "name": "security.py", "score": 71, "lines": 112, "severity": "warn"},
            {"type": "file", "name": "db.py", "score": 91, "lines": 38},
        ]},
        {"type": "folder", "name": "models", "open": False, "children": [
            {"type": "file", "name": "user.py", "score": 94, "lines": 42},
            {"type": "file", "name": "transaction.py", "score": 86, "lines": 78},
        ]},
        {"type": "folder", "name": "services", "open": False, "children": [
            {"type": "file", "name": "stripe_client.py", "score": 79, "lines": 156},
            {"type": "file", "name": "notifier.py", "score": 92, "lines": 64},
        ]},
        {"type": "file", "name": "main.py", "score": 95, "lines": 28},
    ]},
    {"type": "folder", "name": "tests", "open": False, "children": [
        {"type": "file", "name": "test_webhooks.py", "score": 84, "lines": 96},
        {"type": "file", "name": "test_payments.py", "score": 88, "lines": 128},
        {"type": "file", "name": "conftest.py", "score": 96, "lines": 22},
    ]},
    {"type": "file", "name": "pyproject.toml", "score": 90, "lines": 48},
    {"type": "file", "name": "README.md", "score": 88, "lines": 84},
    {"type": "file", "name": ".env.example", "score": 100, "lines": 12},
]

FILE_SCORES = {
    "app/api/webhooks.py": {
        "overall": 62,
        "status": "Dikkat Gerekiyor",
        "statusKind": "warn",
        "metrics": {
            "security":  {"value": 48, "label": "Ağ Güvenliği",       "desc": "HTTP imza doğrulaması eksik, plain HTTP isteği tespit edildi.",     "stats": [("Açık", "3 yüksek"), ("Çözüldü", "2")]},
            "cleanCode": {"value": 71, "label": "Temiz Kod",          "desc": "Cyclomatic complexity 14, fonksiyon başına ortalama 38 satır.",     "stats": [("Smell", "8"), ("Duplicate", "1.4%")]},
            "perf":      {"value": 66, "label": "Performans / Bellek","desc": "Senkron HTTP istekleri olay döngüsünü blokluyor.",                  "stats": [("Hot path", "2"), ("Avg ms", "184")]},
            "robust":    {"value": 64, "label": "Genel Sağlamlık",    "desc": "Hata yönetimi yetersiz, retry stratejisi yok.",                     "stats": [("Try block", "1"), ("Coverage", "58%")]},
        },
    },
    "app/api/payments.py": {
        "overall": 81, "status": "İyi", "statusKind": "good",
        "metrics": {
            "security":  {"value": 84, "label": "Ağ Güvenliği",       "desc": "TLS zorunluluğu sağlanıyor, idempotency key kullanılıyor.",         "stats": [("Açık", "1 düşük"), ("Çözüldü", "6")]},
            "cleanCode": {"value": 78, "label": "Temiz Kod",          "desc": "İki uzun fonksiyon refactor edilebilir.",                           "stats": [("Smell", "3"), ("Duplicate", "0.6%")]},
            "perf":      {"value": 82, "label": "Performans / Bellek","desc": "DB sorguları async, n+1 sorunu yok.",                               "stats": [("Hot path", "0"), ("Avg ms", "44")]},
            "robust":    {"value": 80, "label": "Genel Sağlamlık",    "desc": "Test coverage iyi, edge-case eksikleri var.",                       "stats": [("Try block", "5"), ("Coverage", "82%")]},
        },
    },
    "default": {
        "overall": 87, "status": "Sağlıklı", "statusKind": "good",
        "metrics": {
            "security":  {"value": 92, "label": "Ağ Güvenliği",       "desc": "Bilinen CVE yok, secret sızıntısı tespit edilmedi.",                "stats": [("Açık", "0"), ("Çözüldü", "12")]},
            "cleanCode": {"value": 84, "label": "Temiz Kod",          "desc": "Tutarlı stil, düşük karmaşıklık. Birkaç uzun import bloğu.",        "stats": [("Smell", "4"), ("Duplicate", "0.8%")]},
            "perf":      {"value": 88, "label": "Performans / Bellek","desc": "Async pattern doğru kullanılıyor, bellek profili düz.",             "stats": [("Hot path", "0"), ("Avg ms", "31")]},
            "robust":    {"value": 85, "label": "Genel Sağlamlık",    "desc": "Kapsamlı test paketi, anlamlı hata mesajları.",                     "stats": [("Try block", "18"), ("Coverage", "87%")]},
        },
    },
}

FILE_FINDINGS = {
    "app/api/webhooks.py": [
        {"sev": "h", "title": "Webhook imza doğrulaması atlanmış",      "loc": "webhooks.py:42 · CWE-345",        "tag": "security"},
        {"sev": "h", "title": "Senkron requests çağrısı async fonksiyonda", "loc": "webhooks.py:78 · BLOCKING-IO", "tag": "perf"},
        {"sev": "m", "title": "Bare except blok hatayı yutuyor",         "loc": "webhooks.py:104 · E722",          "tag": "robust"},
        {"sev": "m", "title": "Cyclomatic complexity 14 (limit 10)",     "loc": "webhooks.py:process_event · C901","tag": "clean"},
        {"sev": "l", "title": "Tip ipucu eksik (3 parametre)",           "loc": "webhooks.py:55,62,89 · TYP",       "tag": "clean"},
    ],
    "default": [
        {"sev": "m", "title": "Uzun import bloğu (24 satır)",            "loc": "main.py:1-24 · I001",              "tag": "clean"},
        {"sev": "l", "title": "Docstring eksik public fonksiyon",        "loc": "main.py:start · D103",             "tag": "clean"},
        {"sev": "l", "title": "TODO yorumu çözüm bekliyor",              "loc": "main.py:42 · TD002",               "tag": "todo"},
    ],
}

FILE_SOURCES = {
    "app/api/webhooks.py": [
        (1,  "from fastapi import APIRouter, Request, HTTPException", None),
        (2,  "from typing import Any", None),
        (3,  "import requests  # noqa", "warn"),
        (4,  "import json, logging, hmac, hashlib", None),
        (5,  "", None),
        (6,  "from app.core.config import settings", None),
        (7,  "from app.services.stripe_client import StripeClient", None),
        (8,  "from app.models.transaction import Transaction", None),
        (9,  "", None),
        (10, "router = APIRouter(prefix=\"/webhooks\", tags=[\"webhooks\"])", None),
        (11, "log = logging.getLogger(__name__)", None),
        (12, "", None),
        (13, "", None),
        (14, "@router.post(\"/stripe\")", None),
        (15, "async def stripe_webhook(request: Request):", None),
        (16, "    \"\"\"Stripe webhook ana giriş noktası.\"\"\"", None),
        (17, "    payload = await request.body()", None),
        (18, "    sig = request.headers.get(\"stripe-signature\")", None),
        (19, "", None),
        (20, "    # TODO: imza dogrulama eklenecek", "info"),
        (21, "    event = json.loads(payload)", None),
        (22, "    return await process_event(event)", None),
        (23, "", None),
        (24, "", None),
        (25, "async def process_event(event: dict[str, Any]):", None),
        (26, "    kind = event.get(\"type\", \"\")", None),
        (27, "    obj = event.get(\"data\", {}).get(\"object\", {})", None),
        (28, "", None),
        (29, "    if kind == \"payment_intent.succeeded\":", None),
        (30, "        return await on_paid(obj)", None),
        (31, "    elif kind == \"payment_intent.payment_failed\":", None),
        (32, "        return await on_failed(obj)", None),
        (33, "    elif kind == \"charge.refunded\":", None),
        (34, "        return await on_refund(obj)", None),
        (35, "", None),
        (36, "    log.warning(\"unhandled webhook kind: %s\", kind)", None),
        (37, "    return {\"ok\": True}", None),
        (38, "", None),
        (39, "", None),
        (40, "async def notify_partner(url: str, body: dict):", None),
        (41, "    # senkron istek async fonksiyonu blokluyor", "bad"),
        (42, "    r = requests.post(url, json=body, timeout=5)", "bad"),
        (43, "    return r.status_code", None),
        (44, "", None),
        (45, "", None),
        (46, "async def on_failed(intent: dict):", None),
        (47, "    try:", None),
        (48, "        tx = await Transaction.get(intent[\"id\"])", None),
        (49, "        await tx.mark_failed(intent.get(\"last_payment_error\"))", None),
        (50, "    except:  # noqa", "warn"),
        (51, "        pass", None),
        (52, "    return {\"ok\": True}", None),
    ],
    "default": [
        (1,  "from fastapi import FastAPI", None),
        (2,  "from contextlib import asynccontextmanager", None),
        (3,  "", None),
        (4,  "from app.core.config import settings", None),
        (5,  "from app.core.db import lifespan_db", None),
        (6,  "from app.api import webhooks, payments, auth", None),
        (7,  "", None),
        (8,  "", None),
        (9,  "@asynccontextmanager", None),
        (10, "async def lifespan(app: FastAPI):", None),
        (11, "    async with lifespan_db():", None),
        (12, "        yield", None),
        (13, "", None),
        (14, "", None),
        (15, "app = FastAPI(", None),
        (16, "    title=settings.APP_NAME,", None),
        (17, "    version=settings.VERSION,", None),
        (18, "    lifespan=lifespan,", None),
        (19, ")", None),
        (20, "", None),
        (21, "app.include_router(webhooks.router)", None),
        (22, "app.include_router(payments.router)", None),
        (23, "app.include_router(auth.router)", None),
    ],
}

FILE_ASIDE = {
    "app/api/webhooks.py": [
        {"sev": "bad",  "line": 42, "title": "Bloklayan I/O",        "desc": "Async fonksiyon içinde senkron requests.post — event loop'u blokluyor. httpx.AsyncClient'a geçirin.", "fix": "Auto-fix: requests → httpx"},
        {"sev": "warn", "line": 50, "title": "Bare except",          "desc": "Tüm hataları yutan blok. Specific exception veya en azından Exception yakalayın ve loglayın.",        "fix": "Quick-fix öner"},
        {"sev": "info", "line": 20, "title": "İmza doğrulama eksik", "desc": "Stripe webhook'larda HMAC imza doğrulaması zorunlu. stripe.Webhook.construct_event kullanın.",          "fix": "Snippet ekle"},
    ],
    "default": [
        {"sev": "info", "line": 6, "title": "Import sırası",         "desc": "Modül imports isort konvansiyonuna göre düzenlenmiş. Sorun yok.",                                       "fix": None},
    ],
}


COMMANDS = [
    {"kind": "action", "label": "Tüm projeyi tara",                "icon": "play"},
    {"kind": "file",   "label": "app/api/webhooks.py",             "icon": "py", "path": "app/api/webhooks.py"},
    {"kind": "file",   "label": "app/api/payments.py",             "icon": "py", "path": "app/api/payments.py"},
    {"kind": "file",   "label": "app/core/security.py",            "icon": "py", "path": "app/core/security.py"},
    {"kind": "file",   "label": "app/main.py",                     "icon": "py", "path": "app/main.py"},
    {"kind": "view",   "label": "Skorlar görünümüne geç",          "icon": "gauge", "view": "scores"},
    {"kind": "view",   "label": "Kod görünümüne geç",              "icon": "code",  "view": "code"},
    {"kind": "action", "label": "Auto-fix: tüm güvenlik bulguları","icon": "sparkle"},
    {"kind": "action", "label": "Test coverage raporu üret",       "icon": "list"},
    {"kind": "action", "label": "Tema: dark / light",              "icon": "settings"},
]
