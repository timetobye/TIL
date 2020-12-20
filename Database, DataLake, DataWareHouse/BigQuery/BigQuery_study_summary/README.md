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





----------------

# 6장 빅쿼리 아키텍처
6장에서는 빅쿼리의 내부 작동에 자세히 설명


## 아키텍처 살펴보기
빅쿼리는 구글 클라우드의 모든 리전에 걸친 여러 가용성 존(availability zone)에서 실행 중인 서로 연관된 여러 마이크로서비스가 수십만 개의 태스크를 실행하는 대용량 분산 시스템
- 모든 컴포넌트를 설명하려면 책에 다 담을 수가 없음...


## 쿼리 요청의 수명
이해를 하기 위해서는 고수준 컴포넌트 위주로 살펴보기
- 가장 간단한 쿼리인 select 17 같은 초간단 SQL 쿼리를 실행해보자

-[ ] 그림 넣기


### 1단계 : HTTP POST
클라이언트 -> 빅쿼리 엔드포인트(end ppoint)에 HTTP POST 요청을 보낸다
- 이 요청은 라이브러리 또는 자바 데이터베이스 커넥티비티(JDBC) 드라이버로 감싸져 있지만, 기본적으로 curl이나 HTTP 요청을 보낼 수 있는 다른 도구를 이용해서 쿼리 실행할 수 있음

```bash
POST /bigquery/v2/projects/bigquery-e2e/jobs HTTP/1.1 User-Agent: curl/7.30.0
Host : www.googleapis.com
Accept : */*
Authorization : Bearer <redacted> 
Content-Type : application/json
Content-Length : 
{'configuration' : {'query' : {'query' : 'SELECT 17'}}}
```

중요 포인트
- 새로운 쿼리 작업을 생성해서 상태를 변경 하고 있다 -> HTTP 동사로 POST를 사용한다.
- 인증 토큰 : 인증 토큰은 여러분을 표현하는 OAuth2 토큰
- JSON 페이로드 : 쿼리를 실행할 것이며, 실행할 쿼리 텍스트는 SELECT 17 이라는 것을 표현

- [ ] 그림 넣기


### 2단계 : 라우팅
**HTTP POST 요청은 인터넷의 힘을 빌려 REST 엔드포인트로 라우트 된다.**
- 엔드포인트 : http://www.googleapis.com/bigquery/v2/projects/bigquery-e2e/jobs
- 라우트 : 라우팅(영어: routing)은 어떤 네트워크 안에서 통신 데이터를 보낼 때 최적의 경로를 선택하는 과정
- 엔드포인트는 구글 프론트엔드가 실행 중인 서버를 가리키며, 같은 종류의 서버가 구글 검색 및 다른 구글 제품도 서비스 하고 있다.

어떻게 빅쿼리는 요청을 어느 리전으로 보내야 하는지 어떻게 판단할까?
- URL에 힌트가 숨어 있다.
- 몇몇  클라우드 프로젝트는 쿼리의 실행을 허용하는 위치에 제한
- 기업이 한국 내에서 프로젝트를 실행하도록 설정했다면 쿼리를 한국으로 라우트 된다.
- 특정 지역에 예약이 되어 있다면, 특정 지역으로 라우트 됨

예약도 되어 있지 않고, 작업 이름에 작업을 실행할 리전도 없다면?
- 라우터는 쿼리를 분석해서 어떤 데이터셋에 접근해야 하는지 알아냄
- 데이터셋은 리전과 연결되어 있으므로 빅쿼리는 데이터셋의 지역을 찾아 해당 요청을 그 지역으로 라우트함
- 만일 성능에 극도로 민감하거나 혹은 실행 결과의 위치를 제어하고 싶다면 쿼리 요청의 작업 참조 필드를 이용해서 쿼리를 어느 리전으로 라우트할 것인지를 명시

아무 정도도 없으면....
- 라우터는 미국으로 요청을 보낸다
- 라우터는 JSON HTTP 요청을 플랫폼 및 언어에 중립적이며 모든 구글 서비스 간의 커뮤니케이션에 사용되는 직렬화 형식은 프로토콜 버퍼로 변환한다.

### 3단계 : 작업 서버
**빅쿼리 작업 서버는 요청의 상태를 계속해서 추적하는 역할을 담당**

