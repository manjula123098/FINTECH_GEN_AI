import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv(override=True)

class KGStore:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(
                os.getenv("NEO4J_USERNAME"),
                os.getenv("NEO4J_PASSWORD")
            )
        )

    def run(self, query, params=None):
        with self.driver.session() as session:
            return list(session.run(query, params or {}))

    def close(self):
        self.driver.close()
