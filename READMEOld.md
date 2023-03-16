# README

## Queries

### Constraints
```
CREATE CONSTRAINT authorIdConstraint FOR (author:Author) REQUIRE author.id IS UNIQUE;
```
```
CREATE CONSTRAINT paperIdConstraint FOR (paper:Paper) REQUIRE paper.id IS UNIQUE;
```
```
CREATE CONSTRAINT journalIdConstraint FOR (journal:Journal) REQUIRE journal.id IS UNIQUE;
```
```
CREATE CONSTRAINT conferenceIdConstraint FOR (conference:Conference) REQUIRE conference.id IS UNIQUE;
```
```
CREATE CONSTRAINT categoryIdConstraint FOR (category:Category) REQUIRE category.name IS UNIQUE;
```

### CSV Loadings
#### Load Authors
```Cypher
LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
```
#### Load Papers
```Cypher
LOAD CSV WITH HEADERS FROM "file:///papers-processed.csv" AS rowPaper
CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year: toInteger(rowPaper.year), url: rowPaper.url, openAcces: toBoolean(rowPaper.isopenaccess), publicationDate: date(rowPaper.publicationdate), updated: rowPaper.updated, DOI:rowPaper.DOI, PubMedCentral: rowPaper.PubMedCentral, PubMed:rowPaper.PubMed, DBLP: rowPaper.DBLP, ArXiv: rowPaper.ArXiv, ACL: rowPaper.ACL, MAG: rowPaper.MAG});     
```
#### Load Journals
```Cypher
LOAD CSV WITH HEADERS FROM "file:///journals.csv" AS rowJournal
CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, issn: rowJournal.issn, url: rowJournal.url});
```
### Load Volume
```Cypher
LOAD CSV WITH HEADERS FROM "file:///volume-from.csv" AS row
MATCH (j:Journal {id:row.journalID})
CREATE (j)<-[:VOLUME_FROM]-(v: Volume {id: row.volumeID, year: toInteger(row.year), volume: toInteger(row.volume)});
```
#### Load Conferences
```Cypher
LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
CREATE (c:Conference {id: rowConference.conferenceID, name: rowConference.conferenceName, issn: rowConference.issn, url: rowConference.url});
```
### Load Editions
```Cypher
LOAD CSV WITH HEADERS FROM "file:///is-from.csv" AS rowEdition
MATCH (conference:Conference {id: rowEdition.conferenceID})
CREATE (e:Edition {id: rowEdition.editionID, edition: toInteger(rowEdition.edition), startDate: date(rowEdition.startDate), endDate: date(rowEdition.endDate)})-[:IS_FROM]->(conference);
```
### Relationships
#### Paper - [WRITTEN_BY {corresponding_author: }] -> Author
```Cypher
LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
MATCH (author:Author {id: toInteger(rowRelation.authorID)})
MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
CREATE (paper)-[:WRITTEN_BY{corresponding_author: toBoolean(rowRelation.is_corresponding)}]->(author);
```

#### Paper - [REVIEWED_BY {with_grade: }] -> Reviewer
```Cypher
LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
```

#### Paper - [BELONGS_TO] -> Edition
```Cypher
LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
MATCH (edition: Edition {id:rowBelongs.venueID})
CREATE (paper)-[:BELONGS_TO]->(edition);
```

#### Paper - [PUBLISHED_IN] -> Volume
```Cypher
LOAD CSV WITH HEADERS FROM "file:///published-in.csv" AS row
MATCH (volume:Volume {id: row.venueID})
MATCH (paper:Paper {id: toInteger(row.paperID)})
CREATE (paper)-[:PUBLISHED_IN { startPage: row.startPage, endPage: row.endPage} ]->(volume);
```

#### Paper - [CITED_BY] -> Paper
```Cypher
LOAD CSV WITH HEADERS FROM "file:///cited-by.csv" AS rowRel
MATCH (p1:Paper {id: toInteger(rowRel.paperID_cited)})
MATCH (p2:Paper {id: toInteger(rowRel.paperID_citing)})
CREATE (p1)-[:CITED_BY]->(p2);
```

#### Paper - [RELATED_TO] -> Keyword
```Cypher
LOAD CSV WITH HEADERS FROM "file:///related-to.csv" AS rowCategory
MATCH (p1:Paper {id: toInteger(rowCategory.paperID)})
MATCH (k:Keyword {keyword: rowCategory.keyword})
CREATE (p1)-[:RELATED_TO]->(k);
```

### Adding external attributes
#### Adding Abstracts to Papers
```Cypher
LOAD CSV WITH HEADERS FROM 'file:///abstracts-sample.csv' AS rowAbstract
MATCH (p:Paper {id: toInteger(rowAbstract.corpusid)}) SET p.abstract=rowAbstract.abstract;
```
### Updates
#### Accepted/Non-accepted status
```Cypher
MATCH (p:Paper) 
OPTIONAL MATCH (p)-[e:REVIEWED_BY]->(:Author)
WITH p, COUNT(e) as numRev, COUNT(CASE WHEN e.with_grade>2 THEN 1 END) as numApp
WHERE numRev/2 < numApp
SET p.approved = true
```