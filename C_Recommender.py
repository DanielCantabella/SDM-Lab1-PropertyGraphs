from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687",auth=("dani", "password"))
# driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j", "admin123"))

with driver.session() as session:
### RECOMMENDER

    ## REMOVE CONSTRAINTS (IF EXIST):
    session.run('''
    DROP CONSTRAINT communityNameConstraint IF EXISTS;
    ''')

    ## REMOVE COMMUNITY:
    session.run('''
    MATCH (n:Community)-[d:DEFINED_BY]->() DETACH DELETE n,d;
    ''')

    #Q1
    session.run('''
    CREATE CONSTRAINT communityNameConstraint FOR (community:Community) REQUIRE community.name IS UNIQUE;
    ''')
    session.run('''
    CREATE (community:Community{name: 'database'}) WITH community MATCH (keyword: Keyword) 
    WHERE keyword.keyword IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
    CREATE (community)-[:DEFINED_BY]->(keyword);
    ''')
    #Q2
    session.run('''
    MATCH (p:Paper) -[:BELONGS_TO|PUBLISHED_IN]->(e)-[:VOLUME_FROM|IS_FROM]->(ven)
    WITH ven.id AS venue, COUNT(p) AS numPapers, ven
    MATCH (com:Community)-[:DEFINED_BY]->(k:Keyword)<-[:RELATED_TO]-(p:Paper)-[:PUBLISHED_IN|BELONGS_TO]->(e)-[:VOLUME_FROM|IS_FROM]->(ven2)
    WHERE ven2.id=venue
    WITH ven2, ven2.id AS venue2, COUNT(distinct(p)) AS numPapersWithKeywords, numPapers, com
    WITH ven2, venue2, numPapersWithKeywords, numPapers, com, (toFloat(numPapersWithKeywords)/numPapers) AS percentage
    WHERE percentage>=0.9
    MERGE (ven2)-[:IN_COMMUNITY]->(com);
    ''')

    #Q3
    session.run('''
    MATCH (n)-[:IN_COMMUNITY]->({name: "database"}) 
    MATCH (n)<-[:VOLUME_FROM|IS_FROM]-(n2)
    MATCH (n2)<-[:PUBLISHED_IN|BELONGS_TO]-(p:Paper)
    MATCH (p:Paper)-[cb:CITED_BY]->(:Paper)
    WITH p, count(cb) as numCited
    ORDER BY numCited DESC LIMIT 100
    SET p.is_database_com_top = true 
    ''')

    #Q4
    session.run('''
    MATCH (p:Paper{is_database_com_top:true})-[:WRITTEN_BY]->(a:Author) 
    SET a.potential_database_com_rev = true
    ''')

    session.run('''
    MATCH (p:Paper{is_database_com_top:true})-[:WRITTEN_BY]->(a:Author)
    WITH a, count(*) as num_papers
    WHERE num_papers >1
    SET a.database_com_guru = true
    ''')
    session.close()