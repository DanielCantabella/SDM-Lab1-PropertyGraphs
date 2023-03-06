# B. Querying

### 1. Top 3 most cited papers of each conference
```Cypher
MATCH (c:Conference)<-[:BELONGS_TO]-(p:Paper)
OPTIONAL MATCH (p:Paper)-[e:CITED_BY]->(:Paper)
WITH c, p, count(e) as numCited
ORDER BY c.id, numCited DESC
WITH c, COLLECT({paperId: p.id, numCited: numCited}) AS papers
RETURN c.id, papers[0..3] AS topPapers
```

### 2. Conference author community
```Cypher


```
### 3. Impact factors of the journals in your graph 
```Cypher
MATCH (j:Journal)<-[e:PUBLISHED_IN]-(p:Paper)
OPTIONAL MATCH (p)-[e2:CITED_BY]->(p2:Paper {year: toInteger(e.year)-1})
with j, e.year as year, count(e2) as numCit
OPTIONAL MATCH (p)-[e3:PUBLISHED_IN{year:toInteger(year)-1}]->(j)
WITH j, year, numCit, count(e3) as numPub1
OPTIONAL MATCH (p)-[e3:PUBLISHED_IN{year:toInteger(year)-2}]->(j)
WITH j, year, numCit, numPub1, count(e3) as numPub2
return j.id, year, numCit, numPub1, numPub2, CASE numPub1+numPub2 WHEN 0 THEN 0.0 ELSE toFloat(numCit)/(numPub1+numPub2) END AS IF order by j.id, year
```
### 4. H-indexes of the authors in your graph
```Cypher


```