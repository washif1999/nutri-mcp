from .tools import mcp

@mcp.prompt()
def dietary_analysis() -> str:
    """
    Prompt for LLM to analyze intake vs. goal macros.
    References nutrition://logs and nutrition://targets resources.
    """
    return (
        "Analyze my recent meal logs from nutrition://logs and compare them "
        "to my daily targets from nutrition://targets. Identify deficiencies "
        "or excesses and suggest adjustments for my next meal."
    )

@mcp.prompt()
def health_summary() -> str:
    """
    Prompt for LLM to generate a medical appointment summary.
    References health://complaints resource.
    """
    return (
        "Review my recent health complaints from health://complaints. "
        "Summarize the key symptoms, note any recurring patterns, "
        "and prepare a concise report suitable for a medical consultation."
    )
