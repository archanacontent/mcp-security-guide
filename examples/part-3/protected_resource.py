"""The HTTP authorization layer of a remote MCP server, reduced to two duties:
publish Protected Resource Metadata (RFC 9728) and challenge requests that
carry no token. It is a teaching example, not a full MCP server."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

RESOURCE = "https://mcp.example.com"
METADATA_URL = RESOURCE + "/.well-known/oauth-protected-resource"
METADATA = {
    "resource": RESOURCE,
    "authorization_servers": ["https://auth.example.com"],
    "scopes_supported": ["reports:read"],
    "bearer_methods_supported": ["header"],
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/.well-known/oauth-protected-resource":
            body = json.dumps(METADATA).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            self.send_response(401)
            self.send_header(
                "WWW-Authenticate",
                f'Bearer resource_metadata="{METADATA_URL}", scope="reports:read"',
            )
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.send_error(501, "Token validation is shown in validate_token.py")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8900), Handler).serve_forever()
