"""
app/utils/banner.py - Startup banner and colorful config display.
"""
from colorama import Fore, Back, Style, init
from art import text2art
from app.core.config import settings

init(autoreset=True)  # reset color after each print

def print_banner():
    """Print a styled ASCII art welcome banner for the Nutrition Assistant."""
    banner = text2art("NutriMCP", font="doom")
    print(Fore.GREEN + Style.BRIGHT + banner)
    print(Fore.CYAN + Style.BRIGHT + "  Smart Macro & Nutrition Assistant — MCP Server")
    print(Fore.CYAN + "  Powered by FastMCP · SQLAlchemy · Pydantic")
    print(Style.DIM + "  " + "─" * 58)
    print()

def print_startup_info():
    """Print colorful server configuration and important details."""
    section("SERVER CONFIGURATION")
    info("Host",          "0.0.0.0:9000")
    info("Database",      settings.database_url)
    info("Debug Mode",    str(settings.debug))
    info("Auth Token",    f"{settings.default_auth_token[:8]}***  (default)")
    info("Alert Level",   f"Severity >= {settings.severity_alert_threshold} → Doctor Auto-Booking")
    print()

    section("MCP COMPONENTS")
    component("Tools",     "calculate_macros · log_meal · log_complaint")
    component("Tools",     "calculate_bmi · calculate_tdee · get_weekly_report")
    component("Tools",     "remove_meal · list_appointments")
    component("Resources", "nutrition://targets · nutrition://logs · nutrition://bmi-categories")
    component("Resources", "health://complaints · health://hospitals · health://appointments")
    component("Prompts",   "dietary_analysis · health_summary")
    print()

    section("URLS & ACCESS")
    host = "http://localhost:9000"

    # Health URL
    print(f"  {Fore.GREEN + Style.BRIGHT}{'Health Check':<20}{Style.RESET_ALL}")
    print(f"    URL    : {Fore.CYAN}{host}/health")
    print(f"    Method : {Fore.GREEN}GET{Style.RESET_ALL}   │  {Fore.WHITE}No authentication required")
    print(f"    curl   : {Style.DIM}curl -s {host}/health")
    print()

    # MCP URL
    print(f"  {Fore.BLUE + Style.BRIGHT}{'MCP Protocol':<20}{Style.RESET_ALL}")
    print(f"    URL    : {Fore.CYAN}{host}/mcp")
    print(f"    Method : {Fore.YELLOW}ALL{Style.RESET_ALL}   │  {Fore.RED}Bearer token required")
    print(f"    Header : {Style.DIM}Authorization: Bearer <api_key>")
    print(f"    curl   : {Style.DIM}curl -X POST -H \"Authorization: Bearer {settings.default_auth_token}\" {host}/mcp")
    print()

    # SSE endpoint
    print(f"  {Fore.MAGENTA + Style.BRIGHT}{'MCP SSE Stream':<20}{Style.RESET_ALL}")
    print(f"    URL    : {Fore.CYAN}{host}/sse")
    print(f"    Method : {Fore.GREEN}GET{Style.RESET_ALL}   │  {Fore.WHITE}No auth required (open for MCP Inspector)")
    print(f"    Info   : {Style.DIM}Used by Supergateway and MCP clients for streaming")
    print()

    warning("All /mcp/* routes require:  Authorization: Bearer <api_key>")
    print()

# ── Helpers ───────────────────────────────────────────────────────────────────

def section(title: str):
    print(Fore.YELLOW + Style.BRIGHT + f"  ▸ {title}")
    print(Fore.YELLOW + "  " + "─" * 50)

def info(key: str, value: str):
    print(f"  {Fore.WHITE + Style.BRIGHT}{key:<20}{Style.RESET_ALL}  {Fore.CYAN}{value}")

def component(kind: str, value: str):
    print(f"  {Fore.MAGENTA + Style.BRIGHT}{kind:<12}{Style.RESET_ALL}  {Fore.WHITE}{value}")

def endpoint(method: str, path: str, desc: str):
    color = Fore.GREEN if method == "GET" else Fore.BLUE
    print(f"  {color + Style.BRIGHT}{method:<8}{Style.RESET_ALL}  {Fore.WHITE}{path:<20}{Style.DIM}{desc}")

def warning(msg: str):
    print(Fore.RED + Style.BRIGHT + f"  ⚠  {msg}" + Style.RESET_ALL)
