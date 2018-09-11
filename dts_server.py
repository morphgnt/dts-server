from json import dumps

from flask import Flask, request, Response

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
    return Response(dumps(BASE_API_ENDPOINT), mimetype="application/ld+json")


COLLECTION_BASE = {
    "@context": {
        "@vocab": "https://www.w3.org/ns/hydra/core#",
        "dc": "http://purl.org/dc/terms/",
        "dts": "https://w3id.org/dts/api#"
    },
    "@type" : "Collection",
}

SBLGNT_DOCUMENTS = [
    {"@id": "61-Mt-morphgnt.txt"},
    {"@id": "62-Mk-morphgnt.txt"},
    {"@id": "63-Lk-morphgnt.txt"},
    {"@id": "64-Jn-morphgnt.txt"},
    {"@id": "65-Ac-morphgnt.txt"},
    {"@id": "66-Ro-morphgnt.txt"},
    {"@id": "67-1Co-morphgnt.txt"},
    {"@id": "68-2Co-morphgnt.txt"},
    {"@id": "69-Ga-morphgnt.txt"},
    {"@id": "70-Eph-morphgnt.txt"},
    {"@id": "71-Php-morphgnt.txt"},
    {"@id": "72-Col-morphgnt.txt"},
    {"@id": "73-1Th-morphgnt.txt"},
    {"@id": "74-2Th-morphgnt.txt"},
    {"@id": "75-1Ti-morphgnt.txt"},
    {"@id": "76-2Ti-morphgnt.txt"},
    {"@id": "77-Tit-morphgnt.txt"},
    {"@id": "78-Phm-morphgnt.txt"},
    {"@id": "79-Heb-morphgnt.txt"},
    {"@id": "80-Jas-morphgnt.txt"},
    {"@id": "81-1Pe-morphgnt.txt"},
    {"@id": "82-2Pe-morphgnt.txt"},
    {"@id": "83-1Jn-morphgnt.txt"},
    {"@id": "84-2Jn-morphgnt.txt"},
    {"@id": "85-3Jn-morphgnt.txt"},
    {"@id": "86-Jud-morphgnt.txt"},
    {"@id": "87-Re-morphgnt.txt"},
]

SBLGNT_COLLECTION = {
    **COLLECTION_BASE,
    "@id" : "SBLGNT",
    "title" : "SBL Greek New Testament",
    "totalItems" : len(SBLGNT_DOCUMENTS),
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

DOCUMENTS = {
    d["@id"]: d
    for d in SBLGNT_DOCUMENTS
}

@app.route(COLLECTIONS_PATH)
def collections_endpoint():
    collection_id = request.args.get("id", ROOT_COLLECTION["@id"])
    try:
        collection = COLLECTIONS[collection_id]
        response = Response(dumps(collection), mimetype="application/ld+json")
    except KeyError:
        response = Response(dumps({
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "@type": "Error",
            "title": "Unknown collection",
            "description": f"No collection with @id = '{collection_id}'",
        }), status=404, mimetype="application/ld+json")
    return response


@app.route(DOCUMENTS_PATH)
def documents_endpoint():
    document_id = request.args.get("id")
    if document_id is None:
        response = Response(dumps({
            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
            "@type": "Error",
            "title": "No document id provided",
        }), status=404, mimetype="application/ld+json")
    else:
        try:
            document = DOCUMENTS[document_id]
            data = """<?xml version="1.0" encoding="UTF-8"?>
    TEI xmlns="http://www.tei-c.org/ns/1.0">
    """
            with open("data/" + document_id) as f:
                for line in f:
                    bcv, rest = line.split(maxsplit=1)
                    data += rest
            data += "</TEI>"
            response = Response(data, mimetype="application/tei+xml")
        except KeyError:
            response = Response(dumps({
                "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                "@type": "Error",
                "title": "Unknown document",
                "description": f"No document with @id = '{document_id}'",
            }), status=404, mimetype="application/ld+json")
    return response
