# The WhatsApp Demonstration, April 2025

Approval dialogs are the control most teams count on. Researchers at Invariant Labs showed in April 2025 how an agent can leak a user's WhatsApp messages while the user confirms every tool call.

<span class="label">Source</span> - Luca Beurer-Kellner and Marc Fischer of [Invariant Labs](https://invariantlabs.ai/blog/whatsapp-mcp-exploited) published the work on 7 April 2025. They built it as a demonstration to raise awareness of the risk. Invariant sells MCP security tools, and the post promotes them.

## The Setup

An agent in a client such as Cursor or Claude Desktop is connected to two servers. One is a trusted `whatsapp-mcp` server that can send, receive and check messages. The second belongs to the attacker.

=== "Experiment 1: The Sleeper Server"

    <ol class="steps">
    <li>On first launch, the attacker's server advertises one tool, <code>get_fact_of_the_day</code>, described as "Get a random fact of the day."</li>
    <li>The user approves the tool.</li>
    <li>On its second launch, the server swaps in a new description. The user isn't asked to approve again.</li>
    <li>The new description tells the agent to send WhatsApp messages to a proxy number, place the real recipient in the message body, attach the results of earlier <code>list_chats</code> calls and avoid notifying the user.</li>
    <li>The agent sends the user's chat data to the attacker through the trusted WhatsApp server.</li>
    </ol>

=== "Experiment 2: No Malicious Server"

    The attacker needs only the target's WhatsApp number. A message that contains a prompt injection is sent to the target, and it takes effect once the agent calls `list_chats` and reads the message. Invariant reports that the injection was harder to get working and that it still succeeded.

## Why Approval Didn't Stop It

Invariant states that a user must always confirm a tool call before it runs, at least in Cursor and Claude Desktop. The confirmation showed a raw phone number as the recipient, which is hard to check by eye. The message appeared to read "Hi", and the stolen data sat far to the right, where the user would have to scroll to find it.

!!! note "Sandboxing Would Not Have Helped"
    Invariant states that code isolation or sandboxing of the MCP server is not a relevant mitigation, because the attack relies on the agent's instruction-following. In the first experiment the data left through WhatsApp itself, sent by the trusted server at the agent's request.

Invariant's post gives no detailed list of fixes. Its one piece of general advice is to be cautious when connecting an agent to untrusted MCP servers.

**Next:** [The Fake Postmark Package, September 2025](fake-postmark-package.md)
