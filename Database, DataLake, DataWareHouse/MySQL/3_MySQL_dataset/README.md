Docker MySQL 에 csv file load 하기
---

Docker 로 설치한 MySQL 에 csv file 을 load 하는 방법

## 1. 준비 사항
- Docker
- Docker 에 설치한 MySQL
- load 할 csv file
- csv file 은 https://www.kaggle.com/carrie1/ecommerce-data 에서 다운로드 후 인코딩 문제 해결 및 사이즈를 줄여서 사용
- csv file 의 첫 row 는 제거하고 진행

## 2. csv file 을 Docker MySQL 컨테이너로 옮기기
csv file 을 Docker MySQL 로 옮기는 명령어를 이용해 csv file을 Docker container 로 옮기기

**실행 예시**

```bash
docker cp {current file path}/{file_name} {container_id}:/{Docker MySQL dicretory name}/{file_name}
```

```bash
[-iMac]:{current_path}$ docker cp e_commerce_data_from_kaggle.csv f48abbdf3b99:/e_commerce_data_from_kaggle.csv
```

**결과 예시**

```bash
# ls
bin   dev			  e_commerce_data_from_kaggle.csv  etc	 lib	media  opt   root  sbin  sys  usr
boot  docker-entrypoint-initdb.d  entrypoint.sh			   home  lib64	mnt    proc  run   srv	 tmp  var
```

## 3. Database, table schema 생성
우선, Database 를 생성한다.

```bash
mysql> create database commerce;
Query OK, 1 row affected (0.01 sec)
```

csv file 을 다운로드한 링크를 참고하여 table schema 를 작성한다.

```bash
mysql> create table commerce (
    ->   InvoiceNo int not null,
    ->   StockCode varchar(20) not null,
    ->   Description varchar(45) not null,
    ->   Quantity int not null,
    ->   InvoiceDate varchar(20) not null,
    ->   UnitPrice int not null,
    ->   CustomerID int not null,
    ->   Country varchar(20) not null
    -> );
Query OK, 0 rows affected (0.03 sec)
```

## 4. Load csv file
이제 Docker MySQL 로 csv file 을 load 한다.

```bash
mysql> LOAD DATA LOCAL INFILE '/e_commerce_data_from_kaggle.csv' INTO TABLE commerce FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
ERROR 3948 (42000): Loading local data is disabled; this must be enabled on both the client and server sides
```

에러가 발생했는데 해당 에러는 아래와 같이 대응할 수 있다.

```bash
mysql> SET GLOBAL local_infile=1;
Query OK, 0 rows affected (0.00 sec)

mysql> quit
Bye
```
그 다음으로 아래 명령어를 통해 다시 MySQL로 접속을 한다.

```bash
[-iMac]:{current_path}$ docker exec -it mysql_name mysql -u root -p --local-infile=1
```

database 를 선택 후 다시 명령어를 입력한다.

```bash
mysql> use commerce;
Database changed

mysql> LOAD DATA LOCAL INFILE '/e_commerce_data_from_kaggle.csv' INTO TABLE commerce FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
Query OK, 5 rows affected (0.00 sec)
Records: 5  Deleted: 0  Skipped: 0  Warnings: 0

mysql> select * from commerce;
+-----------+-----------+-------------------------------------+----------+----------------+-----------+------------+----------------+
| InvoiceNo | StockCode | Description                         | Quantity | InvoiceDate    | UnitPrice | CustomerID | Country        |
+-----------+-----------+-------------------------------------+----------+----------------+-----------+------------+----------------+
|    536365 | 85123A    | WHITE HANGING HEART T-LIGHT HOLDER  |        6 | 12/1/2010 8:26 |         3 |      17850 | United Kingdom |
|    536365 | 71053     | WHITE METAL LANTERN                 |        6 | 12/1/2010 8:26 |         3 |      17850 | United Kingdom |
|    536365 | 84406B    | CREAM CUPID HEARTS COAT HANGER      |        8 | 12/1/2010 8:26 |         3 |      17850 | United Kingdom |
|    536365 | 84029G    | KNITTED UNION FLAG HOT WATER BOTTLE |        6 | 12/1/2010 8:26 |         3 |      17850 | United Kingdom |
|    536365 | 84029E    | RED WOOLLY HOTTIE WHITE HEART.      |        6 | 12/1/2010 8:26 |         3 |      17850 | United Kingdom |
+-----------+-----------+-------------------------------------+----------+----------------+-----------+------------+----------------+
5 rows in set (0.01 sec)
```

## 참고 문서
- [How to load csv files into MySQL tables (for Docker users)](https://gist.github.com/jypthemiracle/31a2979d2daca7bbf6625b75a3e5ad30)
- [ERROR: Loading local data is disabled - this must be enabled on both the client and server sides](https://stackoverflow.com/questions/59993844/error-loading-local-data-is-disabled-this-must-be-enabled-on-both-the-client)