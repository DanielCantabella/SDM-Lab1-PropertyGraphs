from neo4j import GraphDatabase

# driver = GraphDatabase.driver("bolt://localhost:7687",auth=("dani", "password"))
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j", "admin123"))

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
    #Conferences
    session.run('''
    MATCH (p:Paper)-[:BELONGS_TO]->(e:Edition)-[:IS_FROM]->(conf:Conference)
    WITH conf.id AS conference, COUNT(p) AS numPapers
    MATCH (conf2:Conference{id: conference})<-[:IS_FROM]-(e:Edition)<-[:BELONGS_TO]-(p:Paper)-[:RELATED_TO]->(k:Keyword)<-[:DEFINED_BY]-(com:Community)
    WITH conf2, conf2.id AS conference2, COUNT(distinct(p)) AS numPapersWithKeywords, numPapers, com
    WITH conf2, conference2, numPapers, numPapersWithKeywords, (toFloat(numPapersWithKeywords)/numPapers) AS percentage, com
    WHERE percentage>=0.9
    MERGE (conf2)-[:IN_COMMUNITY]->(com);
    ''')
    # Journals
    session.run('''
    MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Volume)-[:VOLUME_FROM]->(jour:Journal)
    WITH jour.id AS journal, COUNT(p) AS numPapers
    MATCH (jour2:Journal{id: journal})<-[:VOLUME_FROM]-(v:Volume)<-[:PUBLISHED_IN]-(p:Paper)-[:RELATED_TO]->(k:Keyword)<-[:DEFINED_BY]-(com:Community)
    WITH jour2, jour2.id AS journal2, COUNT(distinct(p)) AS numPapersWithKeywords, numPapers, com
    WITH jour2, journal2, numPapers, numPapersWithKeywords, (toFloat(numPapersWithKeywords)/numPapers) AS percentage, com
    WHERE percentage>=0.9
    MERGE (jour2)-[:IN_COMMUNITY]->(com);
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