from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687",auth=( "neo4j", "password"))

with driver.session() as session:
    session.run('''
    LOAD CSV WITH HEADERS FROM 'file:///authors.csv' AS rowAuthor
    CREATE (:Scientist{name: rowAuthor["name"], ID: toInteger(rowAuthor["authorid"])})
    ''')

#Borrar
# file= ''' 'file:///authors.csv' '''
# with driver.session() as session:
#     result= session.run('''
#     Call dbms.listConfig() YIELD name, value
# WHERE name='dbms.directories.import'
# RETURN value
#     ''')


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