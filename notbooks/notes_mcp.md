# Modul 4 — MCP (Model Context Protocol)

## Was ist MCP?
Einheitliches Protokoll damit LLMs externe Tools nutzen können.
Analogie: USB für KI-Tools — ein Standard, viele Geräte.
Entwickelt von Anthropic, Ende 2024, open source.

## Die drei Rollen
- **Host**: App die das LLM enthält (OpenWebUI, Claude)
- **Client**: Vermittler im Host
- **Server**: Stellt Tools bereit — das programmierst DU

## Wann MCP, wann direktes Python?
- **MCP**: LLM/OpenWebUI soll Tools selbst entdecken und aufrufen
- **Direktes Python**: Streamlit App, du kontrollierst den Ablauf selbst
- Für das Arbeitsprojekt (Streamlit): kein MCP nötig!

## MCP Server starten
```bash
pip install mcp
python 04_mcp_server.py
```

## Minimaler MCP Server
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server Name", host="0.0.0.0", port=8080)

@mcp.tool()
def mein_tool(parameter: str) -> str:
    """Diese Beschreibung sieht das LLM!"""
    return "Ergebnis"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

## In OpenWebUI einbinden
Admin Panel → Tools → URL: `http://localhost:8080/mcp`
Dann im Chat: Tool-Icon aktivieren → LLM ruft Tools automatisch auf.

## Protokoll-Details (curl Test)
MCP braucht Session-Initialisierung vor Tool-Aufrufen.
Für Produktion: Client-Library nutzen, nicht curl.

## Fazit für Arbeitsprojekt
Neo4j direkt aus Python ansprechen — kein MCP nötig.
MCP sinnvoll wenn: mehrere Teams dieselben Tools nutzen sollen,
oder OpenWebUI die Tools selbst entdecken soll.