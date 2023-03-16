from neo4j import GraphDatabase

DATABASE_URL = 'bolt://localhost:7687'
# USER = 'dani'
# PASSWORD = 'password'
USER = 'neo4j'
PASSWORD = 'admin123'

def evolveTheGraph():
    driver = GraphDatabase.driver("bolt://localhost:7687",auth=(USER,PASSWORD))

    with driver.session() as session:
        session.run('''
            LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
            MATCH (p:Paper{id: toInteger(rowReview.paperID)})-[r: REVIEWED_BY]->(a:Author{id:toInteger(rowReview.reviewerID)})
            SET r.description = rowReview.review;
            ''')
        # To update the approved attribute

        # First set all the papers as not approved
        session.run('''MATCH (p:Paper) SET p.approved = false''')

        # Change only the status to approved of the papers that have more than the half os the reviews with a grade higher than 2
        session.run('''
                MATCH (p:Paper)
                OPTIONAL MATCH (p)-[e:REVIEWED_BY]->(:Author)
                WITH p, COUNT(e) as numRev, COUNT(CASE WHEN e.with_grade>2 THEN 1 END) as numApp
                WHERE numRev/2 < numApp
                SET p.approved = true
            ''')

        #Adding reviews
        session.run('''
            LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
            MATCH (p:Paper{id: toInteger(rowReview.paperID)})-[r: REVIEWED_BY]->(a:Author{id:toInteger(rowReview.reviewerID)})
            SET r.description = rowReview.review;
            ''')

        #Adding organizations
        session.run('''
            CREATE CONSTRAINT companyIdConstraint FOR (organization:Organization) REQUIRE organization.id IS UNIQUE;
            ''')
        session.run('''
            LOAD CSV WITH HEADERS FROM "file:///companies.csv" AS rowCompany
            CREATE (c:Organization {id: rowCompany.companyid, name:rowCompany.company, type:'company'});
            ''')
        session.run('''
            LOAD CSV WITH HEADERS FROM "file:///universities.csv" AS rowUniversity
            CREATE (u:Organization {id: rowUniversity.universityid, name:rowUniversity.university, type:'university'});
            ''')
        session.run('''
            LOAD CSV WITH HEADERS FROM "file:///affiliated-to.csv" AS rowAffiliated
            MATCH(a:Author{id:toInteger(rowAffiliated.authorID)})
            MATCH(o:Organization{id:rowAffiliated.affiliation})
            CREATE (a)-[:IS_AFFILIATED_TO]->(o);
            ''')

        session.close()
