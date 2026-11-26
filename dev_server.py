"""Local preview server for まなび時刻表.

The page file has no <!doctype>/<head> of its own: when it is published as an
Artifact, the platform wraps it in a small skeleton (charset, viewport, a reset
with [hidden]{display:none!important}). This server adds the same skeleton so
the local preview looks and behaves like the published page.

Run:  python3 dev_server.py      (then open http://localhost:8080)
"""
import http.server
import os

PORT = int(os.environ.get("PORT", "8080"))
ROOT = os.path.dirname(os.path.abspath(__file__))
START_PAGE = "/index.html"
SKELETON_HEAD = (
    '<!doctype html><html><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0;font:14px/1.4 system-ui,sans-serif}img{max-width:100%}"
    "[hidden]{display:none!important}</style></head><body>"
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] in ("", "/"):
            self.send_response(302)
            self.send_header("Location", START_PAGE)
            self.end_headers()
            return
        path = self.translate_path(self.path)
        if path.endswith(".html") and os.path.isfile(path):
            with open(path, "rb") as f:
                body = f.read()
            if not body.lstrip()[:9].lower().startswith(b"<!doctype"):
                body = SKELETON_HEAD.encode("utf-8") + body + b"</body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving まなび時刻表 at http://localhost:{PORT}{START_PAGE}", flush=True)
    server.serve_forever()
