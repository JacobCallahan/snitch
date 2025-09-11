"""Provides a simple HTTP server to expose Snitch status."""

import http.server
import json
import socketserver

from snitch.logging import logger
from snitch.state import load_state


def serve_api(port=8000):
    """Serve the state file over a simple HTTP API."""

    class StateHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/status":
                try:
                    state = load_state()
                    if not state:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(b'{"error": "State file not found. Run check."}')
                        return

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(state, indent=4).encode("utf-8"))
                except OSError as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f'{{"error": "Could not process request: {e}"}}'.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Not Found. Use /status"}')

    with socketserver.TCPServer(("", port), StateHandler) as httpd:
        logger.info(f"Serving Snitch API on port {port}...")
        logger.info(f"Access status at http://localhost:{port}/status")
        httpd.serve_forever()
