"""Environment configuration for Robot; passwords are never stored in source."""

import os
import secrets
from urllib.parse import urlsplit

from robot.api.types import Secret


def get_variables():
    base_url = os.getenv("TB_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
    parsed = urlsplit(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.path:
        raise ValueError("TB_BASE_URL deve ser uma origem HTTP(S), sem caminho.")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("TB_BASE_URL nao deve conter credenciais, query ou fragmento.")
    for name in ("TB_USERNAME", "TB_PASSWORD"):
        if not os.getenv(name):
            raise ValueError(f"Defina a variavel de ambiente {name} antes de executar.")
    password = os.environ["TB_PASSWORD"]
    invalid_password = os.getenv("TB_INVALID_PASSWORD") or secrets.token_urlsafe(32)
    if invalid_password == password:
        raise ValueError("TB_INVALID_PASSWORD deve diferir de TB_PASSWORD.")
    headless = os.getenv("TB_HEADLESS", "true").lower()
    if headless not in ("true", "false"):
        raise ValueError("TB_HEADLESS deve ser true ou false.")
    return {
        "BASE_URL": base_url,
        "USERNAME": os.environ["TB_USERNAME"],
        "PASSWORD": Secret(password),
        "INVALID_PASSWORD": Secret(invalid_password),
        "BROWSER": os.getenv("TB_BROWSER", "chromium"),
        "HEADLESS": headless == "true",
        "UI_TIMEOUT": os.getenv("TB_UI_TIMEOUT", "15s"),
    }
