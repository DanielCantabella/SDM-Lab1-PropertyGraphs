from neo4j import GraphDatabase
# password=open('password.txt').readline()
# print(password)
# driver = GraphDatabase.driver("bolt://localhost:7687",auth=("dani", "password"))

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "admin123"))

with driver.session() as session:
    #To update the approved attribute

    #First set all the papers as not approved
    session.run('''MATCH (p:Paper) SET p.approved = false''')

    #Change only the status to approved of the papers that have more than the half os the reviews with a grade higher than 2
    session.run('''
        MATCH (p:Paper)
        OPTIONAL MATCH (p)-[e:REVIEWED_BY]->(:Author)
        WITH p, COUNT(e) as numRev, COUNT(CASE WHEN e.with_grade>2 THEN 1 END) as numApp
        WHERE numRev/2 < numApp
        SET p.approved = true
    ''')