작업 서버는 비동기식으로 작동한다.
- 클라이언트와 빅쿼리 서버 간의 네트워크 연결은 언제든 끊어질 수 있으며...
- 일부 쿼리는 실행에 몇 분에서 길게는 몇 시간까지 걸릴 수 있으므로...
  
작업의 실행으로 프로젝트 비용이 발생할 수 있다.
- 작업 서버는 호출자가 쿼리를 실행할 수 있는 권한을 가지고 있는지 확인
- **실제 테이블에 대한 권한은 쿼리가 시작되기 전에는 확인하지 않는다.**

작업 서버는 요청을 올바른 쿼리 서버로 전달하는 역할도 담당
- 대부분 쿼리 서버는 주(primary) 가용성 존과 보조(secondary) 가용성 존으로 구성
- 주 가용성 존이 사용 불가능해지면 쿼리는 보조 가용성 존으로 라우트 된다.


프로젝트 데이터 리밸런싱
- 정리하기


### 4단계 : 쿼리 엔진
쿼리는 전반적인 쿼리의 실행을 책임지는 쿼리 마스터(query master)로 라우트 된다.
- 쿼리 마스터는 메타데이터 서버에 연결해 물리적으로 데이터가 어디에 위치하는지, 그리고 어떻게 파티션되어 있는지 알아낸다.(~~오...?~~) 
- 이 단계에서 파티션 프루닝(pruning)이 발생하므로 쿼리가 전체 파티션을 읽지 못하면 활성 파티션의 메타데이터만 반환된다.
  - [파티션 프루닝](https://seoulforest.tistory.com/entry/Partition-Pruning-%ED%8C%8C%ED%8B%B0%EC%85%98-%ED%94%84%EB%A3%A8%EB%8B%9D) : 파티션을 나누어서 SQL 수행시 데이터가 없는 파티션은 읽지 않는

쿼리 서버가 쿼리의 실행에 얼마나 많은 데이터를 사용해야 하는지 판단
- 이 데이터를 예비 쿼리 계획(preliminary query plan)에 대입할 기회가 생기면 쿼리 마스터가 스케줄러에게 슬롯(slot)을 요청
  - 슬롯 : 쿼리 워커 샤드(worker shard)의 실행 스레드이며, 보통 CPU 코어의 절반과 1GB의 RAM을 의미한다.
  - 슬롯은 필요한 리소스의 양이나 구글 데이터 센터의 컴퓨터가 업그레이드 되면서 늘어나거나 줄어들기도 하므로 고정된 크기라고 보기에는 다소 애매
- 스케줄러는 작업을 쿼리 샤드에 어떻게 위임할 것인지를 결정
- 스케줄러는 쿼리 마스터가 슬롯을 요청하면 쿼리를 실행할 샤드의 주소를 반환
- 쿼리 마스터는 그 쿼리를 각각 드레멜 샤드에 병렬로 보냄

### 5단계 : 쿼리 결과의 반환
쿼리 워커 샤드가 쿼리의 실행을 마치면 실행 결과는 크게 두 부분으로 나눠진다.
- 첫 번쨰 페이지는 분산 관계형 데이터베이스인 스패너에 쿼리 메타데이터와 함께 저장됨
- 스패터 데이터는 쿼리가 실행된 것과 같은 리전에 위치한다.
- 나머지 데이터는 구글의 분산 파일시스템인 콜로서스에 기록된다.
- 결과 집합이 작은 쿼리의 경우는 디스크를 건드릴 필요가 없으므로 그 결과가 매우 빠르게 반환된다.

빅쿼리 API는 재연결을 고려해 디자인 되어 있음
- 즉, 최선의 경우에는 동기식 실행 - 타임아웃이 발생하면 API를 호출한 클라이어트가 재연결할 수 있다.
- 이런 방식을 지원하기 위해 작업 서버는 타임아웃이 발생하기 전에 클라이언트에게 작업 ID를 반환하고 클라이언트는 이 작업 ID를 이용해 해당 작업의 결과를 얻게 된다.

빅쿼리 결과는 24시간 동안 저장된다.
- 쿼리 결과는 테이블과 기능적으로 동일하며 테이블과 동일한 방법으로 쿼리할 수 있다.
- 쿼리 결과는 일반적인 Select 쿼리의 경우 10GB까지만 보관
- 더 큰 데이터를 저장하고 싶다면 크기 제한이 없는 CREATE TABLE AS SELECT 또는 INSERT 구문을 사용하면 된다.

 









