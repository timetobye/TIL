SQL vs NoSQL
----

## 문서 목적
SQL vs NoSQL 내용을 정리하기 위한 문서이다.

## SQL Databases

### SQL
정의 및 개요
- Structured Query Language
- it therefore is not a database itself
  - 구조화된 질의 언어이지 데이터베이스가 아님
- only a query language you can use to interact with a specific type of database.
  - 특정 타입의 데이터베이스와 상호작용 할 수 있는 질의 언어이다.
- store, update, delete, retrieve data from relational database management systems(RDBMS - https://techterms.com/definition/rdbms)

특징
- Data is stored in database tables by following a strict data schema (= structure)
  - 엄격한 스키마 정책
- Data is distributed across multiple tables which are connected via relations
  - 데이터는 관계를 통해 연결된 여러 테이블에 걸쳐 분산되어 있다.
  
### Strict Schema
Data is stored as records in tables and each table has a clearly defined structure - a set of fields which defines which data may go into the table and which data may not.
- 테이블 구조가 선언이 되어 있다
- 각각의 필드에 데이터가 들어갈 것이 있고, 아닌 것이 있다

구조는 필드의 네임과 데이터의 타입으로 결정
- The structure is defined regarding the names of the fields as well as the datatypes.

![alt text](https://d33wubrfki0l68.cloudfront.net/cdecf27a4df30fa1b821ef17ddce49991c1eeaf5/fc564/static/c6c8b088e9d9dd4722a965cde6b76e0d/d7ad1/sql-schema.jpg)

테이블을 고치지 않는 이상 스키마에 맞지 않는 데이터를 추가 할 수 없고, 필드도 안 된다.


### Relations
relation 은 무척이나 중요함
- 테이블을 여러 개로 나눔으로써 데이터의 중복을 피할 수 있다.
- 아래의 그림과 같이 users, products, orders로 나누어서 데이터를 저장하고, 각각의 데이터는 다른 테이블에 중복 저장 되지 않도록 함

![alt text](https://d33wubrfki0l68.cloudfront.net/207e129dd3d0320902cb27535a5849e959edb112/bd8ea/static/5df24f0f34a3d98feb531b5fc7776f72/a2510/sql-relations.jpg)

This clear structure can have advantages
- you won’t end up with incorrect data in one of your tables whilst having correct one in all others. 
- That’s a case you won’t run into because data is always only managed in one table, it is not duplicated across tables.

### NoSQL Databases
NoSQL is named like this because it basically follows the opposite approach of SQL databases.
- SQL 이 아닌게 아니다. 
- SQL 과 다른 방식으로 접근한다고 보는게 타당
  - No schemas
  - No relations

you structure data in collections (= tables in the SQL world). 
- collection 이라는 것이 있는데 SQL에서 테이블에 대응하는 거다

Records are now called documents.
- sql의 records는 documents라고 불린다.

단순히 이름만 다른 건 아니고...핵심 차이가 있다.
- 다른 구조를 가지는 데이터를 같은 collection에 넣을 수 있다.
- 테이블 스키마가 정의된 SQL에서는 안 되는 거다.

![alt text](https://d33wubrfki0l68.cloudfront.net/a987a95901540e9687d66bae3ab2a2cf24547753/5cd72/static/986e1a479cf96ceec8a23a0386111fe9/a2510/nosql-no-schema.jpg)

Documents 는 json 같은 거고(여기서는 json으로 일단 함) 스키마에 대해서 걱정할 필요가 없다.
- 일반적으로 관련 있는 데이터를 동일한 collection에 넣음
- order와 관계된 경우는 모두 orders collection에 저장

you would end up with documents that already got everything you need - no need to join multiple tables/ collections.
- 필요한 건 미리 준비가 됨, 데이터를 얻기 위해 여러 테이블이나 collection을 join할 필요가 없음

**NoSQL databases don’t know the concept of joining tables/ collections.**
- You can manually do that (by retrieving a foreign id in collection A and looking it up in collection B) but this will not be your typical flow.
- 외래키 검색으로 할 수는 있는데 일반적인 flow는 아니다

문제는...아래 이미지와 같이 각각의 collection에 중복 데이터가 들어갈 수가 있다.
- you duplicate data across collections so that each collection 
yields exactly the data some part of your app might be looking for.

![alt text](https://d33wubrfki0l68.cloudfront.net/d85caa66fbde232ec4a42f657417486c56bc0f96/0f500/static/bbea2ff32393dedce24d2114b26254fb/d7ad1/nosql-no-relations.jpg)

데이터 중복의 위험성 존재
- B에서 수정 안 했는데, A에서 수정(update)할 위험이 있다.
- It does and it will be your job to ensure that data updates are performed in all collections that use a certain data piece.
  - 특정 데이터 조각(piece)를 사용하는 모든 collection 에서 데이터 업데이트가 수행되도록 해야 한다.

장점!
- 복잡한 join을 할 필요가 없다
- 모든 데이터는 구조화 된 상태로 저장이 되어 있다.
- This is especially great for data that doesn’t change a dozen times every second.
  - 자주 변경되지 않는 데이터일 경우 특히 좋음
  
### Vertical & Horizontal Scaling

Vertical Scaling
- we simply increase the power of the database server - e.g. by upgrading its CPU.
- 스펙을 높이는 것

Horizontal Scaling
- more servers are added
- database is distributed across them
- you still work with one database but multiple servers that host it.

![alt text](https://d33wubrfki0l68.cloudfront.net/ccef1c5780bfa15b2382d32d96eb0810bf8048d5/c3931/static/3d5e1fd10206c1c76da6214c01c7a5f4/a2510/horizontal-and-vertical-scaling.jpg)

데이터를 저장하는 방식에 따라서
- Due to the way data is stored (related tables vs unrelated collections)
- **SQL** databases generally support vertical scaling only
- horizontal scaling is only possible for **NoSQL** databases.

SQL databases do know the concept of sharding
- but it comes with certain restrictions and is typically hard to implement.
- sharding : 테이블을 나누어서 저장하는 것(간략하게 말하면 성씨 별로 저장, id % 4 값으로 저장 등)
- NoSQL databases natively support this and therefore make it way easier to split your database across multiple servers.
  - NoSQL 데이터베이스는 이를 기본적으로 지원하므로 여러 서버에서 데이터베이스를 쉽게 분리 할 수 있습니다.


### 무엇을 써야 하나?
언제나 그렇듯이 상황에 맞게가 최고의 답

#### SQL
Advantages
- Clearly defined schema, data integrity is ensured
- Relations allow you to store each data only once - no duplicates

disadvantages
- Less flexibility, data schema needs to be known and planned in advance (adjusting it later is difficult or maybe even impossible)
- Relations can lead to very complex queries with a lot of JOIN statements
- Horizontal scaling is hard, often only vertical scaling is possible - this means that you’ll face some growth limits (regarding throughput you can handle/ performance) at some point

So when might SQL be best?
- You got related data, used in different “chunks” in different parts of your app, that changes relatively often (you would have to update multiple collections all the time in a NoSQL world)
- A clear schema is important to you and your data is unlikely to change (drastically)

#### NoSQL
Advantages
- Absence of a schema gives you more flexibility - you can adjust your stored data at any point and introduce new “fields”
- Data is stored in the format your app needs it - this speeds up fetching the data
- Vertical and horizontal scaling is possible, hence your database will be able to handle any amount of read/ write requests your app throws at it

disadvantages
- Increased flexibility might lead you to work sloppy and postpone data structure decisions
- Duplicate data means that you have to update multiple collections and documents if that data changes - not just one record in one table as you would do it in the SQL world


When is NoSQL best?
- Exact data requirements or the data itself is unknown or subject to change/ expand
- You require high (read) throughput but you won’t change your data that often (i.e. you don’t need to update dozens of documents for one change all the time)
- You need to scale your database horizontally (i.e. you store enormous amounts of data and have huge read and write throughput)


## 자료 출처
- https://academind.com/learn/web-dev/sql-vs-nosql/
- https://siyoon210.tistory.com/130