Metabase
----


# Install

## 설치 환경과 준비 사항
설치 환경
- OS : macOS High sierra
- Docker
- browser : Chrome

기본적으로 Docker 설치가 완료가 되어 있어야 한다.
- docker 설치 : https://www.docker.com/ 
 

## 설치 과정

## 1. docker run 
아래 docker run 명령어를 이용하여 설치를 진행한다.

```bash
# 최신 버전 설치

docker run -d -p 3000:3000 --name metabase metabase/metabase
```

version 별로 설치를 진행하고 싶다면 옵션을 준다. 

```bash
# v0.38.0 버전 설치
# --name 은 임의로 변경하였다.

docker run -d -p 3000:3000 --name metabase_v0.38.0 metabase/metabase:v0.38.0
```

접속 Port를 변경하고 싶다면 아래 옵션을 준다.

```bash
docker run -d -p 12345:3000 --name metabase metabase/metabase
```


## 2. 설치 확인
위의 명령어 실행 후 docker ps 명령어를 이용하여 container가 실행되는지 확인한다. 

```bash
docker ps
```

## 3. 접속
container 가 정상적으로 실행되고 있음을 확인했다면 사용하고 있는 브라우저에서 localhost:3000으로 접속한다.

```bash
http://localhost:3000/
```

## 4. 실행
위 링크로 접속을 하게 되면 메타베이스가 initialize 되면서 접속 계정 설정을 하게 된다. 

# Update

Metabase 버전을 변경하면서 db 파일을 백업을 해야 하는 경우가 있다.
- 기존의 정보를 보존해둬야 버전 변경 후 새롭게 설정하는 일을 막을 수 있다.

db 파일은 메타베이스 환경 내에서 관리 되고 있다.

```bash
# metabase.db 관리(예시)

~/metabase-data/metabase.db
```

기존 버전에서 관리하고 있는 db 파일을 다른 곳으로 옮긴다. docker 환경에서 local 환경으로 이동시켰다.

```bash
docker cp container_id:/metabase.db/ "local_path"
```

새로운 버전을 설치 한다. 설치 방법은 위와 같다.

그 후 local 환경에 백업한 db 파일을 새로운 버전에 넣어준다.

```bash
docker cp -a local_path/metabase.db/. new_docker_container_id:metabase.db/
```

접속 후 정상적으로 db 파일이 올라갔는지 확인한다. metabase에 접속하면 된다.