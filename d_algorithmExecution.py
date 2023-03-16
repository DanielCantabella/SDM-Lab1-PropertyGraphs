from neo4j import GraphDatabase
from util import *

DATABASE_URL = 'bolt://localhost:7687'
# USER = 'dani'
# PASSWORD = 'password'
USER = 'neo4j'
PASSWORD = 'admin123'

driver = GraphDatabase.driver("bolt://localhost:7687",auth=(USER,PASSWORD))

def algortihmExecution():
    with driver.session() as session:
        if session.run("CALL gds.graph.exists('similarity_graph')").values()[0][1]:
            session.run('CALL gds.graph.drop("similarity_graph") YIELD graphName;')

        if session.run("CALL gds.graph.exists('LouvainGraph')").values()[0][1]:
            session.run('CALL gds.graph.drop("LouvainGraph") YIELD graphName;')

        print("Algorithm 1")
        session.run('''
        CALL gds.graph.project(
            'similarity_graph',
            ['Author', 'Paper'],
            {
                WRITTEN_BY: {
                    orientation: "REVERSE"
                }
            }
        );
        ''')

        res = session.run('''
            CALL gds.nodeSimilarity.stream('similarity_graph')
            YIELD node1, node2, similarity
            RETURN gds.util.asNode(node1).id AS Author1, gds.util.asNode(node2).id AS Author2, similarity
            ORDER BY similarity DESCENDING, Author1, Author2
                   ''')
        printQuery(res)

        printLine('-', 70)
        print("Algorithm 2")
        session.run('''
            CALL gds.graph.project('LouvainGraph', 'Paper', 'CITED_BY')
            ''')

        res = session.run('''
            CALL gds.louvain.stream('LouvainGraph')
            YIELD nodeId, communityId, intermediateCommunityIds
            RETURN COLLECT(gds.util.asNode(nodeId).title) AS title, communityId
            ORDER BY communityId ASC
            ''')
        printQuery(res)

        session.close()