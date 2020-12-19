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

## 비교 연산자, 논리 연산
다른 RDBMS랑 유사함
- NaN과 비교는 false 반환
- Null 과의 비교는 Null을 반환
- [표준 SQL 연산자](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators)

## NUMERIC을 사용한 정밀 계산
한계점 : 64비트 영역의 컴퓨터 메모리에 2진수 형태로 저장되는 INT64, FLOAT64는 값의 범위에 제한 존재 -> 사실 거의 문제 없음
재무 회계 프로그램에서는 종종 필요

NUMERIC : 데이터 타입은 38자리 숫자 제공 / 숫자중 9자리는 소수점 아래의 숫자 표시 / 문자열 형태로 지정 직접 Bigquery에서 추출 해야함
- string 으로 된 숫자를 처리함

```sql
WITH example AS (
  SELECT NUMERIC '1.23' AS payment UNION ALL SELECT NUMERIC '7.89'
  UNION ALL SELECT NUMERIC '12.43'
)
SELECT SUM(payment) AS total_paid, AVG(payment) AS average_paid
FROM example
```

## 조건식
- IF, COALESCE, IFNULL
- COALESCE 의 경우 NULL이 아닌 값을 얻을 떄까찌 표현식을 계속 평가하여 처리

```sql
-- COALESCE example

SELECT COALESCE('A', 'B', 'C') as result -> A 가 null이 아니므로 종료

SELECT COALESCE(NULL, 'B', 'C') as result -> NULL 확인 후 B 가 NULL이 아니므로 종료
```

## 타입 변환
Cast 함수를 이용하여 처리
- 실패하면 오류 반환
- 오류 발생 안 시키려면 safe_cast를 사용하여 NULL 반환

## COUNTIF
COUNTIF 는 값을 집계하기 위해 사용함

```sql
COUNTIF(expression)  [OVER (...)]

SELECT COUNTIF(x<0) AS num_negative, COUNTIF(x>0) AS num_positive
FROM UNNEST([5, -2, 3, 6, -10, -7, 4, 0]) AS x;

+--------------+--------------+
| num_negative | num_positive |
+--------------+--------------+
| 3            | 4            |
+--------------+--------------+


SELECT
  x,
  COUNTIF(x<0) OVER (ORDER BY ABS(x) ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS num_negative
FROM UNNEST([5, -2, 3, 6, -10, NULL, -7, 4, 0]) AS x;

+------+--------------+
| x    | num_negative |
+------+--------------+
| NULL | 0            |
| 0    | 1            |
| -2   | 1            |
| 3    | 1            |
| 4    | 0            |
| 5    | 0            |
| 6    | 1            |
| -7   | 2            |
| -10  | 2            |
+------+--------------+
```

### 문자열 함수, 정규표현식
[문자열 함수](https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions)는 다양해서 공식 문서에서 필요할 때마다 참고


## 타임스탬프 다루기, 파싱과 형식화, 타임스탬프 연
타임스탬프 : 위치와 관계없이 절대 시점의 시각을 나타냄
- ISO 8601 참고


```sql
select t1, t2, timestamp_diff(t1, t2, microsecond) t_diff
from (
  select
    timestamp "2017-09-27 12:30:00.45" as t1,
    timestamp "2017-09-27 13:30:00.45+1" as t2)
```

|Row                   |t1        |t2       |t_diff|
|----------------------|----------|---------|------|
|1                     |2017-09-27 12:30:00.450 UTC|2017-09-27 12:30:00.450 UTC|0     |


다양한 형태로 시간 표현을 하지만 표준 표현을 가급적 사용하자
- 표준 형식이 아닌 문자열은 [PARSE_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp)로 처리 가능
- [FORMAT_TIMESTAMP](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp)를 사용하면 원하는 형식으로 타임스탬프 출력 가
- 달력 정보는 EXTRACT 함수 등을 이용하면 추출 가

타임스탬프 연산
- TIMESTAMP_ADD
```sql
TIMESTAMP_ADD(timestamp_expression, INTERVAL int64_expression date_part)
```

- TIMESTAMP_SUB
```sql
TIMESTAMP_SUB(timestamp_expression, INTERVAL int64_expression date_part)
```
- TIMESTAMP_DIFF
```sql
TIMESTAMP_DIFF(timestamp_expression_a, timestamp_expression_b, date_part)
```

```sql
select
  extract(time from timestamp_add(t1, interval 1 hour)) plus_1h,
  extract(time from timestamp_sub(t1, interval 10 minute)) as minus_10min,
  timestamp_diff(current_timestamp(), timestamp_sub(current_timestamp(), interval 1 minute), second) as plus_1min,
  timestamp_diff(current_timestamp(), timestamp_add(current_timestamp(), interval 1 minute), second) as minus_1min
from (select timestamp "2017-09-27 12:30:00.45" as t1)
```
















