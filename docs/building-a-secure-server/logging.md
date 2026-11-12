# Logging After The July Change

After an incident, the first question is which tool ran, for which user and with which arguments. A server that can't answer has the gap OWASP lists as MCP08, Lack of Audit and Telemetry. Revision 2026-07-28 adds a second reason to review your logging, because it deprecated the protocol's own Logging feature.

<span class="label">Source</span> - Protocol changes come from the specification's [list of changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog) and its [stdio transport page](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio). Quoted logging advice comes from OWASP's [server development guide](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/).

## What Changed

| Item | Revision 2026-07-28 |
| --- | --- |
| **`logging/setLevel`** | Removed. |
| **Log Level** | Set per request through `io.modelcontextprotocol/logLevel` in `_meta`. Servers MUST NOT emit `notifications/message` for requests that did not include the field. |
| **Logging Feature** | Deprecated. It stays functional during the deprecation window, and new implementations should not add support for it. |
| **Suggested Migration** | Log to `stderr` on stdio, or use OpenTelemetry. |
| **Deprecation Window** | At least twelve months, under the specification's new feature lifecycle policy. |
| **Trace Context** | The revision documents OpenTelemetry trace context conventions for the `_meta` fields `traceparent`, `tracestate` and `baggage`. |

## Where Logs Go Now

=== "stdio"

    The server MAY write UTF-8 strings to `stderr` for any logging purpose. It MUST NOT write anything to `stdout` that is not a valid MCP message, so a stray print statement there breaks the protocol stream.

    The client MAY capture, forward or ignore the server's `stderr` output. A log line written only to `stderr` can therefore disappear, and audit records need a second destination that your team controls.

=== "Streamable HTTP"

    OpenTelemetry is the specification's suggested route. OWASP's guide adds the destination and says to "Feed MCP server audit logs into a centralized monitoring system (SIEM)."

## What To Record

- **Tool Calls** - "Log every action, including tool invocations (with parameters), resource access", in OWASP's words.
- **Scope Elevation** - MCP's [security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) tell servers to "Log elevation events (scope requested, granted subset) with correlation IDs".
- **Failed Validation** - OWASP's guide suggests real-time alerts "for suspicious patterns, such as a spike in failed validations".

## What To Keep Out

Tokens come first. The specification counts tokens "cached or logged on the server" among the ones attackers obtain. For everything else, OWASP's guide says to "Use field-level allowlists and redaction/hashing to prevent sensitive data from entering verbose logs."

The script [`audit_log.py`](https://github.com/archanacontent/mcp-security-guide/blob/main/examples/part-3/audit_log.py) writes one JSON line for each tool call and logs an argument in full only if the tool's allowlist names it.

```python title="An Audit Line With An Allowlist"
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
```

```text title="Output On stderr, 12 November 2026"
{"time": "2026-11-12T14:29:43Z", "event": "tools/call", "user": "user-17", "tool": "send_report", "arguments": {"report_id": "FR-2031", "api_key": "[REDACTED]"}, "is_error": false}
```

The call passed an `api_key` argument that the allowlist does not name, and the log line shows it redacted. Nothing was written to `stdout`.

OWASP's guide closes the loop on storage and says to "Store these logs securely and immutably for forensic analysis."
