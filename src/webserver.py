# webserver.py
# Smart Door System — Flask Webserver (REST API + Webinterface)
# Autor: Ydriss Armel Demanou | Westfälische Hochschule Gelsenkirchen 2026

from flask import Flask, jsonify, request, Response
from functools import wraps
from config import WebConfig

def basic_auth_required(username: str, password: str):
    """HTTP Basic Auth Dekorator."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if not auth or auth.username != username or auth.password != password:
                return Response(
                    "Login noetig", 401,
                    {"WWW-Authenticate": 'Basic realm="SmartDoor"'}
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def create_app(state, actions, web_cfg: WebConfig):
    """
    Flask App erstellen.

    state:   dict-like (shared) -> Statuswerte (Tuer, LDR, Log, ...)
    actions: Objekt mit Methoden open_door(), close_door(), allow_bell()
    """
    app  = Flask(__name__)
    auth = basic_auth_required(web_cfg.USERNAME, web_cfg.PASSWORD)

    @app.get("/api/status")
    @auth
    def status():
        """Systemstatus abfragen."""
        return jsonify(state)

    @app.post("/api/door/open")
    @auth
    def door_open():
        """Tuer oeffnen (manuell via Web)."""
        actions.open_door()
        return jsonify({"ok": True})

    @app.post("/api/door/close")
    @auth
    def door_close():
        """Tuer schliessen."""
        actions.close_door()
        return jsonify({"ok": True})

    @app.post("/api/allow")
    @auth
    def allow():
        """Klingel-Freigabe: Besucher einlassen."""
        actions.allow_bell()
        return jsonify({"ok": True})

    return app
