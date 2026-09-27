@'
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Arabic": "ar"
}

@app.route("/")
def home():
    return render_template("index.html", languages=LANGUAGES)

@app.route("/api/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        source = data.get("source", "auto")
        target = data.get("target", "en")

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter some text to translate."
            }), 400

        if source == target:
            return jsonify({
                "success": True,
                "translation": text
            })

        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{source}|{target}"
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        result = response.json()
        translation = result.get("responseData", {}).get("translatedText", "")

        if not translation:
            return jsonify({
                "success": False,
                "error": "Translation could not be generated."
            }), 500

        return jsonify({
            "success": True,
            "translation": translation
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "success": False,
            "error": "Translation service is currently unavailable."
        }), 503

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
'@ | Set-Content -Encoding UTF8 ".\app.py"
