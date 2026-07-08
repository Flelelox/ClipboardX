import re
import json
import base64
from urllib.parse import urlparse


EMAIL_RE = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

IP_RE = re.compile(
    r"^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(25[0-5]|2[0-4]\d|1?\d?\d)$"
)

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

PHONE_RE = re.compile(
    r"^\+?[0-9\-\(\)\s]{8,20}$"
)


def is_url(text):
    try:
        result = urlparse(text)
        return bool(result.scheme and result.netloc)
    except:
        return False


def is_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False


def is_base64(text):
    try:
        if len(text) < 12:
            return False

        base64.b64decode(text, validate=True)
        return True

    except:
        return False


def detect(text: str) -> str:

    text = text.strip()

    if not text:
        return "📄 Text"

    # URL
    if is_url(text):
        return "🌐 URL"

    # Email
    if EMAIL_RE.match(text):
        return "📧 Email"

    # IP
    if IP_RE.match(text):
        return "🌍 IP"

    # UUID
    if UUID_RE.match(text):
        return "🆔 UUID"

    # Телефон
    if PHONE_RE.match(text):
        return "📱 Phone"

    # JSON
    if is_json(text):
        return "📦 JSON"

    # HTML
    lower = text.lower()

    if "<html" in lower or "<body" in lower:
        return "🌍 HTML"

    # XML
    if "<?xml" in lower:
        return "📰 XML"

    # Markdown
    if "# " in text or "## " in text or "```" in text:
        return "📝 Markdown"

    # SQL
    sql = [
        "SELECT ",
        "INSERT INTO",
        "UPDATE ",
        "DELETE FROM",
        "CREATE TABLE",
        "ALTER TABLE",
        "DROP TABLE"
    ]

    if any(x in text.upper() for x in sql):
        return "🗄 SQL"

    # Python
    python = [
        "def ",
        "class ",
        "import ",
        "from ",
        "if __name__",
        "print("
    ]

    if any(x in text for x in python):
        return "🐍 Python"

    # JavaScript
    js = [
        "console.log",
        "function ",
        "=>",
        "const ",
        "let ",
        "var "
    ]

    if any(x in text for x in js):
        return "🟨 JavaScript"

    # C/C++
    cpp = [
        "#include",
        "std::",
        "cout <<",
        "cin >>"
    ]

    if any(x in text for x in cpp):
        return "⚙️ C/C++"

    # Java
    if "public static void main" in text:
        return "☕ Java"

    # Go
    if "package main" in text:
        return "🐹 Go"

    # Rust
    if "fn main()" in text:
        return "🦀 Rust"

    # Bash
    if text.startswith("#!/bin/bash") or "sudo " in text:
        return "🐧 Bash"

    # PowerShell
    if "Get-ChildItem" in text or "Write-Host" in text:
        return "💙 PowerShell"

    # JWT
    if text.count(".") == 2 and len(text) > 60:
        return "🔑 JWT"

    # Base64
    if is_base64(text):
        return "🔐 Base64"

    # Длинный текст
    if len(text) > 500:
        return "📚 Large Text"

    return "📄 Text"