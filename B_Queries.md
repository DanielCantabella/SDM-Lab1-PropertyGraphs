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

### 2. Conferenece author community
```Cypher


```
### 3. Impact factors of the journals in your graph 
```Cypher


```
### 4. H-indexes of the authors in your graph
```Cypher


```