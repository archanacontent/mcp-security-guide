# What The Protocol Leaves To You

MCP's maintainers wrote a plain admission into the [specification](https://modelcontextprotocol.io/specification/2026-07-28). The protocol, they state, cannot enforce its security principles at the protocol level. They sort every requirement with fixed keywords, and the gap between MUST, SHOULD and OPTIONAL marks where your own work begins.

## Reading The Keywords

The keywords follow [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and carry their formal meaning only in capitals.

=== "MUST"

    An absolute requirement. An implementation that skips it does not conform to the specification.

=== "SHOULD"

    A recommendation. RFC 2119 accepts that valid reasons may exist to ignore it in particular circumstances.

=== "OPTIONAL"

    A free choice. One vendor may include the item and another may leave it out.

## Where The Specification Stops

| Area | What The Specification States | Left To Your Team |
| --- | --- | --- |
| **Authorization** | [OPTIONAL](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) for MCP implementations. HTTP-based transports SHOULD follow the authorization specification when they support it. | Requiring it on every remote server that exposes non-public tools or data. |
| **Human Approval** | There [SHOULD](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) always be a human in the loop with the ability to deny tool invocations. | Choosing which actions need confirmation, and checking that your host asks for it. |
| **Tool Annotations** | Clients MUST consider them untrusted unless they come from trusted servers. | Deciding which servers your organisation trusts, and on what evidence. |
| **Tool Inputs And Outputs** | Servers MUST validate all tool inputs, implement access controls, rate limit invocations and sanitize outputs. | Confirming that a server you didn't write does so. |
| **Audit Logs** | Clients SHOULD log tool usage for audit purposes. | Verifying that your host keeps those logs and that someone reviews them. |
| **Local Server Setup** | A client with one-click setup [MUST](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) show the exact command without truncation and require explicit approval. | Reading the command before anyone approves it. |

!!! note "A Requirement Binds Only Those Who Follow It"
    A MUST tells an honest developer what to build. A hostile server's author has no reason to comply, so each requirement placed on servers still needs a check from your side.

## A Specification That Keeps Moving

MCP's rules change between revisions. [Revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog) removed protocol-level sessions and the `initialize` handshake, and every request now carries its own protocol version and client capabilities. Security advice built around session IDs applies to revision 2025-11-25 and earlier.

The same revision deprecated Dynamic Client Registration in favour of Client ID Metadata Documents, and it deprecated the protocol's Logging feature. Before you apply any published guidance, check which revision your host and servers implement.
