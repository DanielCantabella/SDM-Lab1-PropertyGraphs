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

### CSV Loadings
#### Load Authors
```
LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
```
#### Load Papers
```
LOAD CSV WITH HEADERS FROM "file:///papers-sample.csv" AS rowPaper
CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year:toInteger(rowPaper.year)});
```
#### Load Journals
```
LOAD CSV WITH HEADERS FROM "file:///journals.csv" AS rowJournal
CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, pages: rowJournal.pages, volume: rowJournal.volume});
```
#### Load Conferences
```
LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
CREATE (c:Conference {id: rowConference.venueID, name: rowConference.conferenceName, edition: rowConference.edition, date: rowConference.date});
```

### Relationships
#### Paper - [WRITTEN_BY {corresponding_author: }] -> Author
```
LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
MATCH (author:Author {id: toInteger(rowRelation.authorID)})
MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
CREATE (paper)-[:WRITTEN_BY{corresponding_author: rowRelation.is_corresponding}]->(author);
```

#### citingPaper - [REFERENCES] -> citedPaper
```
LOAD CSV WITH HEADERS FROM "file:///citations-sample.csv" AS rowCitation
MATCH (citingPaper:Paper {id: toInteger(rowCitation.citingcorpusid)})
MATCH (citedPaper:Paper {id: toInteger(rowCitation.citedcorpusid)})
CREATE (citingPaper)-[:REFERENCES]->(citedPaper);
```

#### Paper - [REVIEWED_BY {with_grade: }] -> Reviewer
```
LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
```
#### Paper - [BELONGS_TO] -> Journal
```
LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
MATCH (journal:Journal {id: rowBelongs.venueID})
MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
CREATE (paper)-[:BELONGS_TO]->(journal);
```
#### Paper - [BELONGS_TO] -> Conference
```
LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
MATCH (conference:Conference {id: rowBelongs.venueID})
MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
CREATE (paper)-[:BELONGS_TO]->(conference);
```


### Adding external attributes
#### Adding Abstracts to Papers
```
LOAD CSV WITH HEADERS FROM 'file:///abstracts-sample.csv' AS rowAbstract
MATCH (p:Paper {id: toInteger(rowAbstract.corpusid)}) SET p.abstract=rowAbstract.abstract;
```
