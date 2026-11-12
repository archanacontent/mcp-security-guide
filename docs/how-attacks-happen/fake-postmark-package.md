# The Fake Postmark Package, September 2025

Postmark publishes its MCP server on GitHub and, before September 2025, had never published one on npm. Someone else filled that gap. A package named `postmark-mcp` appeared on npm, built trust across 15 versions and then began copying the emails it sent to an outside address.

<span class="label">Source</span> - Koi Security found the backdoor, and [Postmark](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package) confirmed the incident in a statement on 25 September 2025. Koi's figures on these pages come from [The Register's report](https://www.theregister.com/2025/09/29/postmark_mcp_server_code_hijacked/) of 29 September 2025.

<div class="cards stats">
<div class="card"><span class="big">15</span><span class="txt">versions published before the backdoor, according to Postmark</span></div>
<div class="card"><span class="big">1.0.16</span><span class="txt">the version that added it, according to Postmark</span></div>
<div class="card"><span class="big">~1,500</span><span class="txt">downloads in a week, according to Koi Security</span></div>
<div class="card"><span class="big">1</span><span class="txt">customer known to have used it, Postmark told The Register</span></div>
</div>

## What The Backdoor Did

Version 1.0.16 "added a backdoor" that "secretly BCC'd emails to an external server", in Postmark's words. The Register reports that the change was a single line of code. Its reporting adds that the developer appears to have copied the real server's code from GitHub and published it on npm under the look-alike name.

Postmark states that it had no involvement with the package, and that its own API and services remain secure and unaffected.

## Two Sets Of Numbers

Koi Security counted about 1,500 downloads in a week. Idan Dardikman, Koi's co-founder and CTO, estimated that around 20 percent of those were in active use, which he put at about 300 organisations. Postmark told The Register that it knew of only one customer that used the package. No source has published a confirmed count of affected organisations.

## Code Changed, Descriptions Didn't Have To

In the two earlier cases, a server fed instructions to the model through tool descriptions. The Postmark reports describe a change in the package's code, and none of them mentions a changed description. [OWASP's MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) warns that pinning tool definitions by hash detects metadata changes only. A check of that kind would not catch a server whose code changes behind an unchanged definition.

## If You Installed It

Postmark gives three steps to anyone who used the fake package.

- **Remove** - Remove the package from your systems right away.
- **Review** - Check your email logs for suspicious activity.
- **Rotate** - Consider rotating any credentials that were sent by email while the package was in use.

Postmark's official MCP server is at [github.com/ActiveCampaign/postmark-mcp](https://github.com/ActiveCampaign/postmark-mcp).

**Next:** [The Cases Against OWASP's Beta List](owasp-mapping.md)
