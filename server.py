from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
from urllib.parse import urlparse, parse_qs

HOST = "0.0.0.0"
PORT = 8000

class Handler(BaseHTTPRequestHandler):
        def _set_headers(self):
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def do_OPTIONS(self):
                self.send_response(200)
                self._set_headers()
                self.end_headers()

        def do_POST(self):
                if self.path != "/query":
                        self.send_response(404)
                        self.end_headers()
                        return

                length = int(self.headers['Content-Length'])
                body = self.rfile.read(length)
                data = json.loads(body)
                prompt = data.get("prompt","")

                result = subprocess.run(
                        ["llama.cpp/build/bin/llama-simple", "-m", "llama.cpp/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", "-p", prompt],
                        capture_output=True, text=True
                )
                response = {"response": result.stdout}
                self.send_response(200)
                self._set_headers()
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))

httpd = HTTPServer((HOST,PORT), Handler)
print(f"Server running on http://{HOST}:{PORT}")
httpd.serve_forever()