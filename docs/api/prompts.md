# 💬 MCP Prompts Reference

Prompts are built-in instruction templates that guide the LLM to perform structured analysis.

---

## `dietary_analysis`

Guides the LLM to compare the user's actual macro intake against their daily targets and provide actionable recommendations.

**When to use:** After logging multiple meals, ask the LLM to analyse the day's nutrition.

**Example invocation (Claude Desktop):**
> *"Use the dietary_analysis prompt to review today's meals."*

**What it does:**
1. Reads `nutrition://logs` for today's meals
2. Reads `nutrition://targets` for daily goals
3. Compares actual vs. target for calories, protein, carbs, and fat
4. Returns a structured report with surplus/deficit and suggestions

---

## `health_summary`

Prepares a structured summary of recent health complaints suitable for sharing with a medical professional.

**When to use:** Before a doctor's visit, or when you want a recap of recent health events.

**Example invocation:**
> *"Use the health_summary prompt to summarise my recent complaints."*

**What it does:**
1. Reads `health://complaints` for recent entries
2. Reads `health://appointments` for any auto-booked visits
3. Formats a clean chronological health summary
4. Highlights high-severity complaints and appointment details
