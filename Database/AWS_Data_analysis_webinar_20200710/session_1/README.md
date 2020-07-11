AWS 데이터 분석 특집 웨비나 - 데알못을 위한 데이터레이크(Data Lake) 구성 및 관리하기 
---

## 목차
- 데이터 분석의 현주소
- AWS 기반 데이터레이크 구축 방식
  - 데이터 레이크 정의 및 요구 사항
  - 데이터 레이크 기능 및 대응 서비스(Amazon S3, AWS Glue)
- AWS Lake Formation
  - 기존 데이터 레이크 작업 방법
  - Lake Formation 소개 및 구축 데모
  

## 1. 데이터 분석의 현주소
데이터가 폭증하고 있고, 새롭게 나타나는 데이터 분석 기술이 많아지고 이싿.
- 오픈 소스가 대세(Hadoop, ELS, Spark)
- 더 복잡해진 데이터 욕구 사항
  - 과거 단순한 로그 분석에서 벗어나서, 기업 내 다양한 욕구가 생기고 있음

데이터 사일로(silos)에서 데이터 레이크로 전환 필요
- 기존의 데이터 사일로로 구성된 것들을 하나의 저장소에 모아서 분석할 수 있도록 하는 방법론
- BI, ML 등으로 확장 가능

![alt text](images/7.jpg)

## 2. AWS 기반 데이터레이크 구축 방식

### 데이터 레이크 정의 및 요구 사항
데이터 레이크
- 정형 혹은 비정형 데이터에 상관 없이 어떤 규모에서도 저장 및 분석이 가능한 **단일저장소**
- 기업 내의 모든 데이터를 한 곳에!

![alt text](images/9.jpg)


![alt text](images/10.jpg)


AWS 서비스 데이터레이크 장점
- 손쉽고, 보안성 높고, 솔루션 많고, 확장성

### AWS 기반 데이터 분석 아키텍처
Data Sourcses
- RDB, DynamoDB(no-sql 계열)

kinesis
- 실시간 데이터 수집

저장 방식
- Amazon s3에 저장해서 Glue를 이용하여 전처리

Process & Analyze
- Athena는 S3에 저장된 데이터를 ad-hoc SQL 질의를 해서 조회 할 수 있는 서비스
- EMR은 하둡
- Redshift 는 warehouse
- ELS는 검색

사용 방법
- 노트북, 퀵사이트, 태블로 등등

![alt text](images/12.jpg)


### 데이터 레이크 기능 및 대응 서비스(Amazon S3, AWS Glue)

#### Amazon Simple Storage Service(S3)
S3에 있는 데이터를 뽑아내서 분석도 가능하고 다재다능

![alt text](images/13.jpg)

#### Amazon Glue - 서버리스 ETL(추출, 변환 및 로드) 서비스
Glue를 이용하여 S3에 저장된 데이터를 간편하고 유연하게 ETL 작업 가능
- 자동으로 데이터의 catalog를 생성 가능
- spark 제공

![alt text](images/14.jpg)

![alt text](images/15.jpg)

![alt text](images/16.jpg)

![alt text](images/18.jpg)


![alt text](images/20.jpg)


S3 데이터 관리 및 분석
- 기본적으로 select 질의가 가능하고, 써드 파티를 써도 됨
- Redshift, Ahtena, EMR, ElasticSearch, Quicksight, SageMaker

![alt text](images/21.jpg)


서버리스
- 서버를 구성하지 않아도 사용한만큼만 비용을 제공하는 것

![alt text](images/22.jpg)

## 3. AWS Lake Formation
대부분의 데이터 레이크 운영 시 데이터 준비에 많은 시간이 투입됨

![alt text](images/27.jpg)

### 기존 데이터 레이크 작업 방법

![alt text](images/28.jpg)

### AWS Lake Formation
기존의 데이터 레이크 작업을 손쉽게 해주는 것

![alt text](images/29.jpg)

![alt text](images/30.jpg)


AWS CloudTrail
- 계정 내에서 이루어지는 모든 작업에 대해 log를 남겨서 확인 가능한 기능

이후 부터는 실습 화면을 제공하였음

![alt text](images/31.jpg)

![alt text](images/34.jpg)

![alt text](images/35.jpg)

![alt text](images/36.jpg)

![alt text](images/37.jpg)

![alt text](images/38.jpg)

![alt text](images/39.jpg)







