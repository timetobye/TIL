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


### 8.13 Date and Time Functions and Operators

#### Date and Time Operators

|Operator|Example                                          |Result                 |
|--------|-------------------------------------------------|-----------------------|
|+       |date '2012-08-08' + interval '2' day             |2012.8.10              |
|+       |time '01:00' + interval '3' hour                 |04:00:00.000           |
|+       |timestamp '2012-08-08 01:00' + interval '29' hour|2012-08-09 06:00:00.000|
|+       |timestamp '2012-10-31 01:00' + interval '1' month|2012-11-30 01:00:00.000|
|+       |interval '2' day + interval '3' hour             |2 03:00:00.000         |
|+       |interval '3' year + interval '5' month           |3-5                  |
|-       |date '2012-08-08' - interval '2' day             |2012-08-06               |
|-       |time '01:00' - interval '3' hour                 |22:00:00.000           |
|-       |timestamp '2012-08-08 01:00' - interval '29' hour|2012-08-06 20:00:00.000|



#### Date and Time Functions

current_date -> date
- Returns the current date as of the start of the query.

```sql
select current_date 

September 5, 2019, 12:00 AM
```

current_time -> time with time zone
- Returns the current time as of the start of the query.

current_timestamp -> timestamp with time zone
- Returns the current timestamp as of the start of the query.


date(x) → date
- This is an alias for `CAST(x AS date)`.

```sql
select date('2020-09-04')

select cast ('2020-09-04' as date)
```

from_iso8601_timestamp(string) → timestamp with time zone
- Parses the ISO 8601 formatted string into a timestamp with time zone.

from_iso8601_date(string) → date
- Parses the ISO 8601 formatted string into a date.

from_unixtime(unixtime) → timestamp
- Returns the UNIX timestamp unixtime as a timestamp.

from_unixtime(unixtime, string) → timestamp with time zone
- Returns the UNIX timestamp unixtime as a timestamp with time zone using string for the time zone.

from_unixtime(unixtime, hours, minutes) → timestamp with time zone
- Returns the UNIX timestamp unixtime as a timestamp with time zone using hours and minutes for the time zone offset.


now() → timestamp with time zone
- This is an alias for `current_timestamp`.
 
The following SQL-standard functions do not use parenthesis:
- current_date
- current_time
- current_timestamp
- localtime
- localtimestamp

#### Truncation Function
The date_trunc function supports the following units:

|Unit|Example Truncated Value                          |Query|
|----|-------------------------------------------------|------|
|second|2001-08-22 03:04:05.000                          |select date_trunc('second', timestamp '2001-08-22 03:04:05.321')|
|minute|2001-08-22 03:04:00.000                          |select date_trunc('minute', timestamp '2001-08-22 03:04:05.321')|
|hour|2001-08-22 03:00:00.000                          |select date_trunc('hour', timestamp '2001-08-22 03:04:05.321')|
|day |2001-08-22 00:00:00.000                          |select date_trunc('day', timestamp '2001-08-22 03:04:05.321')|
|week|2001-08-20 00:00:00.000                          |select date_trunc('week', timestamp '2001-08-22 03:04:05.321')|
|month|2001-08-01 00:00:00.000                          |select date_trunc('month', timestamp '2001-08-22 03:04:05.321')|
|quarter|2001-07-01 00:00:00.000                          |select date_trunc('quarter', timestamp '2001-08-22 03:04:05.321')|
|year|2001-01-01 00:00:00.000                          |select date_trunc('year', timestamp '2001-08-22 03:04:05.321')|

date_trunc(unit, x) → [same as input]
- Returns x truncated to unit.

example
- 2001-08-22 03:04:05.321


#### Interval Functions
The functions in this section support the following interval units:

|Unit|Description                                      |query|
|----|-------------------------------------------------|------|
|millisecond|Milliseconds                                     |select date_add('millisecond', 32, timestamp '2001-08-22 03:04:05.321')|
|second|Seconds                                          |select date_add('second', 32, timestamp '2001-08-22 03:04:05.321')|
|minute|Minutes                                          |select date_add('minute', 32, timestamp '2001-08-22 03:04:05.321')|
|hour|Hours                                            |select date_add('hour', 32, timestamp '2001-08-22 03:04:05.321')|
|day |Days                                             |select date_add('day', 32, timestamp '2001-08-22 03:04:05.321')|
|week|Weeks                                            |select date_add('week', 32, timestamp '2001-08-22 03:04:05.321')|
|month|Months                                           |select date_add('month', 32, timestamp '2001-08-22 03:04:05.321')|
|quarter|Quarters of a year                               |select date_add('quarter', 32, timestamp '2001-08-22 03:04:05.321')|
|year|Years                                            |select date_add('year', 32, timestamp '2001-08-22 03:04:05.321')|


