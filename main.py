
from flask import Flask,request,redirect
from urllib.parse import urlparse
import string
import secrets
import os
import sqlite3
from datetime import datetime, timezone
app=Flask(__name__)
DATABASE = os.getenv("DATABASE_PATH", "urls.db")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
@app.get("/")
def home():
    return{
        "message":"your url shortner is running"
    }

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ""

    for i in range(6):
        short_code = short_code + secrets.choice(characters)

    return short_code 
def short_code_exists(short_code):

    connection = None

    try:
        connection = sqlite3.connect(DATABASE)

        cursor = connection.execute(
            """
            SELECT 1
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,)
        )

        row = cursor.fetchone()

        return row is not None

    except sqlite3.Error:
        return False

    finally:
        if connection is not None:
            connection.close()

def save_url(short_code, original_url):
    connection = None
    try:
        connection = sqlite3.connect(DATABASE)

        connection.execute(
            """
            INSERT INTO urls (short_code, original_url, created_at)
            VALUES (?, ?, ?)
            """,
            (
                short_code,
                original_url,
                datetime.now(timezone.utc).isoformat()
            )
        )

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error:
        return False
    finally:
        if connection is not None:
            connection.close()
    
def get_original_url(short_code):

    connection = None

    try:
        connection = sqlite3.connect(DATABASE)

        cursor = connection.execute(
            """
            SELECT original_url
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row[0]

    except sqlite3.Error:
        raise

    finally:
        if connection is not None:
            connection.close()
 
@app.post("/shorten")
def url_shorten():
    data=request.get_json(silent=True)
    if not data:
        return{
            "message":"JSON body missing"
        },400

    if "url" not in data:
          return {
            "error": "URL is required"
        }, 400
    url=data["url"]
    if not isinstance(url, str) or not url.strip():
     return {
        "error": "URL must be a non-empty string"
    }, 400
    result=urlparse(url)
    if result.scheme not in ("http","https") or not result.netloc:
        return{
            "message":"url is invalid"
        },400
    short_code=generate_short_code()
    while short_code_exists(short_code):
     short_code = generate_short_code() 

    saved=save_url(short_code, url)

    if not saved:
        return{
            "error":"url is not saved"
        },500

    return  {
    "message": "URL shortened successfully",
    "short_code": short_code,
    "short_url": f"{BASE_URL}/{short_code}"
},201
@app.get("/<short_code>")

def redirect_to_url(short_code):

    
    try:
        original_url = get_original_url(short_code)

    except sqlite3.Error:
        return {
            "error": "Database error"
        }, 500
        

    if original_url is None:
        return {
            "error": "short url is not found"
        }, 404

    return redirect(original_url)


def init_db():
    connection=sqlite3.connect(DATABASE)
    connection.execute("""CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


if __name__=="__main__":
    init_db()
    app.run(debug=True)
