Row vs Column Oriented Databases
----

## 문서 목적
Row vs Column Oriented Databases 내용을 정리하기 위한 문서이다.


## 개요
Row oriented databases
- Row oriented databases are databases that organize data by **record**, keeping all of the data associated with a record next to each other in memory.
- the traditional way of organizing data
- still provide some key benefits for storing data quickly
- optimized for reading and writing rows efficiently

Common row oriented databases
- Postgresql
- MySQL


Column oriented databases
- Column oriented databases are databases that organize data by **field**, keeping all of the data associated with a field next to each other in memory.
- Columnar databases have grown in popularity and provide performance advantages to querying data.
- They are optimized for reading and computing on columns efficiently.

Common column oriented databases
- Redshift
- BigQuery
- Snowflake

## Row oriented databases
Traditional Database Management Systems were created to store data. They are optimized to read and write a single row of data which lead to a series of design choices including having a row store architecture.

In a row store, or row oriented database, the data is stored row by row, such that the first column of a row will be next to the last column of the previous row.
- 이전 행의 마지막 - 다음 행의 처음인 구조

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling1.png)



![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling2.png)


This allows the database write a row quickly because, all that needs to be done to write to it is to tack on another row to the end of the data.


### Writing to Row Store Databases

이런 상태라고 하자
![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling3.png)

그리고 새로운 row가 추가된다고 할 때
![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling4.png)

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling5.png)

Online Transactional Processing (OLTP) style applications에 잘 어울리고 여전히 쓰이고 있음


### Reading from Row Store Databases
Row oriented databases are fast at retrieving a row or a set of rows
- but when performing an aggregation it brings extra data (columns) into memory which is slower than only selecting the columns that you are performing the aggregation on.
- 행 또는 행 집합을 검색하는데는 빠르지만 집계를 수행할 때 집계를 수행하는 열만 선택하는 것보다 느린 추가 데이터를 메모리로 가져옴
- row 지향 데이터 베이스가 접근하는 디스크 수도 일반적으로 더 크다


### Extra data into Memory
집계를 하고 싶으면 3개의 row를 다 가져와서 메모리에 올려야 한다.

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling6.png)

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling7.png)

row 기반에 디스크가 나누어져 있다면 3개의 디스크를 다 살펴봐야 함
- 데이터를 빠르고 쉽게 추가할 수 있지않 데이터를 가져 오려면 추가 메모리를 사용하고 여러 디스크에 엑세스 해야함


## Column oriented databases
데이터 분석을 지원하기 위해 DW가 만ㄷ르어지고, 읽기에 최적화 되어 있다
- column 기반 데이터베이스에서는 데이터는 열의 각 행이 동일한 열의 다른 행 옆에 저장됨

우선 동일한 테이블이 있다고 하자
![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling8.png)

테이블은 행별로 순서대로 한 번에 한 열씩 저장
![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling9.png)

### Writing to a Column Store Databases
새로운 record를 입력한다고 하자

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling10.png)

아래와 같이 들어간다.

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling11.png)

column oriented databases will have significant benefits when stored on separate disks.

![alt text](https://dataschool.com/assets/images/data-modeling-101/row_vs_col_databases/modeling12.png)

### Reading from a Column store Database
만약에 나이에 대한 합계를 구한다고 하면...
- To get the sum of the ages the computer only needs to go to one disk (Disk 3) and sum all the values inside of it. 
- No extra memory needs to be pulled in, and it accesses a minimal number of disks.
- disk3에만 접근하면 된다.

While this is a slight over simplification, it illustrates that by organizing data by column the number of disks that will need to be visited will be reduced and the amount of extra data that has to be held in memory is minimized. This greatly increases the overall speed of the computation.
- 계산 속도가 올라간다
- 메모리가 최소화 된다

## 출처
- https://dataschool.com/data-modeling-101/row-vs-column-oriented-databases/

