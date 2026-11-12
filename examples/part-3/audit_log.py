"""One JSON audit line for each tool call, written to stderr. Only argument
fields on the tool's allowlist are logged in full. On the stdio transport,
stdout carries protocol messages."""
import json
import sys
import time

LOGGED_FIELDS = {"send_report": {"report_id"}}


def audit(user_id, tool, arguments, is_error):
    allowed = LOGGED_FIELDS.get(tool, set())
    safe = {k: (v if k in allowed else "[REDACTED]") for k, v in arguments.items()}
    line = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": "tools/call",
        "user": user_id,
        "tool": tool,
        "arguments": safe,
        "is_error": is_error,
    }
    print(json.dumps(line), file=sys.stderr)


if __name__ == "__main__":
    audit("user-17", "send_report", {"report_id": "FR-2031", "api_key": "sk-live-123"}, False)
