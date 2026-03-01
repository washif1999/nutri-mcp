# 💬 MCP Prompts Reference

This MCP server exposes one built-in prompt template.

> The `dietary_analysis` prompt has moved to the `nutrimcp-agent` project.

---

## `health_summary`

Generates a structured medical summary of recent health complaints suitable for sharing with a doctor.

**When to use:** Before a doctor's visit, or when you want a recap of recent health events.

**Example invocation (Claude Desktop):**
> *"Use the health_summary prompt to summarise my recent complaints."*

**What it does:**
1. Reads `health://complaints` for recent entries
2. Reads `health://appointments` for any auto-booked visits
3. Formats a clean chronological health summary
4. Highlights high-severity complaints and appointment details
5. Returns a report ready to share with a medical professional
