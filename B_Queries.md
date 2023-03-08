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
```Cypher
MATCH (c:Conference) <-[:BELONGS_TO]-(p:Paper)-[:WRITTEN_BY]-> (a:Author) WITH c.name AS ConferenceName, a.name AS authorName, COUNT(DISTINCT(p)) as numPapers WHERE numPapers>=4 RETURN ConferenceName, authorName, numPapers  ORDER BY ConferenceName;
```

[//]: # (```Cypher)
[//]: # (MATCH &#40;c:Conference&#41; <-[:BELONGS_TO]-&#40;p:Paper&#41;-[:WRITTEN_BY]-> &#40;a:Author&#41; WITH c.name AS ConferenceName, COLLECT&#40;DISTINCT&#40;a&#41;&#41; AS authorCollection, count&#40;distinct&#40;p&#41;&#41; as numPapers WHERE numPapers>=4 RETURN ConferenceName, authorCollection, numPapers  order by ConferenceName)
[//]: # (```)


### 3. Impact factors of the journals in your graph 
```Cypher
MATCH (j:Journal)<-[e1:VOLUME_FROM]-(v:Volume)
MATCH (v:Volume)<-[e:PUBLISHED_IN]-(p:Paper)
OPTIONAL MATCH (p)-[e2:CITED_BY]->(p2:Paper {year: toInteger(v.year)-1})
with j, v.year as year, count(e2) as numCit
OPTIONAL MATCH (p)-[e3:PUBLISHED_IN{year:toInteger(year)-1}]->(j)
WITH j, year, numCit, count(e3) as numPub1
OPTIONAL MATCH (p)-[e3:PUBLISHED_IN{year:toInteger(year)-2}]->(j)
WITH j, year, numCit, numPub1, count(e3) as numPub2
return j.id, year, numCit, numPub1, numPub2, CASE numPub1+numPub2 WHEN 0 THEN 0.0 ELSE toFloat(numCit)/(numPub1+numPub2) END AS IF order by j.id, year
```
### 4. H-indexes of the authors in your graph
```Cypher
MATCH (a:Author)<-[WRITTEN_BY]-(p:Paper) -[c:CITED_BY]-> (:Paper)
WITH a.name as authorName, p.title AS title, COUNT(c) AS numCites 
ORDER BY numCites DESC
WITH authorName, COLLECT(numCites) AS numCitesList
WITH authorName, [x IN range(1,size(numCitesList)) WHERE x<=numCitesList[x-1]| [numCitesList[x-1],x] ] AS hIndexList
RETURN authorName,hIndexList[-1][1] AS h_index

```