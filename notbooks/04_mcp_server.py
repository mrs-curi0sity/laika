from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase

# muss eingetragen werden unter http://localhost:3000/admin/settings/integrations

mcp = FastMCP(
    "LAIKA Neo4j Server",
    host="0.0.0.0",
    port=8080
)

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "DEIN_PASSWORT")
)

@mcp.tool()
def get_personen() -> str:
    """Gibt alle Personen im Ermittlungsgraph zurück"""
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person)
            RETURN p.name as name, p.rolle as rolle, p.status as status
            ORDER BY p.rolle
        """)
        personen = [dict(r) for r in result]
        return str(personen)

@mcp.tool()
def get_ueberweisungen() -> str:
    """Gibt alle Geldüberweisungen zurück"""
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Person)-[r:ÜBERWIES]->(b:Person)
            RETURN a.name as von, b.name as an, 
                   r.betrag as betrag, r.datum as datum
        """)
        return str([dict(r) for r in result])

@mcp.tool()
def get_netzwerk(name: str) -> str:
    """Gibt alle bekannten Personen einer Person zurück"""
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person {name: $name})-[:KENNT]->(bekannt:Person)
            RETURN bekannt.name as name, bekannt.rolle as rolle
        """, name=name)
        return str([dict(r) for r in result])

if __name__ == "__main__":
    mcp.run(transport="streamable-http")