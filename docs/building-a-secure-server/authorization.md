# Authorization Under The 2026-07-28 Spec

A remote MCP server without authorization answers any client that can reach its address. The specification still lists authorization as OPTIONAL, so nothing in the protocol stops a team from shipping one. OWASP's [server development guide](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/) takes the firmer line and says to "Treat authentication as mandatory for all remote MCP servers."

<span class="label">Source</span> - Requirements on this page come from the [authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) and its [security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations) for revision 2026-07-28. OWASP published its guide in February 2026, before that revision.

## Which Rules Apply To Your Server

| Transport | What The Specification Says |
| --- | --- |
| **Streamable HTTP** | An implementation that supports authorization SHOULD conform to the authorization specification. |
| **stdio** | It SHOULD NOT follow that specification, and retrieves credentials from the environment instead. |
| **Any Other Transport** | It MUST follow established security best practices for its protocol. |

!!! note "Two Sources, Two Positions On Environment Variables"
    The specification points stdio servers to the environment for credentials. OWASP's guide says "Do not store secrets in environment variables, logs or plain-text in code", and its checklist asks for secrets to be stored in vaults. If your stdio server reads a credential from its environment, settle where that value is kept before launch and who can read it.

## Your Server's Role

In OAuth terms, a protected MCP server is a resource server. It accepts access tokens and answers requests that carry a valid one. An authorization server signs the user in and issues those tokens, and the specification allows it to be hosted with your server or run as a separate service.

## Three Duties On Every Remote Server

<ol class="steps">
<li><strong>Publish Protected Resource Metadata</strong> - MCP servers MUST implement OAuth 2.0 Protected Resource Metadata (RFC 9728). The document names your server and the authorization servers it relies on.</li>
<li><strong>Challenge Requests That Carry No Token</strong> - Answer with HTTP 401 and a <code>WWW-Authenticate</code> header. The client reads the address of your metadata from that header. Your server SHOULD add a <code>scope</code> value, which tells the client the scopes to request.</li>
<li><strong>Validate Every Token</strong> - Authorization MUST be included in every HTTP request from client to server, and your server MUST validate each token. <a href="../tokens-and-scopes/">Tokens And Scopes</a> covers the checks.</li>
</ol>

## A Tested Example

The guide's repository holds a small script, [`protected_resource.py`](https://github.com/archanacontent/mcp-security-guide/blob/main/examples/part-3/protected_resource.py), that performs the first two duties. It is a teaching example and leaves out the rest of an MCP server.

```python title="The Metadata Document"
RESOURCE = "https://mcp.example.com"
METADATA_URL = RESOURCE + "/.well-known/oauth-protected-resource"
METADATA = {
    "resource": RESOURCE,
    "authorization_servers": ["https://auth.example.com"],
    "scopes_supported": ["reports:read"],
    "bearer_methods_supported": ["header"],
}
```

```python title="The Challenge"
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
```

A request for the metadata and a request without a token returned the following on 12 November 2026.

```text title="Output"
200 {"resource": "https://mcp.example.com", "authorization_servers": ["https://auth.example.com"], "scopes_supported": ["reports:read"], "bearer_methods_supported": ["header"]}
401 Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource", scope="reports:read"
```

## What Changed For Authorization In July 2026

| Area | Revision 2026-07-28 |
| --- | --- |
| **Client Registration** | Authorization servers and clients SHOULD support Client ID Metadata Documents. Dynamic Client Registration is deprecated and kept for backwards compatibility. |
| **Issuer Check** | Authorization servers SHOULD include the `iss` parameter in authorization responses, and clients MUST validate a present `iss` before they redeem the authorization code. The specification expects a future revision to raise that SHOULD to a MUST. |
| **Client Credentials** | Clients MUST store credentials under the issuer that granted them and MUST NOT reuse them with a different authorization server. |

## Questions For Your Authorization Server

Most of the authorization rules bind the authorization server and the client. Your team still picks the authorization server, so check it against the specification before you connect it.

| Check | Requirement In The Specification |
| --- | --- |
| **OAuth 2.1** | It MUST implement OAuth 2.1 with security measures for confidential and public clients. |
| **Discovery** | It MUST provide OAuth 2.0 Authorization Server Metadata (RFC 8414) or OpenID Connect Discovery 1.0. |
| **PKCE** | Its metadata has to list `code_challenge_methods_supported`. Clients MUST refuse to proceed if the field is absent. |
| **HTTPS** | All of its endpoints MUST be served over HTTPS. |
| **Redirect URIs** | It MUST validate exact redirect URIs against pre-registered values. |
| **Token Lifetime** | It SHOULD issue short-lived access tokens. |
| **Refresh Tokens** | It MUST rotate refresh tokens for public clients. |

**Next:** [Tokens And Scopes](tokens-and-scopes.md)
