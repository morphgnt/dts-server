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


COLLECTIONS = [
    {
         "@id" : "@@@",
         "title" : "SBL Greek New Testament",
         "@type" : "Collection",
         "totalItems" : 27,
    },
]

COLLECTIONS_ENDPOINT = {
    "@context": {
        "@vocab": "https://www.w3.org/ns/hydra/core#",
        "dc": "http://purl.org/dc/terms/",
        "dts": "https://w3id.org/dts/api#"
    },
    "@id": COLLECTIONS_PATH,
    "@type": "Collection",
    "totalItems": len(COLLECTIONS),
    "title": "MorphGNT DTS Server Collection",
    "member": COLLECTIONS,
}


@app.route(COLLECTIONS_PATH)
def collections_endpoint():
    # @@@ actually needs to return with content type of "application/ld+json"
    return jsonify(COLLECTIONS_ENDPOINT)
