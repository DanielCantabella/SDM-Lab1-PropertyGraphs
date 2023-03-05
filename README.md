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
CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, issn: rowJournal.issn, url: rowJournal.url});
```
#### Load Conferences
```
LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
CREATE (c:Conference {id: rowConference.venueID, name: rowConference.conferenceName, edition: toINteger(rowConference.edition),issn: rowConference.issn,url:rowConference.url, startDate: date(rowConference.startDate), endDate: date(rowConference.endDate)});
```
#### Load Categories
```
LOAD CSV WITH HEADERS FROM "file:///uniqueCategories.csv" AS rowCategory
CREATE (c:Category {name: rowCategory.categoryName});
```

### Relationships
#### Paper - [WRITTEN_BY {corresponding_author: }] -> Author
```
LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
MATCH (author:Author {id: toInteger(rowRelation.authorID)})
MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
CREATE (paper)-[:WRITTEN_BY{corresponding_author: toBoolean(rowRelation.is_corresponding)}]->(author);
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
#### Paper - [IS_ABOUT] -> Category
```
LOAD CSV WITH HEADERS FROM "file:///categoriesRelations.csv" AS rowCategory
MATCH (category:Category {name: rowCategory.categoryName})
MATCH (paper:Paper {id: toInteger(rowCategory.paperID)})
CREATE (paper)-[:IS_ABOUT]->(category);
```

### Adding external attributes
#### Adding Abstracts to Papers
```
LOAD CSV WITH HEADERS FROM 'file:///abstracts-sample.csv' AS rowAbstract
MATCH (p:Paper {id: toInteger(rowAbstract.corpusid)}) SET p.abstract=rowAbstract.abstract;
```
### Updates
#### Accepted/Non-accepted status
```
MATCH (p:Person)-[l:REVIEWED_BY]->(r:Author) WITH count(l) AS connexions, COUNT(l.with_grade=5) AS approved  WHERE approved > connexions/2 RETURN count(*);
```