# Cybersecurity For AI Agents - MCP Security Guide

AI agents now reach company files, databases and internal tools through the Model Context Protocol (MCP). Its maintainers state in the [specification](https://modelcontextprotocol.io/specification/2026-07-28) that MCP cannot enforce its own security principles at the protocol level. Whoever deploys it carries that duty.

**Read the guide:** [archanacontent.github.io/mcp-security-guide](https://archanacontent.github.io/mcp-security-guide/)

## The Problem

What Changed - Through MCP, a language model can query databases, call APIs and run computations on systems outside the chat window. The specification describes tools as model-controlled, so the model finds and invokes them on its own from the user's prompt.

What Breaks - Each server supplies the text that describes its tools, and the model reads that text when it chooses what to do. Some clients showed a tool's description once at approval and gave no notice when it later changed, as [Invariant Labs reported](https://invariantlabs.ai/blog/whatsapp-mcp-exploited) in April 2025.

Real Example - On 10 August 2026, one GitHub account opened 23 pull requests in 74 minutes to spread an MCP server named `productivity-suite`. After a client's third tool call, its tool descriptions changed and directed the connected agent to seek SSH keys and AWS credentials. [Pillar Security](https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign) disclosed the campaign and found none of the pull requests merged when it reviewed them.

## What The Guide Covers

- **Part 1** - How MCP Works And Where Trust Breaks. Published.
- **Part 2** - How Attacks Happen, with three documented cases. Published.
- **Part 3** - Building A Secure Server. In progress.
- **Part 4** - Connecting Servers Safely. Planned.
- **Part 5** - Running MCP Over Time. Planned.
- **Part 6** - Reference. Planned.

## How It Is Built

- **Sources** - Protocol statements are checked against MCP specification revision 2026-07-28. Incident details come from the researchers who first reported them, and every page links its sources.
- **Docs-As-Code** - The pages are written in Markdown and built with MkDocs and the Material theme. A GitHub Actions workflow publishes the site on every push to `main`.
- **First-Visit Tour** - The tour on the home page is defined in `docs/assets/tour.json`, so its steps can change without touching the script.

## Author

Archana Panda, Senior Technical Writer and B2B Content Marketer. Portfolio: [archanacontent.github.io](https://archanacontent.github.io)
