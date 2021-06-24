Cumulative sum that reset when 0 is encountered
----

### 문서 목적
누적 합계를 구할 때 특정 값에 도달하거나, 넘을 경우 초기화 하면서 다시 누적 합계를 구하는 방법에 대해 기술

### 문제 개요
Window function 을 이용하여 누적 합계를 구할 때 특정 조건에 해당 할 경우 해당 row의 누적 합은 0으로 초기화를 해야 하는 문제

예를 들면 value 값이 0일 경우 누적 합을 하지 않고, 누적 값을 초기화 처리해야 한다.

|no|value|cumulative_sum|
|----------------------|----------------------|----|
|1|1|1|
|2|2|3|
|3|0|0|
|4|3|3|
|5|-1|2|
|6|3|5|
|7|0|0|
|8|1|1|

### 문제 해결
Window function 을 좀 더 유연하게 사용하면 해당 문제를 해결할 수 있다.
- value 값이 0 일 경우 flag를 1로 하고 아닐 경우 0으로 한다.
- 이 flag 는 새로운 그룹의 기준이 된다.
- 그 후에 그룹 단위로 다시 누적 합을 구하면 0이 있는 부분을 기준으로 자연스럽게 구역을 나누어서 합계를 구하게 된다.

```sql
select
    no, value, cumulative_group, # 생략해도 됨
    sum(value) over (partition by cumulative_group order by no) as cumulative_sum
from (
    select
        no, value,
        sum(case when value = 0 then 1 else 0 end) over (order by no) as cumulative_group
    from table
) as result_table
```

이렇게 쿼리를 작성하면 특정 값에 해당 할 때 리셋해서 누적 합을 다시 구할 수 있다.

### 참고 문서
- [SQL Server - Cumulative Sum that resets when 0 is encountered](https://stackoverflow.com/questions/50394155/sql-server-cumulative-sum-that-resets-when-0-is-encountered)
