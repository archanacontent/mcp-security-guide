# Tokens And Scopes

A valid token is not always a token meant for your server. If your server accepts one that was issued for a different service, a token stolen there works here too. Scopes carry the second risk, because a token that holds every scope turns one leak into access to every tool.

<span class="label">Source</span> - Requirements come from the [authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), its [security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations) and MCP's [security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices). Quoted advice from OWASP comes from its [server development guide](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/).

## Check Who The Token Was Issued For

MCP servers MUST validate that access tokens were issued specifically for them as the intended audience. Invalid or expired tokens MUST receive an HTTP 401 response. OWASP's guide lists the checks for each request: "validate iss, aud, exp, and signatures on every request."

The script [`validate_token.py`](https://github.com/archanacontent/mcp-security-guide/blob/main/examples/part-3/validate_token.py) signs two test tokens with a throwaway key and validates both.

```python title="Audience And Issuer Validation"
def validate(token, public_key):
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=RESOURCE,
        issuer=ISSUER,
        options={"require": ["exp", "aud", "iss"]},
    )
```

```text title="Output, 12 November 2026"
issued for this server: accepted
issued for another API: rejected, respond with HTTP 401 (Audience doesn't match)
```

## Never Pass A Client's Token Downstream

Many MCP servers call another API to do their work, and forwarding the client's token to that API looks like the short route. The specification calls it token passthrough and forbids it. An MCP server MUST NOT pass through the token it received from the MCP client. For upstream calls, the server acts as an OAuth client and uses a separate token issued by the upstream authorization server.

MCP's security best practices name four risks of passthrough.

- **Security Control Circumvention** - Clients can use tokens directly with downstream APIs and bypass rate limiting, request validation or traffic monitoring.
- **Accountability And Audit Trail Issues** - The MCP server cannot tell its clients apart, and downstream logs show requests under a different identity.
- **Trust Boundary Issues** - If several services accept the same token, an attacker who compromises one of them can reach the others.
- **Future Compatibility Risk** - A server that starts as a pure proxy may need security controls later, and separate token audiences make that change easier.

For delegation, OWASP's guide points to the OAuth token delegation flow in RFC 8693.

## Keep Scopes Small

The attack described in MCP's best practices starts with a server that lists every scope in `scopes_supported` and a client that requests them all. One stolen token then carries `files:*`, `db:*` and `admin:*`.

=== "At First Contact"

    Start with a minimal scope set that covers only low-risk discovery and read operations. The specification intends `scopes_supported` to be the minimal set needed for basic functionality. Servers SHOULD NOT include `offline_access` in it or in a `WWW-Authenticate` scope.

=== "At A Privileged Call"

    Answer with HTTP 403 and name the scopes the operation needs. Servers SHOULD include all scopes required for the current operation in a single challenge. The example below is the specification's own.

    ```http
    HTTP/1.1 403 Forbidden
    WWW-Authenticate: Bearer error="insufficient_scope",
                             scope="files:write",
                             resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                             error_description="File write permission required for this operation"
    ```

| Status Code | Usage In The Specification |
| --- | --- |
| **401 Unauthorized** | Authorization required or token invalid |
| **403 Forbidden** | Invalid scopes or insufficient permissions |
| **400 Bad Request** | Malformed authorization request |

## Scope Mistakes The Specification Names

- Publishing all possible scopes in `scopes_supported`
- Using wildcard or omnibus scopes (`*`, `all`, `full-access`)
- Bundling unrelated privileges to preempt future prompts
- Returning the entire scope catalog in every challenge
- Silent scope semantic changes without versioning
- Treating claimed scopes in a token as sufficient without server-side authorization logic

!!! warning "A Scope Is A Claim, And Your Server Still Decides"
    The last mistake on that list pairs with a server duty in the tools specification, which says servers MUST implement proper access controls. A scope in a token tells your server what was granted. Your own authorization logic decides whether this user may run this tool on this record.

## Token Lifetime

Authorization servers SHOULD issue short-lived access tokens to reduce the impact of a leak. OWASP's guide is more specific and asks for "minimal lifetimes (minutes) and narrow scopes." The specification also counts tokens "cached or logged on the server" among the ones attackers obtain, which is one reason [Logging After The July Change](logging.md) keeps tokens out of log lines.

**Next:** [Inputs, Outputs And State Handles](inputs-outputs-state.md)
