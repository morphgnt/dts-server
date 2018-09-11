from flask import Flask, jsonify, request


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


COLLECTION_BASE = {
    "@context": {
        "@vocab": "https://www.w3.org/ns/hydra/core#",
        "dc": "http://purl.org/dc/terms/",
        "dts": "https://w3id.org/dts/api#"
    },
    "@type" : "Collection",
}

SBLGNT_COLLECTION = {
    **COLLECTION_BASE,
    "@id" : "SBLGNT",
    "title" : "SBL Greek New Testament",
    "totalItems" : 27,
}

MORPHGNT_DTS_SERVER_COLLECTIONS = [SBLGNT_COLLECTION]

ROOT_COLLECTION = {
    **COLLECTION_BASE,
    "@id": "root",
    "title": "MorphGNT DTS Server Collection",
    "totalItems": len(MORPHGNT_DTS_SERVER_COLLECTIONS),
    "member": MORPHGNT_DTS_SERVER_COLLECTIONS,
}

COLLECTIONS = {
    c["@id"]: c for c in [
        ROOT_COLLECTION,
        SBLGNT_COLLECTION,
    ]
}

@app.route(COLLECTIONS_PATH)
def collections_endpoint():
    # @@@ actually needs to return with content type of "application/ld+json"
    collection_id = request.args.get("id", ROOT_COLLECTION["@id"])
    collection = COLLECTIONS[collection_id]
    return jsonify(collection)
