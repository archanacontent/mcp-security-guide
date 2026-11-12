<p class="eyebrow">MCP · Security Guide</p>

# Cybersecurity For AI Agents

<p class="lead" markdown>AI agents now reach company files, databases and internal tools through the Model Context Protocol, known as MCP. Its maintainers state in the <a href="https://modelcontextprotocol.io/specification/2026-07-28">specification</a> that MCP cannot enforce its own security principles at the protocol level. Whoever deploys it carries that duty.</p>

[Start With How MCP Works](how-mcp-works/roles.md){ .md-button .md-button--primary }
[Read The Real Cases](how-attacks-happen/deadbugz.md){ .md-button }

<a href="#" id="tour-start" class="tour-link">New here? Take the 30-second tour</a>

<div class="belt">
<div><b>23</b><span>Pull requests opened in 74 minutes to spread one malicious MCP server</span></div>
<div><b>3</b><span>Tool calls before that server changed its instructions</span></div>
<div><b>15</b><span>Versions published before the fake Postmark package added a backdoor</span></div>
<div><b>28 Jul 2026</b><span>MCP specification revision behind every protocol statement here</span></div>
</div>

## The Problem

<span class="label">What Changed</span> - Through MCP, a language model can query databases, call APIs and run computations on systems outside the chat window. The specification describes [tools as model-controlled](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), so the model finds and invokes them on its own from the user's prompt.

<span class="label">What Breaks</span> - Each server supplies the text that describes its tools, and the model reads that text when it chooses what to do. Some clients showed a tool's description once at approval and gave no notice when it later changed, as [Invariant Labs reported](https://invariantlabs.ai/blog/whatsapp-mcp-exploited) in April 2025.

<span class="label">Real Example</span> - On 10 August 2026, one GitHub account opened 23 pull requests in 74 minutes to spread an MCP server named `productivity-suite`. The server formatted and summarised text as promised. After a client's third tool call, its tool descriptions changed and directed the connected agent to seek SSH keys and AWS credentials, and to hide the activity from the user. [Pillar Security](https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign) disclosed the campaign and found none of the pull requests merged when it reviewed them.

## Start Where Your Problem Is

<div class="cards">
<a class="card" href="how-mcp-works/roles/"><span class="num">PART 1</span><strong>How MCP Works And Where Trust Breaks</strong><span class="txt">You've been asked to approve MCP and can't yet picture what connects to what.</span></a>
<a class="card" href="how-attacks-happen/deadbugz/"><span class="num">PART 2</span><strong>How Attacks Happen</strong><span class="txt">You want proof from documented cases before you set policy.</span></a>
<div class="card"><span class="soon">Coming Next</span><span class="num">PART 3</span><strong>Building A Secure Server</strong><span class="txt">Your team writes its own server and has to get authorization, tokens and logging right.</span></div>
<div class="card"><span class="soon">Coming Next</span><span class="num">PART 4</span><strong>Connecting Servers Safely</strong><span class="txt">A developer wants to install a server that someone else built.</span></div>
<div class="card"><span class="soon">Coming Next</span><span class="num">PART 5</span><strong>Running MCP Over Time</strong><span class="txt">A server you approved last month may have changed since.</span></div>
<div class="card"><span class="soon">Coming Next</span><span class="num">PART 6</span><strong>Reference</strong><span class="txt">You need the OWASP mapping, a checklist or a term defined.</span></div>
</div>

!!! info "Checked Against Primary Sources"
    Protocol statements were checked against MCP specification revision **2026-07-28** on 12 November 2026. Incident details come from the researchers who first reported them, and every page links its sources.
