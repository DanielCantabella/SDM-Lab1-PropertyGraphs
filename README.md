# README

## Queries

### Constraints
```
CREATE CONSTRAINT authorIdConstraint FOR (author:Author) REQUIRE author.id IS UNIQUE;
```
```
CREATE CONSTRAINT paperIdConstraint FOR (paper:Paper) REQUIRE paper.id IS UNIQUE;
```

### CSV Loadings
#### Load Authors
```
LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
```
#### Load Papers
```
LOAD CSV WITH HEADERS FROM "file:///papers-sample.csv" AS rowPaper
CREATE (p:Paper {id: toInteger(rowPaper.corpusId), title: rowPaper.title, year:toInteger(rowPaper.year)});
```

### Relations

#### Paper - [WRITTEN_BY] -> Author

```
LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
MATCH (author:Author {id: toInteger(rowRelation.authorID)})
MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
CREATE (paper)-[:WRITTEN_BY]->(author);
```

#### citingPaper - [REFERENCES] -> citedPaper
```
LOAD CSV WITH HEADERS FROM "file:///citations-sample.csv" AS rowCitation
MATCH (citingPaper:Paper {id: toInteger(rowCitation.citingcorpusid)})
MATCH (citedPaper:Paper {id: toInteger(rowCitation.citedcorpusid)})
CREATE (citingPaper)-[:REFERENCES]->(citedPaper);
```

