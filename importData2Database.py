from neo4j import GraphDatabase
# password=open('password.txt').readline()
# print(password)
# driver = GraphDatabase.driver("bolt://localhost:7687",auth=("dani", "password"))

driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j", "admin123"))

with driver.session() as session:
    # session.run('''
    # CREATE CONSTRAINT authorIdConstraint FOR (author:Author) REQUIRE author.id IS UNIQUE;
    # ''')
    #
    # session.run('''
    # CREATE CONSTRAINT paperIdConstraint FOR (paper:Paper) REQUIRE paper.id IS UNIQUE;
    # ''')
    #
    # session.run('''
    # CREATE CONSTRAINT journalIdConstraint FOR (journal:Journal) REQUIRE journal.id IS UNIQUE;
    # ''')
    #
    # session.run('''
    # CREATE CONSTRAINT conferenceIdConstraint FOR (conference:Conference) REQUIRE conference.id IS UNIQUE;
    # ''')
    # session.run('''
    # CREATE CONSTRAINT categoryIdConstraint FOR (category:Category) REQUIRE category.name IS UNIQUE;
    # ''')

    # session.run('''
    #     CREATE CONSTRAINT keywordConstraint FOR (keyword:Keyword) REQUIRE keyword.keyword IS UNIQUE;
    #     ''')

    #LOAD AUTHORS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///authors-sample.csv" AS rowAuthor
    CREATE (a:Author {id: toInteger(rowAuthor.authorid), name: rowAuthor.name, url: rowAuthor.ur});
    ''')
    #LOAD PAPERS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///papers-processed.csv" AS rowPaper
    CREATE (p:Paper {id: toInteger(rowPaper.corpusid), title: rowPaper.title, year:toInteger(rowPaper.year), url: rowPaper.url, openAcces: toBoolean(rowPaper.isopenaccess), publicationDate:date(rowPaper.publicationdate), updated: rowPaper.updated,DOI:rowPaper.DOI, PubMedCentral: rowPaper.PubMedCentral, PubMed:rowPaper.PubMed, DBLP: rowPaper.DBLP, ArXiv: rowPaper.ArXiv, ACL: rowPaper.ACL, MAG: rowPaper.MAG});
     ''')
    #LOAD JOURNALS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///journals.csv" AS rowJournal
    CREATE (j:Journal {id: rowJournal.venueID, name: rowJournal.journalName, issn: rowJournal.issn, url: rowJournal.url});
    ''')
    #LOAD CONFERENCES
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///conferences.csv" AS rowConference
    CREATE (c:Conference {id: rowConference.venueID, name: rowConference.conferenceName, edition: toINteger(rowConference.edition),issn: rowConference.issn,url:rowConference.url, startDate: date(rowConference.startDate), endDate: date(rowConference.endDate)});
    ''')
    #LOAD CATEGORIES
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///uniqueCategories.csv" AS rowCategory
    CREATE (c:Category {name: rowCategory.categoryName});
    ''')

    #ADD WRITTEN_BY RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///written-by.csv" AS rowRelation
    MATCH (author:Author {id: toInteger(rowRelation.authorID)})
    MATCH (paper:Paper {id: toInteger(rowRelation.paperID)})
    CREATE (paper)-[:WRITTEN_BY{corresponding_author: toBoolean(rowRelation.is_corresponding)}]->(author);
    ''')
    #ADD REFERENCES RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///citations-sample.csv" AS rowCitation
    MATCH (citingPaper:Paper {id: toInteger(rowCitation.citingcorpusid)})
    MATCH (citedPaper:Paper {id: toInteger(rowCitation.citedcorpusid)})
    CREATE (citingPaper)-[:REFERENCES]->(citedPaper);
    ''')
    #ADD REVIEWED_BY RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///reviewed-by.csv" AS rowReview
    MATCH (reviewer:Author {id: toInteger(rowReview.reviewerID)})
    MATCH (paper:Paper {id: toInteger(rowReview.paperID)})
    CREATE (paper)-[:REVIEWED_BY {with_grade: toInteger(rowReview.grade)}]->(reviewer);
    ''')
    # ADD BELONGS_TO RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///belongs-to.csv" AS rowBelongs
    MATCH (conference:Conference {id: rowBelongs.venueID})
    MATCH (paper:Paper {id: toInteger(rowBelongs.paperID)})
    CREATE (paper)-[:BELONGS_TO]->(conference);
    ''')

    # ADD PUBLISHED_IN RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///published-in.csv" AS row
    MATCH (journal:Journal {id: row.venueID})
    MATCH (paper:Paper {id: toInteger(row.paperID)})
    CREATE (paper)-[:PUBLISHED_IN {year: toInteger(row.year), volume: row.volume, startDate: row.startDate, endDate: row.endDate} ]->(journal);
    ''')
    #ADD IS_ABOUT RELATIONS
    session.run('''
    LOAD CSV WITH HEADERS FROM "file:///categoriesRelations.csv" AS rowCategory
    MATCH (category:Category {name: rowCategory.categoryName})
    MATCH (paper:Paper {id: toInteger(rowCategory.paperID)})
    CREATE (paper)-[:IS_ABOUT]->(category);
    ''')

    #ADD ABSTRACTS
    session.run('''
    LOAD CSV WITH HEADERS FROM 'file:///abstracts-sample.csv' AS rowAbstract
    MATCH (p:Paper {id: toInteger(rowAbstract.corpusid)}) SET p.abstract=rowAbstract.abstract;
     ''')

    # LOAD KEYWORDS
    session.run('''
            LOAD CSV WITH HEADERS FROM "file:///keywords.csv" AS rowKw
            CREATE (k:Keyword {keyword: rowKw.keyword});
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
