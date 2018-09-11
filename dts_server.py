from flask import Flask, jsonify


app = Flask(__name__)


BASE_PATH = "/"  # often "/dts/api/" in spec examples

COLLECTIONS_PATH = f"{BASE_PATH}collections/"
DOCUMENTS_PATH = f"{BASE_PATH}documents/"
NAVIGATION_PATH = f"{BASE_PATH}navigation/"


BASE_API_ENDPOINT = {
  "@context": f"{BASE_PATH}contexts/EntryPoint.jsonld",
  "@id": BASE_PATH,
  "@type": "EntryPoint",
  "collections": COLLECTIONS_PATH,
  "documents": DOCUMENTS_PATH,
  "navigation" : NAVIGATION_PATH,
}

@app.route(BASE_PATH)
def base_api_endpoint():
    # @@@ actually needs to return with content type of "application/ld+json"
    return jsonify(BASE_API_ENDPOINT)
