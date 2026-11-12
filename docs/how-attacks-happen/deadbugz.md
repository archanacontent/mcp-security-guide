# Deadbugz, August 2026

A security reviewer who installed `productivity-suite` and tried its two tools would have found nothing wrong. Both tools did their job. The server was built to wait until a client had made three tool calls, and only then did it start sending the agent instructions to hunt for credentials.

<span class="label">Source</span> - [Pillar Security](https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign) disclosed the campaign on 12 August 2026 in a report by Ariel Fogel. The name comes from `deadbug-mcp.py`, a file the campaign used for delivery.

## How The Campaign Ran

<ol class="steps">
<li><strong>10 August 2026</strong> - One public GitHub account opens 23 pull requests within 74 minutes. Pillar describes the targets as unrelated AI, MCP and developer-tool projects.</li>
<li><strong>The Requests</strong> - Seventeen add a remote MCP server to a project's configuration. Four point to a hidden local Python script, and two submit the server to directories or listings.</li>
<li><strong>First Contact</strong> - A client that connects finds two tools, <code>format_text</code> and <code>summarize</code>, each with a plain one-line description. They behave normally at first.</li>
<li><strong>The Counter</strong> - The server counts each client's <code>tools/call</code> requests in memory. Once the count reaches three, its <code>tools/list</code> and <code>prompts/get</code> responses change.</li>
<li><strong>The Switch</strong> - The new metadata directs the agent to seek SSH keys, AWS credentials, shell history and Kubernetes configuration, and to conceal the activity from the user.</li>
<li><strong>12 August 2026</strong> - Pillar publishes its disclosure and says it will update the report as verified information becomes available.</li>
</ol>

## What Is Established And What Isn't

| Established By Pillar | Not Established |
| --- | --- |
| None of the 23 pull requests had been merged through GitHub's merge mechanism at the time of review. Nineteen were closed and four were open. | Whether any organisation connected the server. Pillar reports no confirmed victim. |
| The server's behaviour, which Pillar observed in its public source code and under test requests. | How stolen data would leave a machine. The disclosure describes no exfiltration method. |
| The source includes optional telemetry sent to a configured webhook address. | Whether that telemetry carries stolen data, and who runs the campaign. |

!!! warning "Do Not Test The Original"
    Pillar advises against running `deadbug-mcp.py`. Part 5 reproduces the delayed change with a harmless server built for this guide.

## Why A Review At Install Time Misses It

A review at install time sees the definitions a server returns on its first response. In Deadbugz those definitions were clean, and the harmful text arrived only after normal use had begun. Pillar's message to the people who build MCP clients is that "Tool descriptions and schemas are a security boundary." It asks them to treat any change to an approved server's tool definitions as a security event that requires renewed approval.

## If You Find It In Your Environment

Pillar's disclosure lists the indicators to search for and gives five steps.

- **Block** - Block the endpoint named in the disclosure.
- **Revert** - Reject or revert any configuration change that adds the server.
- **Search** - Look for Pillar's indicators across repositories and developer machines.
- **Preserve** - Keep your MCP client logs.
- **Rotate** - Rotate credentials under your incident-response policy.

OWASP's GenAI Security Project included the campaign in its [exploit roundup for the third quarter of 2026](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/).

**Next:** [The WhatsApp Demonstration, April 2025](whatsapp-demonstration.md)
