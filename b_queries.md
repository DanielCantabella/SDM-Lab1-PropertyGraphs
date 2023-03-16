# B. Querying

### 1. Top 3 most cited papers of each conference
```Cypher
MATCH (c:Conference)<-[:IS_FROM]-(e:Edition)
MATCH (e)<-[:BELONGS_TO]-(p:Paper)
MATCH (p:Paper)-[cb:CITED_BY]->(:Paper)
WITH c, p, count(cb) as numCited
ORDER BY c, numCited DESC
WITH c, COLLECT({paperId: p.id, numCited: numCited}) AS papers
RETURN c.id, c.name, papers[0..3] AS topPapers
```

### 2. Conference author community
Previous to edition, volume, etc. nodes
```Cypher
MATCH (c:Conference) <-[:BELONGS_TO]-(p:Paper)-[:WRITTEN_BY]-> (a:Author) WITH c.name AS ConferenceName, a.name AS authorName, COUNT(DISTINCT(p)) as numPapers WHERE numPapers>=4 RETURN ConferenceName, authorName, numPapers  ORDER BY ConferenceName;
```
After (and maybe final schema) edition, volumne, nodes added:
```Cypher
MATCH (author:Author)<-[:WRITTEN_BY]-(paper:Paper)-[:BELONGS_TO]->(edition:Edition)-[:IS_FROM]->(conf:Conference)
WITH conf.name AS conference, author.name AS authName, COUNT(DISTINCT(paper)) as numPapers
WHERE numPapers>3
WITH conference, COLLECT(authName) AS community, numPapers
RETURN conference, community, numPapers
```


### 3. Impact factors of the journals in your graph 
```Cypher
MATCH (j:Journal)<-[e1:VOLUME_FROM]-(v:Volume)<-[e2:PUBLISHED_IN]-(p:Paper)
with j, toInteger(v.year) as year, count(e2) as numCit
OPTIONAL MATCH (j)<-[:VOLUME_FROM]-(v2:Volume{year:year-1})<-[e3:PUBLISHED_IN]-(:Paper)
WITH j, year, numCit, count(e3) as numPub1
OPTIONAL MATCH (j)<-[:VOLUME_FROM]-(v3:Volume{year:year-2})<-[e4:PUBLISHED_IN]-(:Paper)
WITH j, year, numCit, numPub1, count(e4) as numPub2
return j.id, year, numCit, numPub1, numPub2, CASE numPub1+numPub2 WHEN 0 THEN 0.0 ELSE toFloat(numCit)/(numPub1+numPub2) END AS IF order by j.id, year
```
### 4. H-indexes of the authors in your graph
```Cypher
MATCH (a:Author)<-[WRITTEN_BY]-(p:Paper)-[c:CITED_BY]-> (:Paper)
WITH a.name as authorName, p.title AS title, COUNT(c) AS numCites 
ORDER BY numCites DESC
WITH authorName, COLLECT(numCites) AS numCitesList
WITH authorName, [x IN range(1,size(numCitesList)) WHERE x<=numCitesList[x-1]| [numCitesList[x-1],x] ] AS hIndexList
RETURN authorName,hIndexList[-1][1] AS h_index

```

