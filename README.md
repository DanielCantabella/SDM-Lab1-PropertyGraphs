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
CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year:toInteger(rowPaper.year), url: rowPaper.url, openAcces: toBoolean(rowPaper.isopenaccess), publicationDate:date(rowPaper.publicationdate), updated: rowPaper.updated,DOI:rowPaper.DOI, PubMedCentral: rowPaper.PubMedCentral, PubMed:rowPaper.PubMed, DBLP: rowPaper.DBLP, ArXiv: rowPaper.ArXiv, ACL: rowPaper.ACL, MAG: rowPaper.MAG});
```
#### Load Journals
```Cypher
LOAD CSV WITH HEADERS FROM "file:///journals.csv" AS rowJournal
CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, issn: rowJournal.issn, url: rowJournal.url});
```
#### Load Conferences
```Cypher
LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
CREATE (c:Conference {id: rowConference.venueID, name: rowConference.conferenceName, edition: toINteger(rowConference.edition),issn: rowConference.issn,url:rowConference.url, startDate: date(rowConference.startDate), endDate: date(rowConference.endDate)});
```
#### Load Categories
```Cypher
LOAD CSV WITH HEADERS FROM "file:///uniqueCategories.csv" AS rowCategory
CREATE (c:Category {name: rowCategory.categoryName});
```

### Relationships
#### Paper - [WRITTEN_BY {corresponding_author: }] -> Author
```Cypher
LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
MATCH (author:Author {id: toInteger(rowRelation.authorID)})
MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
CREATE (paper)-[:WRITTEN_BY{corresponding_author: toBoolean(rowRelation.is_corresponding)}]->(author);
```

#### citingPaper - [REFERENCES] -> citedPaper
```Cypher
LOAD CSV WITH HEADERS FROM "file:///citations-sample.csv" AS rowCitation
MATCH (citingPaper:Paper {id: toInteger(rowCitation.citingcorpusid)})
MATCH (citedPaper:Paper {id: toInteger(rowCitation.citedcorpusid)})
CREATE (citingPaper)-[:REFERENCES]->(citedPaper);
```

#### Paper - [REVIEWED_BY {with_grade: }] -> Reviewer
```Cypher
LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
```
#### Paper - [PUBLISHED_IN] -> Journal
```Cypher
LOAD CSV WITH HEADERS FROM "file:///published-in.csv" AS rowPublished
MATCH (journal:Journal {id: rowPublished.venueID})
MATCH (paper:Paper {id: toInteger(rowPublished.paperID)})
CREATE (paper)-[:PUBLISHED_IN{year: toInteger(rowPublished.year), volume: toInteger(rowPublished.volume),startPage: toInteger(rowPublished.startPage), endPage: toInteger(rowPublished.endPage)}]->(journal);
```
#### Paper - [BELONGS_TO] -> Conference
```Cypher
LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
MATCH (conference:Conference {id: rowBelongs.venueID})
MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
CREATE (paper)-[:BELONGS_TO]->(conference);
```
#### Paper - [IS_ABOUT] -> Category
```Cypher
LOAD CSV WITH HEADERS FROM "file:///categoriesRelations.csv" AS rowCategory
MATCH (category:Category {name: rowCategory.categoryName})
MATCH (paper:Paper {id: toInteger(rowCategory.paperID)})
CREATE (paper)-[:IS_ABOUT]->(category);
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