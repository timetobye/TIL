Presto & AWS Athena
-----

## 문서 목적
이 문서는 Presto 와 AWS Athena 에서 사용하는 문법을 학습하고 정리하기 위해 작성하였습니다.

## 안내 사항
Presto & AWS Athena 는 ANSI-SQL을 사용합니다.
- 공식 페이지 : [Presto](https://prestodb.io/docs/current/index.html), [AWS Athena](https://aws.amazon.com/ko/athena/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc)

이 문서에서는 주로 문법적인 것을 작성해두었습니다.
- 엔지니어링 적은 요소는 없습니다.
- 쿼리 연습용 입니다.
- Presto 공식 문서를 기반으로 학습 하였습니다. 순서는 작성자 마음대로
- 알고 있는 내용은 깊게 작성하지 않았습니다. 복습 차원에서 가볍게 작성한 것도 많습니다.

## 8. Functions and Operators
함수 위주로 학습합니다.
- 쿼리를 작성할 때 가장 많이 사용하는 날짜 함수, 집계 함수 등
- https://prestodb.io/docs/current/functions.html


### 8.3. Conditional Expressions

#### CASE

The standard SQL CASE expression has two forms. The “simple” form searches each value expression from left to right until it finds one that equals expression:
```sql
CASE expression
    WHEN value THEN result
    [ WHEN ... ]
    [ ELSE result ]
END


-- Example 
SELECT a,
       CASE a
           WHEN 1 THEN 'one'
           WHEN 2 THEN 'two'
           ELSE 'many'
       END
```


The “searched” form evaluates each boolean condition from left to right until one is true and returns the matching result:


```sql
CASE
    WHEN condition THEN result
    [ WHEN ... ]
    [ ELSE result ]
END

-- Example 
SELECT a, b,
       CASE
           WHEN a = 1 THEN 'aaa'
           WHEN b = 2 THEN 'bbb'
           ELSE 'ccc'
       END
```


#### IF

The IF function is actually a language construct that is equivalent to the following CASE expression:

```sql
CASE
    WHEN condition THEN true_value
    [ ELSE false_value ]
END
```

```sql
select
    IF((value / 2) = 0, 'y', 'n')
from table_name
```


#### COALESCE
COALESCE을 이용하여 값이 존재하면 my_field를, null 일 경우 0

```sql
coalesce(my_field,0)
```

#### NULLIF
Returns null if value1 equals value2, otherwise returns value1.

```sql
nullif(value1, value2)
``` 

#### TRY

```sql
try(expression)
```

Evaluate an expression and handle certain types of errors by returning NULL.

In cases where it is preferable that queries produce NULL or default values instead of failing when corrupt or invalid data is encountered, the TRY function may be useful. To specify default values, the TRY function can be used in conjunction with the COALESCE function.

The following errors are handled by TRY:
- Division by zer
- Invalid cast or function argument
- Numeric value out of range


**Examples**

```sql
SELECT * FROM shipping;

 origin_state | origin_zip | packages | total_cost
--------------+------------+----------+------------
 California   |      94131 |       25 |        100
 California   |      P332a |        5 |         72
 California   |      94025 |        0 |        155
 New Jersey   |      08544 |      225 |        490
(4 rows)

-- Query failure without TRY:


SELECT CAST(origin_zip AS BIGINT) FROM shipping;

Query failed: Can not cast 'P332a' to BIGINT


-- NULL values with TRY:

SELECT TRY(CAST(origin_zip AS BIGINT)) FROM shipping;

 origin_zip
------------
      94131
 NULL
      94025
      08544
(4 rows)

-- 응용하면 다음과 같이도 가능하다.

SELECT COALESCE(TRY(total_cost / packages), 0) AS per_package FROM shipping;
```


## TO-DO list
- https://prestodb.io/docs/current/sql/select.html