from neo4j import GraphDatabase
password=open('password.txt').readline()
driver = GraphDatabase.driver("bolt://localhost:7687",auth=( "neo4j", password))

with driver.session() as session:
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
    CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
    ''')

    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///papers-sample.csv" AS rowPaper
    CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year:toInteger(rowPaper.year)});
    ''')

    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
    MATCH (author:Author {id: toInteger(rowRelation.authorID)})
    MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
    CREATE (paper)-[:WRITTEN_BY{corresponding_author: rowRelation.is_corresponding}]->(author);
    ''')

    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///citations-sample.csv" AS rowCitation
    MATCH (citingPaper:Paper {id: toInteger(rowCitation.citingcorpusid)})
    MATCH (citedPaper:Paper {id: toInteger(rowCitation.citedcorpusid)})
    CREATE (citingPaper)-[:REFERENCES]->(citedPaper);
    ''')

    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
    MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
    MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
    CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
    ''')

    session.run('''
        LOAD CSV WITH HEADERS FROM 'file:///abstracts-sample.csv' AS rowAbstract
        MATCH (p:Paper {id: toInteger(rowAbstract.corpusid)}) SET p.abstract=rowAbstract.abstract;
     ''')

    session.run('''
        LOAD CSV WITH HEADERS FROM 'file:///belongs-to.csv' AS rowBelongs
        MATCH (p:Paper {id: toInteger(rowBelongs.paperID)}) SET p.venueId=rowBelongs.venueID;
     ''')

    session.run('''
        LOAD CSV WITH HEADERS FROM 'file:///publication-venues-sample.csv' AS rowVenues
        MATCH (p:Paper {venueId: rowVenues.id}) SET p.venueType=rowVenues.type;
     ''')




# class HelloWorldExample:
#
#     def __init__(self, uri, user, password):
#         self.driver = GraphDatabase.driver(uri, auth=(user, password))
#
#     def close(self):
#         self.driver.close()
#
#     def print_greeting(self, message):
#         with self.driver.session() as session:
#             greeting = session.execute_write(self._create_and_return_greeting, message)
#             print(greeting)
#
#     @staticmethod
#     def _create_and_return_greeting(tx, message):
#         result = tx.run("CREATE (a:Greeting) "
#                         "SET a.message = $message "
#                         "RETURN a.message + ', from node ' + id(a)", message=message)
#         return result.single()[0]
#
#
# if __name__ == "__main__":
#     greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "5Diamante$")
#     greeter.print_greeting("hello, world")
#     greeter.close()