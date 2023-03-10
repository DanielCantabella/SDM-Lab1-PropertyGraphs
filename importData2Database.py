from neo4j import GraphDatabase

# driver = GraphDatabase.driver("bolt://localhost:7687",auth=("dani", "password"))
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j", "admin123"))

with driver.session() as session:

    ## REMOVE ALL NODES:
    session.run('''
    MATCH (n) DETACH DELETE n;
    ''')
    ## REMOVE CONSTRAINTS (IF EXIST):
    session.run('''
    DROP CONSTRAINT authorIdConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT paperIdConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT journalIdConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT conferenceIdConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT categoryIdConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT keywordConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT communityNameConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT volumeConstraint IF EXISTS;
    ''')
    session.run('''
    DROP CONSTRAINT companyIdConstraint IF EXISTS;
    ''')

    # ADD CONSTRAINTS
    session.run('''
    CREATE CONSTRAINT authorIdConstraint FOR (author:Author) REQUIRE author.id IS UNIQUE;
    ''')

    session.run('''
    CREATE CONSTRAINT paperIdConstraint FOR (paper:Paper) REQUIRE paper.id IS UNIQUE;
    ''')

    session.run('''
    CREATE CONSTRAINT journalIdConstraint FOR (journal:Journal) REQUIRE journal.id IS UNIQUE;
    ''')

    session.run('''
    CREATE CONSTRAINT conferenceIdConstraint FOR (conference:Conference) REQUIRE conference.id IS UNIQUE;
    ''')
    session.run('''
    CREATE CONSTRAINT categoryIdConstraint FOR (category:Category) REQUIRE category.name IS UNIQUE;
    ''')

    session.run('''
    CREATE CONSTRAINT keywordConstraint FOR (keyword:Keyword) REQUIRE keyword.keyword IS UNIQUE;
    ''')

    session.run('''
        CREATE CONSTRAINT volumeConstraint FOR (volume:Volume) REQUIRE volume.id IS UNIQUE;
        ''')

    # LOAD AUTHORS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
    CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
    ''')
    # LOAD PAPERS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///papers-processed.csv" AS rowPaper
    CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year: toInteger(rowPaper.year), url: rowPaper.url, openAcces: toBoolean(rowPaper.isopenaccess), publicationDate: date(rowPaper.publicationdate), updated: rowPaper.updated, DOI:rowPaper.DOI, PubMedCentral: rowPaper.PubMedCentral, PubMed:rowPaper.PubMed, DBLP: rowPaper.DBLP, ArXiv: rowPaper.ArXiv, ACL: rowPaper.ACL, MAG: rowPaper.MAG});
     ''')
    # LOAD KEYWORDS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///keywords.csv" AS rowKw
    CREATE (k:Keyword {keyword: rowKw.keyword});
    ''')
    # LOAD JOURNALS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///journals.csv" AS rowJournal
    CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, issn: rowJournal.issn, url: rowJournal.url});
    ''')
    # LOAD VOLUME
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///volume-from.csv" AS row
    MATCH (j:Journal {id:row.journalID})
    CREATE (j)<-[:VOLUME_FROM]-(v: Volume {id: row.volumeID, year: toInteger(row.year), volume: toInteger(row.volume)});
    ''')
    # LOAD CONFERENCES
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
    CREATE (c:Conference {id: rowConference.conferenceID, name: rowConference.conferenceName, issn: rowConference.issn, url: rowConference.url});
    ''')
    # LOAD EDITIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///is-from.csv" AS rowEdition
    MATCH (conference:Conference {id: rowEdition.conferenceID})
    CREATE (e:Edition {id: rowEdition.editionID, edition: toInteger(rowEdition.edition), startDate: date(rowEdition.startDate), endDate: date(rowEdition.endDate)})-[:IS_FROM]->(conference);
    ''')

    # ADD WRITTEN_BY RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
    MATCH (author:Author {id: toInteger(rowRelation.authorID)})
    MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
    CREATE (paper)-[:WRITTEN_BY{corresponding_author: toBoolean(rowRelation.is_corresponding)}]->(author);
    ''')
    # ADD REVIEWED_BY RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
    MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
    MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
    CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
    ''')
    # ADD BELONGS_TO RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
    MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
    MATCH (edition: Edition {id:rowBelongs.venueID})
    CREATE (paper)-[:BELONGS_TO]->(edition);
    ''')
    # ADD PUBLISHED_IN RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///published-in.csv" AS row
    MATCH (volume:Volume {id: row.venueID})
    MATCH (paper:Paper {id: toInteger(row.paperID)})
    CREATE (paper)-[:PUBLISHED_IN { startPage: row.startPage, endPage: row.endPage} ]->(volume);
    ''')
    # ADD ABSTRACTS (IDs DO NOT COINCIDE!)
    session.run('''
    LOAD CSV WITH HEADERS FROM 'file:///withAbstracts.csv' AS rowAbstract
    MATCH (p:Paper {id: toInteger(rowAbstract.paperID)}) SET p.abstract=rowAbstract.abstract;
     ''')
    # ADD CITED_BY RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///cited-by.csv" AS rowRel
    MATCH (p1:Paper {id: toInteger(rowRel.paperID_cited)})
    MATCH (p2:Paper {id: toInteger(rowRel.paperID_citing)})
    CREATE (p1)-[:CITED_BY]->(p2);
    ''')
    # ADD RELATED_TO RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///related-to.csv" AS rowCategory
    MATCH (p1:Paper {id: toInteger(rowCategory.paperID)})
    MATCH (k:Keyword {keyword: rowCategory.keyword})
    CREATE (p1)-[:RELATED_TO]->(k);
    ''')

### EVOLVING THE GRAPH
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
    MATCH (p:Paper{id: toInteger(rowReview.paperID)})-[r: REVIEWED_BY]->(a:Author{id:toInteger(rowReview.reviewerID)})
    SET r.description = rowReview.review;
    ''')
    session.run('''
    CREATE CONSTRAINT companyIdConstraint FOR (organization:Organization) REQUIRE organization.id IS UNIQUE;
    ''')
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///companies.csv" AS rowCompany
    CREATE (c:Organization {id: rowCompany.companyid, name:rowCompany.company, type:'company'});
    ''')
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///universities.csv" AS rowUniversity
    CREATE (u:Organization {id: rowUniversity.universityid, name:rowUniversity.university, type:'university'});
    ''')
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///affiliated-to.csv" AS rowAffiliated
    MATCH(a:Author{id:toInteger(rowAffiliated.authorID)})
    MATCH(o:Organization{id:rowAffiliated.affiliation})
    CREATE (a)-[:IS_AFFILIATED_TO]->(o);
    ''')

    session.close()





