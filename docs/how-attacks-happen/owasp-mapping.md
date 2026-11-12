# The Cases Against OWASP's Beta List

Security teams often have to file a finding under a recognised category before anyone funds the fix. The [OWASP MCP Top 10](https://owasp.org/projects/mcp-top-10) supplies those categories for MCP. Treat it with some care, because OWASP's project page places the list at Phase 3, a beta release under pilot testing, and calls it a living document.

## The Ten Entries

| ID | Entry |
| --- | --- |
| MCP01 | Token Mismanagement & Secret Exposure |
| MCP02 | Privilege Escalation via Scope Creep |
| MCP03 | Tool Poisoning |
| MCP04 | Software Supply Chain Attacks & Dependency Tampering |
| MCP05 | Command Injection & Execution |
| MCP06 | Prompt Injection via Contextual Payloads |
| MCP07 | Insufficient Authentication & Authorization |
| MCP08 | Lack of Audit and Telemetry |
| MCP09 | Shadow MCP Servers |
| MCP10 | Context Injection & Over-Sharing |

## Where Each Case Fits

| Case | Closest Beta Entry | OWASP's Wording For That Entry |
| --- | --- | --- |
| **Deadbugz** | MCP03 Tool Poisoning | "an adversary compromises the tools, plugins, or their outputs that an AI model depends on" |
| **WhatsApp, Experiment 1** | MCP03 Tool Poisoning | The same wording applies. |
| **WhatsApp, Experiment 2** | MCP06 Prompt Injection via Contextual Payloads | "in the MCP world the 'interpreter' is the model and the 'payload' is text" |
| **Fake Postmark Package** | MCP04 Software Supply Chain Attacks & Dependency Tampering | "A compromised dependency can alter agent behavior or introduce execution-level backdoors." |

!!! note "The Pairings Are This Guide's Own"
    OWASP itself has not sorted these three cases into its MCP list. Each pairing in the table is this guide's own, based on the quoted wording of the entry.

## OWASP's Own Classification Of Deadbugz

OWASP's GenAI Security Project did classify Deadbugz in its [exploit roundup for the third quarter of 2026](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/), against two of its other lists. The roundup assigns the campaign no MCP Top 10 codes.

| OWASP List | Entries Assigned To Deadbugz |
| --- | --- |
| Top 10 for Agentic Applications | ASI04 Agentic Supply Chain Vulnerabilities, ASI06 Memory & Context Poisoning, ASI09 Human-Agent Trust Exploitation |
| Top 10 for LLM Applications | LLM04:2026 Supply Chain, LLM02:2026 Sensitive Information Disclosure |

## Entries These Cases Don't Reach

The three cases touch three of the ten entries. Token handling (MCP01), scope creep (MCP02), command injection (MCP05), authentication (MCP07), audit gaps (MCP08), shadow servers (MCP09) and over-sharing of context (MCP10) have no case on these pages. Parts 3 to 5 take them up from the builder's and the operator's side.
