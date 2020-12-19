구글 빅쿼리 완벽 가이드
------

# 문서 목적
이 문서는 [구글 빅쿼리 완벽 가이드](http://www.yes24.com/Product/Goods/95562895) 책을 보고 스터디한 내용을 정리한 문서 입니다.

# 안내 사항
코드는 책에서 안내된 [Github](https://github.com/onlybooks/bigquery) 에서 참고하였으나, 가급적 직접 연습하였다.

모든 내용을 적기 보다는 책을 보면서 중요하거나 기억하기 위해 필요한 내용을 정리하였다. 목차는 책에 있는 내용을 참고하였다.

# Table of Contents

--------

# 1장 구글 빅쿼리
구글 빅쿼리
- 서버리스 서비스
- 빠르게 쿼리 처리 가능하며, 인프라 별도 관리가 필요 없음, 인덱스 없음
  - 2019년에 구글 빅쿼리 교육에서 들은 말 중 인상 깊은 것은 인덱스가 없다는 점이었다.
  

관계형 데이터베이스 관리 시스템 + 맵리듀스 프레임워크
- OLTP 작업은 전체를 살펴보거나 애드훅 쿼리에는 적합하지 않음
- 구글에서 2004년에 대용량 분산 병렬 컴퓨팅 처리를 하기 위해 맵리듀스라는 소프트웨어 프레임워크 개발
  - Map : 키/값 쌍을 처리해 중간 키/값 쌍을 처리하는 함수
  - Reduce : 중간 키와 연관된 모든 중간 값을 병합하는 함수
- 직접 구축하면 어려우니까 빅쿼리를 쓰자!

빅쿼리에 대한 짤막 설명
- 데이터 웨어하우스
- RDBMS 처럼 SQL 실행 가능
- 분산 병렬 처리
- 여러 유형의 데이터 저장 가능
- ETL, EL, ELT 모두 지원 가능
- Column 기반으로 제작 : [BigQuery Explained: Storage Overview](https://medium.com/google-cloud/bigquery-explained-storage-overview-70cac32251fa)
- 그외 빅쿼리가 만들어진 역사 소개


# 2장 쿼리 필수 요소
기본적인 SQL 문법을 기반으로 소개되었다.

## select로 행 검색하기
Bigquery는 행을 읽는 작업
- 여러 워커에 분배 -> 각 샤드에서 데이터 읽기 -> 출력 전달
  - 구글 빅쿼리 공식 문서 : [파티션을 나눈 테이블 소개](https://cloud.google.com/bigquery/docs/partitioned-tables#partitioning_versus_sharding)

Partition과 Shard
- Partition : 큰 테이블을 작은 단위의 테이블로 물리적 분할 하여 관리하는 방법
- Partition 의 종류 : 수평(Horizontal) 과 수직(Vertical) 방법이 있다.
  - 수평 파티셔닝은 shard(또는 샤딩 이라고 부른다.) – [Stackoverflow](https://stackoverflow.com/questions/20771435/database-sharding-vs-partitioning)
- 샤딩을 이렇게도 기억을 하고 있다.
  - ㄱ 성씨 ~ ㅎ 성씨를 나누어서 저장한다고 할 떄, 특정 성씨만 조회를 한다면 다른 성씨들은 확인하지 않아도 된다.
  - ㄱ ~ ㅎ 성씨를 다 본다고 하더라도, 하나의 테이블에 다 저장되어서 모든 row를 봐야할 수도 있다.
  - 그러나 하나의 테이블을 모두 보는 것과, 나눠진 테이블을 다 보는 것은 속도 측면에서 차이가 있다고 알고 있다. 
  
  

![alt text](https://miro.medium.com/max/1200/1*yyHih3GveWruzwYgLxTu3w.png)

빅쿼리는 테이블을 읽는 방법이 다른 RDMBS와는 조금 다르다

|빅쿼리 객체                |이름  |특징 및 설명|
|----------------------|----|-------|
|프로젝트(Project)         |`bigquery-public-data`|-백틱(`)을 감싸서 처리할 것, ’-’(하이픈) 뺄셈 처리 방지|
|                      |    |-객체 전체를 감쌀 수 있으나, 테이블 별칭을 사용할 수 없으므로 프로젝트만 백틱 처리|
|                      |    |-데이터셋, 테이블과 연결된 스토리지 소유자|
|데이터셋(Dataset)         |new_york_citibike|-테이블, 뷰에 대한 엑세스 구성 및 제어|
|                      |    |-여러 데이터 셋 생성 가능|
|테이블/뷰                 |citibike_trips|-데이터 셋에 속함|
|(Table / view)        |    |-데이터 로드 전 하나 이상의 데이터셋을 생성 해야함|


## AS로 컬럼 이름에 별칭 지정하기
다른 SQL과 마찬가지로 별칭 지정 가능하다.
- 다만, 지정하지 않으면 빅쿼리가 임의로 지정한다. 예를 들면 `f0._`

## Select *, EXCEPT, REPLACE
빅쿼리를 쓰면서 정말 신기한 기능이라고 생각했던 것 중 하나이다.

컬럼 선택 방법
- 모든 컬럼 선택 -> select *
- 모든 컬럼 선택 + 특정 컬럼 제외
```sql
Select *, except(short_name, last_reported)
``` 
  
- 모든 컬럼 선택 + 특정 컬럼의 값 변환 : AS를 안쪽에 사용해줘야 함
```sql
select * replace(num_bikes_available + 5 as num_bikes_available)
```

- 두 개의 컬럼을 변경해주고 싶다면...
```sql
select * replace(
  num_bikes_available + 5 as num_bikes_available,
  region_id + 5 as region_id)
from `bigquery-public-data`.new_york_citibike.citibike_stations
```

## WITH 사용한 서브쿼리, Order by
WITH의 경우 서브쿼리 역할을 해준다.

기본적으로 빅쿼리에서 쿼리를 하게 되면 출력 결과가 정렬되지 않음
- 왜?
- 분산된 테이블에서 만족하는 결과를 우선해서 올리기 때문이다. 물론 전체적인 쿼리 결과는 다르지 않음


## Groupby, Count, Havin, Distinct
생략

## 배열과 구조체 기초
빅쿼리에서는 Array가 존재한다.
- Array는 쿼리에서 대괄호로 감싸진 부분을 표현한다.


```sql
SELECT * FROM UNNEST([ 'Seattle WA', 'New York', 'Singapore' ]) AS city
```

쿼리를 하면...

```bash
|Row                   |city|
|----------------------|----|
|1                     |Seattle WA|
|2                     |New York|
|3                     |Singapore|
```

아래에 split을 이용하면 분리해서 테이블 결과를 반환할 수 있다.

```sql
select 
  city, SPLIT(city, ' ') AS parts 
from (
    select * 
	from UNNEST(['Seattle WA', 'New York', 'Singapore' ]) AS city 
)
```

```bash
|Row                   |city      |parts    |
|----------------------|----------|---------|
|1                     |Seattle WA|Seattle  |
|                      |          |WA       |
|2                     |New York  |New      |
|                      |          |York     |
|3                     |Singapore |Singapore|
```

## ARRAY_AGG 로 배열 만들기

ARRAY_AGG 로 배열을 만들 수 있다.
- https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg

```sql
ARRAY_AGG([DISTINCT] expression [{IGNORE|RESPECT} NULLS]
          [ORDER BY key [{ASC|DESC}] [, ... ]]  [LIMIT n])
[OVER (...)]
```

```sql
SELECT FORMAT("%T", ARRAY_AGG(x)) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

+-------------------------+
| array_agg               |
+-------------------------+
| [2, 1, -2, 3, -2, 1, 2] |
+-------------------------+


SELECT FORMAT("%T", ARRAY_AGG(DISTINCT x)) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

+---------------+
| array_agg     |
+---------------+
| [2, 1, -2, 3] |
+---------------+


SELECT FORMAT("%T", ARRAY_AGG(x IGNORE NULLS)) AS array_agg
FROM UNNEST([NULL, 1, -2, 3, -2, 1, NULL]) AS x;

+-------------------+
| array_agg         |
+-------------------+
| [1, -2, 3, -2, 1] |
+-------------------+


SELECT FORMAT("%T", ARRAY_AGG(x ORDER BY ABS(x))) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

+-------------------------+
| array_agg               |
+-------------------------+
| [1, 1, 2, -2, -2, 2, 3] |
+-------------------------+


SELECT FORMAT("%T", ARRAY_AGG(x LIMIT 5)) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

+-------------------+
| array_agg         |
+-------------------+
| [2, 1, -2, 3, -2] |
+-------------------+


SELECT
  x,
  FORMAT("%T", ARRAY_AGG(x) OVER (ORDER BY ABS(x))) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

+----+-------------------------+
| x  | array_agg               |
+----+-------------------------+
| 1  | [1, 1]                  |
| 1  | [1, 1]                  |
| 2  | [1, 1, 2, -2, -2, 2]    |
| -2 | [1, 1, 2, -2, -2, 2]    |
| -2 | [1, 1, 2, -2, -2, 2]    |
| 2  | [1, 1, 2, -2, -2, 2]    |
| 3  | [1, 1, 2, -2, -2, 2, 3] |
+----+-------------------------+
```

## 구조체의 배열, 튜플, 배열 활용하기, 배열 풀기
구조체(STRUCT)는 순서를 갖는 필드의 그룹
- 필드에는 원하는 이름을 지정할 수 있으며, 생략하면 빅쿼리에서 이름을 지정
- 가독성을 위해서 지정하자

```sql
SELECT [ 
	STRUCT('male' AS gender, [9306602, 3955871] AS numtrips) , 
	STRUCT('female' AS gender, [3236735, 1260893] AS numtrips) 
] AS bikerides

|Row                   |bikerides.gender|bikerides.numtrips|
|----------------------|----------------|------------------|
|1                     |male            |9306602           |
|                      |                |3955871           |
|                      |female          |3236735           |
|                      |                |1260893           |

```

위의 테이블을 풀려면.... UNNEST 함수를 쓰면 된다.

```sql
SELECT * 
from unnest(
	[ STRUCT('male' AS gender, [9306602, 3955871] AS numtrips) , 
	STRUCT('female' AS gender, [3236735, 1260893] AS numtrips) 
] ) 

|Row                   |gender    |numtrips |
|----------------------|----------|---------|
|1                     |male      |9306602  |
|                      |          |3955871  |
|2                     |female    |3236735  |
|                      |          |1260893  |
```

## 조인의 작동 원리, 각 조인 쿼리
조인은 표준 SQL에서 지원해주는 조인은 다 지원해준다.
- inner, outer, cross, anti(차집합), semi(inner 비슷하나 중복이 없음) 등
- 빅쿼리에서 조인을 하려면 모든 데이터셋이 동일한 리전(region)에 존재 해야함


## 3장 타입, 함수, 연산자

데이터 타입
- INT64 : 정수형, 대략 10^-19 ~ 10^19까지 숫자 지원, 실수형이면 FLOAT64
- NUMERIC : 38자리의 정밀도, 재무 계산이나 과학 계산에 사용
- STRING : 가변 문자 타입
- TIMESTAMP : 시간의 절대 시점
- DATETIME : 달력상의 날짜와 시간을 나타냄
- GEOGRAPHY : 지구 표면의 점, 선, 폴리곤
- STRUCT & ARRAY : 2장에 나옴

여기서부터는 다른 RDBMS에서 사용하고 있는 부분과 유사한 것이 많다.
- ROUND, ABS, power, log, mod 등

분모를 0으로 나눌 때
- 오류가 발생한다
- IEEE_DIVIDE 함수를 사용하면 NAN(Not-a-number)로 반
- 함수 앞에 접두사 Safe를 넣으면 오류 방지 가능 -> null로 반환

```sql
select safe.log(10, -3)
```


























