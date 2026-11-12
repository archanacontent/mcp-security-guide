# Why The Model Reads Tool Definitions

Before a model can use a tool, the client asks the server for its tool list. The server answers with a definition for each tool, and the client passes those definitions to the model as context. Everything the model knows about a tool before the first call comes from text that the server's author wrote.

<ol class="steps">
<li>The client sends a <code>tools/list</code> request to the server.</li>
<li>The server returns its tool definitions.</li>
<li>The client passes the definitions to the model as context.</li>
<li>The model reads them and selects a tool for the user's request.</li>
<li>The client sends a <code>tools/call</code> request, and the server runs the tool.</li>
</ol>

## Inside A Tool Definition

The example below comes from the [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).

```json
{
  "name": "get_weather", // (1)!
  "title": "Weather Information Provider",
  "description": "Get current weather information for a location", // (2)!
  "inputSchema": { // (3)!
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code" // (4)!
      }
    },
    "required": ["location"]
  }
}
```

1.  The tool's unique identifier within one server.
2.  Free text from the server's author. The model reads it to decide when and how to call the tool.
3.  A JSON Schema that defines the parameters the tool expects.
4.  Parameter descriptions are free text too, and the model reads them as well.

A definition can also carry `annotations`, optional properties that describe the tool's behaviour. The specification requires clients to treat annotations as untrusted unless they come from a trusted server.

## Text That Works As An Instruction

A description is written for the model, and a model is built to follow natural-language instructions. [OWASP's MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) names the resulting risk tool poisoning, where malicious instructions hidden in tool descriptions, parameter schemas or return values manipulate the model's behaviour. OWASP advises treating the whole schema as a possible injection surface, parameter names and types included.

!!! example "Research Demonstration, April 2025"
    [Invariant Labs](https://invariantlabs.ai/blog/whatsapp-mcp-exploited) built a test server with one tool, `get_fact_of_the_day`. Its description told the agent to change the recipient of any WhatsApp message sent through a second, trusted server. In the researchers' demonstration, the agent sent the user's WhatsApp chat data to a number they controlled. Nobody was attacked, and the work was a proof of concept. Part 2 walks through it step by step.

## One Server Can Steer Another's Tools

The model sees tool descriptions from every connected server in the same context, as OWASP's cheat sheet points out. A description from one server can therefore change how the agent uses a tool from another, a risk OWASP lists as tool shadowing. In the Invariant Labs test, the untrusted server never touched WhatsApp itself.

## Definitions Can Change

A tool list isn't fixed. The specification allows the set of tools to change over time, and a server that declares `listChanged` should notify clients that subscribed to updates. OWASP uses the term rug pull for the harmful case, where a server changes its tool definitions after the user's initial approval.

!!! tip "The Practical Consequence"
    Reviewing a server's tools once tells you what they said on that day. Part 5 covers how to record approved definitions and detect a change.

**Next:** [What The Protocol Leaves To You](what-the-protocol-leaves.md)