date_add(unit, value, timestamp) → [same as input]
- Adds an interval `value` of type `unit` to `timestamp`. 
- Subtraction can be performed by using a negative value.

date_diff(unit, timestamp1, timestamp2) → bigint
- Returns `timestamp2 - timestamp1` expressed in terms of `unit`.
- 차이를 unit 단위 기준으로 변경해서 전달

#### Duration Function
- 생략


#### MySQL Date Functions
The functions in this section use a format string that is compatible with the MySQL date_parse and str_to_date functions. 
The following table, based on the MySQL manual, describes the format specifiers:
- https://prestodb.io/docs/current/functions/datetime.html


|Specifier|Description                                      |
|---------|-------------------------------------------------|
|%a       |Abbreviated weekday name (Sun .. Sat)            |
|%b       |Abbreviated month name (Jan .. Dec)              |
|%c       |Month, numeric (1 .. 12) [4]                     |
|%D       |Day of the month with English suffix (0th, 1st, 2nd, 3rd, …)|
|%d       |Day of the month, numeric (01 .. 31) [4]         |
|%e       |Day of the month, numeric (1 .. 31) [4]          |
|%f       |Fraction of second (6 digits for printing: 000000 .. 999000; 1 - 9 digits for parsing: 0 .. 999999999) [1]|
|%H       |Hour (00 .. 23)                                  |
|%h       |Hour (01 .. 12)                                  |
|%I       |Hour (01 .. 12)                                  |
|%i       |Minutes, numeric (00 .. 59)                      |
|%j       |Day of year (001 .. 366)                         |
|%k       |Hour (0 .. 23)                                   |
|%l       |Hour (1 .. 12)                                   |
|%M       |Month name (January .. December)                 |
|%m       |Month, numeric (01 .. 12) [4]                    |
|%p       |AM or PM                                         |
|%r       |Time, 12-hour (hh:mm:ss followed by AM or PM)    |
|%S       |Seconds (00 .. 59)                               |
|%s       |Seconds (00 .. 59)                               |
|%T       |Time, 24-hour (hh:mm:ss)                         |
|%U       |Week (00 .. 53), where Sunday is the first day of the week|
|%u       |Week (00 .. 53), where Monday is the first day of the week|
|%V       |Week (01 .. 53), where Sunday is the first day of the week; used with %X|
|%v       |Week (01 .. 53), where Monday is the first day of the week; used with %x|
|%W       |Weekday name (Sunday .. Saturday)                |
|%w       |Day of the week (0 .. 6), where Sunday is the first day of the week [3]|
|%X       |Year for the week where Sunday is the first day of the week, numeric, four digits; used with %V|
|%x       |Year for the week, where Monday is the first day of the week, numeric, four digits; used with %v|
|%Y       |Year, numeric, four digits                       |
|%y       |Year, numeric (two digits) [2]                   |
|%%       |A literal % character                            |
|%x       |x, for any x not listed above                    |



date_format(timestamp, format) → varchar
- Formats timestamp as a string using format.

```sql
select date_format(timestamp '2001-08-22 03:04:05.321', '%Y-%m-%d %h:%i:%s')
```

date_parse(string, format) → timestamp
- Parses string into a timestamp using format.
- 형태를 맞춰줘야 함

```sql
select date_parse('2001-08-22 03:04:05', '%Y-%m-%d %h:%i:%s')
select date_parse('2001-08-22 03:04', '%Y-%m-%d %h:%i')
```

#### Extraction Function
The `extract` function supports the following fields:

|Field|Description                                      |query|
|-----|-------------------------------------------------|-----|
|YEAR |year()                                           |
|QUARTER|quarter()                                        |
|MONTH|month()                                          |
|WEEK |week()                                           |
|DAY  |day()                                            |
|DAY_OF_MONTH|day()                                            |
|DAY_OF_WEEK|day_of_week()                                    |
|DOW  |day_of_week()                                    |
|DAY_OF_YEAR|day_of_year()                                    |
|DOY  |day_of_year()                                    |
|YEAR_OF_WEEK|year_of_week()                                   |
|YOW  |year_of_week()                                   |
|HOUR |hour()                                           |
|MINUTE|minute()                                         |
|SECOND|second()                                         |
|TIMEZONE_HOUR|timezone_hour()                                  |
|TIMEZONE_MINUTE|timezone_minute()                                |

extract(field FROM x) → bigint
- Returns field from x.

```sql
select extract(year from timestamp '2020-08-04 12:34:56') -> 2020

select extract(day from timestamp '2020-08-04 12:34:56') -> 4

select extract(DAY_OF_WEEK from timestamp '2020-08-04 12:34:56') -> 2
```

Convenience Extraction Functions

day(x) → bigint
- Returns the day of the month from x.

```sql
select day(timestamp '2020-08-04 12:34:56')
```