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
WHERE numPapers>1
WITH conference, COLLECT(authName) AS community, numPapers
RETURN conference, community, numPapers
```


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
MATCH (a:Author)<-[WRITTEN_BY]-(p:Paper)-[c:CITED_BY]-> (:Paper)
WITH a.name as authorName, p.title AS title, COUNT(c) AS numCites 
ORDER BY numCites DESC
WITH authorName, COLLECT(numCites) AS numCitesList
WITH authorName, [x IN range(1,size(numCitesList)) WHERE x<=numCitesList[x-1]| [numCitesList[x-1],x] ] AS hIndexList
RETURN authorName,hIndexList[-1][1] AS h_index

```

### RECOMMENDER
Q1
```Cypher
CREATE CONSTRAINT communityNameConstraint FOR (community:Community) REQUIRE community.name IS UNIQUE;
CREATE (community:Community{name: 'database'}) WITH community MATCH (keyword: Keyword) WHERE keyword.keyword IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying'] CREATE (community)-[:DEFINED_BY]->(keyword);
```
Q2
```
MATCH (p:Paper)-[:BELONGS_TO]->(e:Edition)-[:IS_FROM]->(conf:Conference)
WITH conf.id AS conference, COUNT(p) AS numPapers
MATCH (conf2:Conference{id: conference})<-[:IS_FROM]-(e:Edition)<-[:BELONGS_TO]-(p:Paper)-[:RELATED_TO]->(k:Keyword)<-[:DEFINED_BY]-(com:Community)
WITH conf2, conf2.id AS conference2, COUNT(distinct(p)) AS numPapersWithKeywords, numPapers, com
WITH conf2, conference2, numPapers, numPapersWithKeywords, (toFloat(numPapersWithKeywords)/numPapers) AS percentage, com
WHERE percentage>=0.9
MERGE (conf2)-[:IN_COMMUNITY]->(com);
    
MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Volume)-[:VOLUME_FROM]->(jour:Journal)
WITH jour.id AS journal, COUNT(p) AS numPapers
MATCH (jour2:Journal{id: journal})<-[:VOLUME_FROM]-(v:Volume)<-[:PUBLISHED_IN]-(p:Paper)-[:RELATED_TO]->(k:Keyword)<-[:DEFINED_BY]-(com:Community)
WITH jour2, jour2.id AS journal2, COUNT(distinct(p)) AS numPapersWithKeywords, numPapers, com
WITH jour2, journal2, numPapers, numPapersWithKeywords, (toFloat(numPapersWithKeywords)/numPapers) AS percentage, com
WHERE percentage>=0.9
MERGE (jour2)-[:IN_COMMUNITY]->(com);
```
