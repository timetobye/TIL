BigQuery 에서의 JSON 함수 사용 예시
----

## 문서 목적
BigQuery 에서의 JSON 함수 사용 예시를 정리한 문서


## 데이터 안내
두 가지 데이터를 사용
- 직접 json 형태로 구성
- BigQuery 에서 제공하는 Firebase 샘플 데이터를 이용 
 
Firebase 샘플 데이터 조회 방법
```sql
SELECT *
FROM `firebase-public-project.analytics_153293282.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20180501' AND '20240131';
```

## JSON_EXTRACT 또는 JSON_EXTRACT_SCALAR
추출 방법

```sql
JSON_EXTRACT(json_string_expr, json_path_format)는 JSON 값을 STRING으로 반환합니다.
```

```sql
JSON_EXTRACT_SCALAR(json_string_expr, json_path_format)는 스칼라 JSON 값을 STRING으로 반환합니다.
```

```sql
SELECT JSON_EXTRACT(json_text, '$') AS json_text_string
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;
```

```bash
+-----------------------------------------------------------+
| json_text_string                                          |
+-----------------------------------------------------------+
| {"class":{"students":[{"name":"Jane"}]}}                  |
| {"class":{"students":[]}}                                 |
| {"class":{"students":[{"name":"John"},{"name":"Jamie"}]}} |
+-----------------------------------------------------------+
```

```sql
SELECT JSON_EXTRACT(json_text, '$.class.students[0]') AS first_student
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;
```

````bash
+-----------------+
| first_student   |
+-----------------+
| {"name":"Jane"} |
| NULL            |
| {"name":"John"} |
+-----------------+
````

class -> students list 내 1번째 항목(0부터 시작) 의 이름
```sql
SELECT JSON_EXTRACT(json_text, '$.class.students[1].name') AS second_student_name
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name" : null}]}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;
```

```bash
+-------------------+
| second_student    |
+-------------------+
| NULL              |
| NULL              |
| NULL              |
| "Jamie"           |
+-------------------+
```


```sql
SELECT JSON_EXTRACT(json_text, "$.class['students']") AS student_names
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;
```

```bash
+------------------------------------+
| student_names                      |
+------------------------------------+
| [{"name":"Jane"}]                  |
| []                                 |
| [{"name":"John"},{"name":"Jamie"}] |
+------------------------------------+
```

```sql
SELECT JSON_EXTRACT('{ "name" : "Jakob", "age" : "6" }', '$.name') as json_name,
  JSON_EXTRACT_SCALAR('{ "name" : "Jakob", "age" : "6" }', '$.name') as scalar_name,
  JSON_EXTRACT('{ "name" : "Jakob", "age" : "6" }', '$.age') as json_age,
  JSON_EXTRACT_SCALAR('{ "name" : "Jakob", "age" : "6" }', '$.age') as scalar;
```

```bash
+-----------+-------------+----------+--------+
| json_name | scalar_name | json_age | scalar |
+-----------+-------------+----------+--------+
| "Jakob"   | Jakob       | "6"      | 6      |
+-----------+-------------+----------+--------+
```

## JSON_EXTRACT_ARRAY
추출 방법

```sql
JSON_EXTRACT_ARRAY(json_string_expr[, json_path_format])
```

JSON 형식의 문자열에서 배열을 추출합니다.
- return : ARRAY<STRING>

```sql
SELECT JSON_EXTRACT_ARRAY('[1,2,3]') as string_array

+----------------+
| string_array   |
+----------------+
| ['1','2','3']  |
+----------------+
```


```sql
-- Don't strip the double quotes
SELECT JSON_EXTRACT_ARRAY('["apples","oranges","grapes"]', '$') as string_array

+--------------------------------------+
| string_array                         |
+--------------------------------------+
| ['"apples"','"oranges"','"grapes"']  |
+--------------------------------------+

-- Strip the double quotes
SELECT ARRAY(
  SELECT JSON_EXTRACT_SCALAR(string_element, '$')
  FROM UNNEST(JSON_EXTRACT_ARRAY('["apples","oranges","grapes"]','$')) AS string_element
) AS string_array

+---------------------------------+
|  string_array                   |
+---------------------------------+
| ['apples', 'oranges', 'grapes'] |
+---------------------------------+
```


Fruit의 항목만 배열로 추
```sql
SELECT JSON_EXTRACT_ARRAY(
  '{"fruit":[{"apples":5,"oranges":10},{"apples":2,"oranges":4}],"vegetables":[{"lettuce":7,"kale": 8}}',
  '$.fruit'
) as string_array

+----------------------------------------------------------------------+
| string_array                                                         |
+----------------------------------------------------------------------+
| ['{"apples" : 5, "oranges" : 10}' , '{"apples" : 2, "oranges" : 4}'] |
+----------------------------------------------------------------------+
```

## JSON_QUERY 또는 JSON_VALUE
JSON_QUERY(json_string_expr, json_path_format)는 JSON 값을 STRING으로 반환합니다.

JSON_VALUE(json_string_expr, json_path_format)는 스칼라 JSON 값을 STRING으로 반환합니다.

```sql
SELECT JSON_QUERY(json_text, '$') AS json_text_string
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;

+-----------------------------------------------------------+
| json_text_string                                          |
+-----------------------------------------------------------+
| {"class":{"students":[{"name":"Jane"}]}}                  |
| {"class":{"students":[]}}                                 |
| {"class":{"students":[{"name":"John"},{"name":"Jamie"}]}} |
+-----------------------------------------------------------+
```


```sql
SELECT JSON_QUERY(json_text, '$.class.students[0]') AS first_student
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;

+-----------------+
| first_student   |
+-----------------+
| {"name":"Jane"} |
| NULL            |
| {"name":"John"} |
+-----------------+
```


```sql
SELECT JSON_QUERY(json_text, '$.class.students[1].name') AS second_student_name
FROM UNNEST([
  '{"class" : {"students" : [{"name" : "Jane"}]}}',
  '{"class" : {"students" : []}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name" : null}]}}',
  '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'
  ]) AS json_text;

+-------------------+
| second_student    |
+-------------------+
| NULL              |
| NULL              |
| NULL              |
| "Jamie"           |
+-------------------+
```