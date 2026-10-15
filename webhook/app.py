"""
Minimal Instagram webhook receiver for Meta.

It does two things and nothing else:
  GET  /webhook  -> answers Meta's verification challenge
  POST /webhook  -> checks the request signature, logs a safe summary, returns 200

It does NOT send DMs, reply to comments, or publish anything.
"""

import hashlib
import hmac
import json
import logging
import os

from flask import Flask, Response, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("instagram-webhook")


@app.get("/")
def health():
    # Lets you (and Render) check that the server is awake. Returns no secrets.
    return "ok", 200


@app.get("/webhook")
def verify_webhook():
    """Meta calls this when you save the callback URL in the Meta app dashboard."""
    expected_token = os.environ.get("META_VERIFY_TOKEN", "")
    if not expected_token:
        log.error("META_VERIFY_TOKEN is not set. Verification refused.")
        return "server not configured", 500

    mode = request.args.get("hub.mode", "")
    token = request.args.get("hub.verify_token", "")
    challenge = request.args.get("hub.challenge", "")

    token_ok = hmac.compare_digest(token.encode("utf-8"), expected_token.encode("utf-8"))
    if mode == "subscribe" and token_ok:
        log.info("Webhook verification succeeded.")
        return Response(challenge, status=200, mimetype="text/plain")

    log.warning("Webhook verification failed (mode=%s).", mode or "missing")
    return "forbidden", 403


@app.post("/webhook")
def receive_event():
    """Meta calls this for every event on the fields you subscribe to."""
    app_secret = os.environ.get("META_APP_SECRET", "")
    if not app_secret:
        log.error("META_APP_SECRET is not set. Events refused.")
        return "server not configured", 500

    # The signature is computed over the exact raw bytes Meta sent,
    # so read the raw body before any JSON parsing.
    raw_body = request.get_data()
    received_sig = request.headers.get("X-Hub-Signature-256", "")
    expected_sig = "sha256=" + hmac.new(
        app_secret.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(received_sig.encode("utf-8"), expected_sig.encode("utf-8")):
        log.warning("Rejected event: signature missing or does not match.")
        return "forbidden", 403

    try:
        payload = json.loads(raw_body)
    except ValueError:
        log.warning("Rejected event: body is not valid JSON.")
        return "bad request", 400

    log_event_summary(payload)
    return "EVENT_RECEIVED", 200


def log_event_summary(payload):
    """Log only metadata: object type, account id, and which fields changed.
    Comment text, message text, and user details are never logged."""
    try:
        obj = payload.get("object", "unknown")
        for entry in payload.get("entry", []):
            fields = [change.get("field", "unknown") for change in entry.get("changes", [])]
            if entry.get("messaging"):
                fields.append("messaging")
            log.info(
                "Event received: object=%s account_id=%s fields=%s",
                obj,
                entry.get("id", "unknown"),
                ",".join(fields) or "none",
            )
    except (AttributeError, TypeError):
        log.info("Event received, but its shape was not recognised. Body not logged.")


if __name__ == "__main__":
    # Local testing only. On Render, gunicorn runs the app (see README.md).
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
