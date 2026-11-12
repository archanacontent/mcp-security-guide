# The Three Roles: Host, Client, Server

A developer adds a few lines to a configuration file, and an AI assistant gains a new connection to company data. Behind those lines sit a host, a client and a server. Each holds a different share of the security work, and the [MCP architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture) assigns most of it to the host.

<figure class="diagram">
<svg viewBox="0 0 400 330" role="img" aria-label="A host application contains three clients. Each client connects to exactly one server. Two servers run as local processes and one runs as a remote service.">
<rect class="dg-host" x="10" y="10" width="380" height="150" rx="10"/>
<text class="dg-accent" x="24" y="32">HOST</text>
<text class="dg-sub" x="24" y="50">The AI application. Holds the model and the full conversation.</text>
<rect class="dg-box" x="24" y="88" width="104" height="52" rx="6"/>
<text class="dg-text" x="76" y="119" text-anchor="middle">Client 1</text>
<rect class="dg-box" x="148" y="88" width="104" height="52" rx="6"/>
<text class="dg-text" x="200" y="119" text-anchor="middle">Client 2</text>
<rect class="dg-box" x="272" y="88" width="104" height="52" rx="6"/>
<text class="dg-text" x="324" y="119" text-anchor="middle">Client 3</text>
<path class="dg-line" d="M76 140 V236"/>
<path class="dg-line" d="M200 140 V236"/>
<path class="dg-line" d="M324 140 V236"/>
<text class="dg-sub" x="82" y="194">stdio</text>
<text class="dg-sub" x="206" y="194">stdio</text>
<text class="dg-sub" x="330" y="188">Streamable</text>
<text class="dg-sub" x="330" y="202">HTTP</text>
<rect class="dg-box" x="24" y="236" width="104" height="80" rx="6"/>
<text class="dg-text" x="76" y="262" text-anchor="middle">Server</text>
<text class="dg-sub" x="76" y="282" text-anchor="middle">Files</text>
<text class="dg-accent" x="76" y="302" text-anchor="middle">LOCAL</text>
<rect class="dg-box" x="148" y="236" width="104" height="80" rx="6"/>
<text class="dg-text" x="200" y="262" text-anchor="middle">Server</text>
<text class="dg-sub" x="200" y="282" text-anchor="middle">Database</text>
<text class="dg-accent" x="200" y="302" text-anchor="middle">LOCAL</text>
<rect class="dg-box" x="272" y="236" width="104" height="80" rx="6"/>
<text class="dg-text" x="324" y="262" text-anchor="middle">Server</text>
<text class="dg-sub" x="324" y="282" text-anchor="middle">External API</text>
<text class="dg-accent" x="324" y="302" text-anchor="middle">REMOTE</text>
</svg>
<figcaption>One host, one client for each server. Adapted from the MCP architecture page.</figcaption>
</figure>

## Who Does What

| Role | What It Is | Its Security Job In The Specification |
| --- | --- | --- |
| **Host** | Your developers open the host every day. It's the AI application itself, a chat interface or an AI code editor for example, and it creates one client for every server they connect. | Most of the load sits here. A host enforces security policies and consent requirements, controls each client's connection permissions and handles the user's authorization decisions. |
| **Client** | Three connected servers mean three clients. A client is a connector that lives inside the host and talks to exactly one server. | Maintains the security boundaries between servers. |
| **Server** | The program behind the tools. It runs as a local process on the user's machine or as a remote service, and it exposes resources, prompts and tools to the client. | Must respect security constraints. Where it offers tools, the specification says a server MUST validate all inputs, implement access controls, rate limit invocations and sanitize outputs. |

MCP's design principles state that a server should not be able to read the whole conversation or see into other servers. The full conversation history stays with the host, and the host process enforces the boundaries.

There's a limit to that promise. The specification adds that MCP cannot enforce its security principles at the protocol level, so your protection depends on how the host your developers chose was built.

## Local And Remote Servers

A server runs either as a local process on the user's machine or as a remote service. Local servers usually communicate over `stdio`, the standard input and output streams of a process the client launches. Remote servers use Streamable HTTP, and the older HTTP+SSE transport is deprecated.

!!! warning "A Local Server Runs With The User's Access"
    [OWASP's MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) notes that `stdio` avoids a listening endpoint. It does nothing to restrict the server process's access to files, the network or credentials. MCP's own [security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) asks clients to warn that a local server runs with the same privileges as the client.

## What A Server Can Offer

=== "Tools"

    Functions for the AI model to execute. A tool can query a database, call an API or perform a computation.

=== "Resources"

    Context and data, for the user or the AI model to use.

=== "Prompts"

    Templated messages and workflows for users.

The specification singles out tools. It states that they represent arbitrary code execution and must be treated with appropriate caution.

**Next:** [Why The Model Reads Tool Definitions](tool-definitions.md)
