Schema on Write vs Schema on Read
----

## 문서 목적
**Schema on Write vs Schema on Read**에 대해 정리하기 위한 문서 입니다.

![alt text](https://t1.daumcdn.net/cfile/tistory/993621405A31485517)

![alt text](https://luminousmen.com/media/schema-on-read-vs-schema-on-write.jpg)

![alt text](https://iamluminousmen-media.s3.amazonaws.com/media/schema-on-read-vs-schema-on-write-1.jpg)

## Schema on Write
일반적으로 우리가 자주 사용하는 SQL RDBMS에서 사용되는 방식이다.
- In SQL, you can't add data until **AFTER** the table's schema has been declared.
- 스키마가 정의가 되어 있어야 데이터를 insert 할 수 있고, 쿼리를 할 수 있다.
- If the schema is to be redefined, the table is dropped and re-loaded.
- 데이터의 형태가 미리 정의된 table schema의 속성과 다르면 에러를 발생시킨다.
  - 넣고자 하는 데이터의 형태가 잘못 되었을 경우 미리 인지할 수 있다.

아래와 같은 순서로 작업이 진행 된다.
- Create Schema -> Add data -> Query data

Create Schema
```sql
create table Customers(
  Key int,
  name varchar(40)...
)
```

Add data
```bash
BULK INSERT Customers
From "file path"
with Fieldterminator='","'
```

Query data
```sql
select key, name from Customers
```

장점
- Schema-on-write helps to execute the query faster because the data is already loaded in a strict format and you can easily find the desired data.

단점
- we can't upload data until the table is created and we can't create tables until 
we understand the schema of the data that will be in this table.
- This also leads to problems with changing the data. For example, a source text file has changed, or someone has added data or changed the column type. 
Then we need to drop the table and load all the data again.
- this requires much more preliminary preparation and continuous transformation of incoming data, and the cost of making changes to the schema is high and should be avoided.

## Schema on Read
데이터가 들어올 때 어떤 형식이든 관계가 없다.
- we upload data as it arrives without any changes or transformations
- It is a schema-on-read, it has fast data ingestion because data shouldn't follow any internal schema
  - it's just copying/moving files. This type of data handling is more flexible in case of big data, unstructured data, or frequent schema changes.
- We do not need to change the schemas and reload all the data in the data storage.
- you should understand that some level of schema design is inevitable.
  - 일정 수준의 스키마 디자인은 불가피함을 이해해야 한다.

Reading 할 때
- 테이블 스키마를 정해서 read를 한다.
- when we are reading the data we specify the schema

장점
- Schema-on-read can provide flexibility, scalability, and prevent some human mistakes.
- It is generally recommended that data is stored in the original raw format (just in case) and optimized in another format suitable for further data processing.
- The ETL may have invalid transformations, and the original raw data will allow you to return to the original data and process it correctly.
  - ETL을 할 때 유효하지 않더라도, 원래의 데이터로 돌아갈 수 있다.

단점
- But since the data does not go through strict ETLs and 
transformation into strict data storage schemas, there can be 
a lot of missing or invalid data, duplicates, and many other problems 
that can lead to inaccurate or incomplete query results.
- In addition, since the schema must be defined when querying data, SQL queries tend to be very complex. They take time to write, and even more to complete.
  - query가 복잡함


## 자료 출처
- https://luminousmen.com/post/schema-on-read-vs-schema-on-write
- [schema on Read의 이해](https://datacookbook.kr/90)
- https://www.youtube.com/watch?v=cfEYEah1XMg
- https://www.youtube.com/watch?v=FoJ_V7fDJpk









