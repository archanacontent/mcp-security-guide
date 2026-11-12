# Inputs, Outputs And State Handles

The model writes every tool argument your server receives. Part 2 showed how text from an untrusted source can steer a model, so an argument can carry whatever an attacker managed to put in front of it. The [tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) answers with four duties.

<div class="cards stats">
<div class="card"><span class="num">SERVERS MUST</span><strong>Validate all tool inputs</strong></div>
<div class="card"><span class="num">SERVERS MUST</span><strong>Implement proper access controls</strong></div>
<div class="card"><span class="num">SERVERS MUST</span><strong>Rate limit tool invocations</strong></div>
<div class="card"><span class="num">SERVERS MUST</span><strong>Sanitize tool outputs</strong></div>
</div>

## Validate Inputs Against The Schema

Every tool already declares an `inputSchema`. OWASP's [server development guide](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/) asks teams to enforce it and to "Reject any request that doesn't match the expected schema."

The specification separates two kinds of error, and the choice affects whether the model can recover.

| Error Kind | Examples In The Specification | How It Is Returned |
| --- | --- | --- |
| **Protocol Error** | Unknown tool, malformed request, server error | A standard JSON-RPC error |
| **Tool Execution Error** | API failure, input validation error, business logic error | A tool result with `isError: true` |

Input validation errors sit in the second row. The specification says tool execution errors "contain actionable feedback that language models can use to self-correct and retry with adjusted parameters."

The script [`validate_input.py`](https://github.com/archanacontent/mcp-security-guide/blob/main/examples/part-3/validate_input.py) validates three sets of arguments against one schema.

```python title="Schema Validation With A Tool Execution Error"
INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "report_id": {"type": "string", "pattern": "^[A-Z]{2}-[0-9]{4}$"}
    },
    "required": ["report_id"],
    "additionalProperties": False,
}
validator = Draft202012Validator(INPUT_SCHEMA)


def call_read_report(arguments):
    errors = [error.message for error in validator.iter_errors(arguments)]
    if errors:
        return {
            "resultType": "complete",
            "content": [{"type": "text", "text": "Invalid arguments: " + "; ".join(errors)}],
            "isError": True,
        }
    return {
        "resultType": "complete",
        "content": [{"type": "text", "text": f"Report {arguments['report_id']} loaded."}],
        "isError": False,
    }
```

```text title="Output, 12 November 2026"
{"report_id": "FR-2031"} -> {"resultType": "complete", "content": [{"type": "text", "text": "Report FR-2031 loaded."}], "isError": false}
{"report_id": "../../etc/passwd"} -> {"resultType": "complete", "content": [{"type": "text", "text": "Invalid arguments: '../../etc/passwd' does not match '^[A-Z]{2}-[0-9]{4}$'"}], "isError": true}
{"report_id": "FR-2031", "debug": true} -> {"resultType": "complete", "content": [{"type": "text", "text": "Invalid arguments: Additional properties are not allowed ('debug' was unexpected)"}], "isError": true}
```

The third call fails because the schema sets `additionalProperties` to `false`, so a field the tool never declared is refused.

## Keep Outputs Tight

A tool's output goes back into the model's context, and from there it can reach the user or another tool.

- **Schema** - If a tool declares an `outputSchema`, servers MUST provide structured results that conform to it.
- **Size** - OWASP's guide says to "Enforce size limits on all outputs from the tools or model."
- **Fields** - It also says to "Only expose minimal, strictly necessary fields to the model".
- **Errors** - "Do not return stack traces, tokens, filesystem paths, or tool internals in responses", in OWASP's words.

## Rate Limits

Rate limiting is one of the four duties, and the specification leaves the numbers to you. OWASP's guide asks teams to "Impose quotas and rate limits on tool invocations and data fetches per session."

## State Handles Replaced Sessions

Revision 2026-07-28 removed protocol-level sessions. A server that needs state across calls, such as a shopping basket, now returns an explicit handle from a creation tool and accepts it back as an ordinary argument. MCP's [security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) describe the attack that follows, in which someone obtains or guesses a handle and uses it to reach another user's state.

| Rule | Source Wording |
| --- | --- |
| **Possession Proves Nothing** | MCP servers MUST NOT treat possession of a state handle as authentication. |
| **Verify Each Request** | MCP servers that implement authorization MUST verify all inbound requests. |
| **Make Handles Unguessable** | Servers SHOULD use secure, non-deterministic handles generated with secure random number generators. |
| **Bind Handles To The User** | Servers SHOULD bind handles server-side to the authenticated user, with the user ID derived from the verified token. |
| **State The Lifetime** | The retention policy should be stated in the creation tool's description. |
| **Report Expiry** | A call against an expired or unknown handle should return a tool execution error that says so. |

The script [`state_handles.py`](https://github.com/archanacontent/mcp-security-guide/blob/main/examples/part-3/state_handles.py) stores each basket under the user ID and the handle together.

```python title="Handles Bound To The User"
baskets = {}


def create_basket(user_id):
    handle = "bsk_" + secrets.token_urlsafe(16)
    baskets[(user_id, handle)] = []
    return handle


def add_item(user_id, handle, sku):
    basket = baskets.get((user_id, handle))
    if basket is None:
        return {"isError": True, "text": "Unknown or expired basket. Create a new one."}
    basket.append(sku)
    return {"isError": False, "text": f"Added {sku}. Basket holds {len(basket)} item(s)."}
```

```text title="Output, 12 November 2026"
handle length: 26
owner: {'isError': False, 'text': 'Added SKU-1. Basket holds 1 item(s).'}
other user, same handle: {'isError': True, 'text': 'Unknown or expired basket. Create a new one.'}
```

A second user who presents the first user's handle gets the same answer as for a handle that never existed.

!!! note "Reading Guidance Written Before July 2026"
    OWASP's guide dates from February 2026 and speaks of sessions. Its rule "Never rely on session IDs alone for authorization or authentication" matches what the specification now says about state handles. For servers on revision 2025-11-25 or earlier, the best practices page links to its earlier guidance on session hijacking.

**Next:** [Logging After The July Change](logging.md)
