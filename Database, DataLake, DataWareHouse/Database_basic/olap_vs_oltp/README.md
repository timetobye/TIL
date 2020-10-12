OLTP vs OLAP
----

## 문서 목적
OLTP vs OLAP 내용을 정리하기 위한 문서이다.

## OLAP
Online Analytical Processing
- a category of software tools which provide analysis of data for business decisions. 
- OLAP systems allow users to analyze database information from multiple database systems at one time.
- 최종 사용자가 다차원 정보에 직접 접근하여 대화식으로 정보를 분석하고 의사결정에 활용하는 과정
- **The primary objective is data analysis and not data processing.**

### Example of OLAP
Any Datawarehouse system is an OLAP system
- A company might compare their mobile phone sales in September with sales in October, then compare those results with the with another location which may be stored in a sperate database.
- Amazon analyzes purchases by its customers to come up with a personalized homepage with products which likely interest to their customer.

### Pros and Cons
Pros
- OLAP creates a single platform for all type of business analytical needs which includes planning, budgeting, forecasting, and analysis.
- The main benefit of OLAP is the consistency of information and calculations.
- Easily apply security restrictions on users and objects to comply with
regulations and protect sensitive data.

Cons
- Implementation and maintenance are dependent on IT professional because the traditional OLAP tools require a complicated modeling procedure.
- OLAP tools need cooperation between people of various departments to be effective which might always be not possible.

## OLTP
Online transaction processing
- supports transaction- oriented applications in a 3-tier architecture
- OLTP administers day to day transaction of an organization.
- 빈번한 거래 데이터의 입력, 수정, 삭제 과정에서의 효율성, 즉 효과적인 갱신이 주요 목표
- **The primary objective is data processing and not data analysis**

### Example of OLTP
An example of OLTP system is ATM center
- Assume that a couple has a joint account with a bank. 
One day both simultaneously reach different ATM centers at precisely the same time 
and want to withdraw total amount present in their bank account.
- However, the person that completes authentication process first will be able to get money. 
In this case, OLTP system makes sure that withdrawn amount will be never more than the amount present in the bank. 
The key to note here is that OLTP systems are optimized for transactional superiority instead data analysis.

Case
- Online banking
- Online airline ticket booking
- Sending a text message
- Order entry
- Add a book to shopping cart

### Pros and Cons
Pros
- It administers daily transactions of an organization.
- OLTP widens the customer base of an organization by simplifying individual processes.

Cons
- If OLTP system faces hardware failures, then online transactions get severely affected.
- OLTP systems allow multiple users to access and change the same data at the same time which many times created unprecedented situation.


## 자료 출처
- https://12bme.tistory.com/144
- https://effectivesquid.tistory.com/entry/OLTP%EC%99%80-OLAP