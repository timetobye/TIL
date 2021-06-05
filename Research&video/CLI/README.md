커맨드 라인 사용법
----

커맨드 라인 사용법을 정리한 문서

```bash

```

### pwd
현재 디렉토리를 알려주는 명령어

```bash
$ pwd
/Users/user_name
```

### cd
디렉토리 이동을 할 때 사용하는 명령어

```bash
$ cd /
상위 디렉토리로 이동

$ cd directory path or directory name
directory 로 이동
```

### 현재 디렉토리 표현
현재 디렉토리 -> 현재 디렉토리 이동

```bash
$ pwd
/Users/user_name
$ cd .
$ pwd
/Users/user_name
$ 
```

정확한 위치로 이동하고자 한다면 상대 경로 보다는 절대 경로를 이용하는 것이 편리

### 상위 디렉토리, 홈 디렉터리, 임시 디렉터리 /tmp
```bash
.. 은 상위 디렉터리를 의미

$ pwd
/Users/user_name/Documents
$ cd ..
$ pwd
/Users/user_name
$ 

.. 을 여러번 사용하는 것도 가능
../.. 과 같이 표현

$ pwd
/Users/user_name/Documents
$ cd ../..
$ pwd
/Users
```

아래의 예시처럼 논리적으로 확장도 가능

```bash
$ pwd
/Users/44bits
$ cd ../44bits/../../Users/../Users/44bits
$ pwd
/Users/44bits
```

현재 사용자 확인
```bash
whoami
```

현재 프로세스를 실행한 사용자의 홈 디렉토리로 이동
```bash
cd ~
```

홈 디렉토리로 바로 이동
```bash
cd
```

### ls - 디렉토리 정보 파악

```bash
# 기본 옵션
ls

# 타입에 따라 다르게 출력 옵션
# 흰색 : 파일, 파란색 출력 : 디렉토리
ls -G

# 디렉토리만 출력
ls -d */

# 자세한 정보까지 출력
# 파일의 권한, 소유자, 그룹, 파일 크기, 수정일
ls -l -G

# -t : 가장 최근에 수정된 파일
# -s : 사이즈가 큰 파일부터 출력
# -r : 순서를 거꾸로 출력

ls -l -S -G -r

# . 으로 시작하는 파일 출력
ls -a
```

### 파일과 디렉토리 조작 명령어

```bash
# 디렉토리 생성
mkdir

# 한꺼번에 디렉토리 만들기(지정된 경로의 상위에 디렉토리가 없어도 가능)
mkdir -p parent_directory_name/chiledren_directory_name
```


```bash
# 현재 디렉토리 내용 확인
ls -R

# 파일 생성
touch file_name_1

# 한번에 여러 파일 생성
touch file_name_2 file_name_3 file_name_4 file_name_5

# mv - 파일 이름 이동, cp - 파일 복사
# <SRC> : 복사/이동하고자 하는 파일의 경로
# <DEST> : 새로운 경로

cp <SRC> <DEST>
mv <SRC> <DEST>

$ touch a
$ ls
a	hello

$ ls -G
a     hello

$ touch b c d e
$ ls
a	b	c	d	e	hello

$ mv a airport
$ ls
airport	b	c	d	e	hello

$ cp b batman
$ ls
airport	b	batman	c	d	e	hello

# airport file -> hello directory
$ mv airport hello/

# 원래대로 돌리는 방법 : 절대경로를 쓰거나 ../ 를 이용

$ mv airport ../
$ cd ..
$ ls
airport b   batman  c   d   e   hello
```

```bash
# 파일 삭제 명령어
$ rm c d

# 디렉토리 삭제 명령어
$ rm -rf
```

### 문자열 출력, 파일과 관련된 셀 기본 명령어

echo 명령어는 인자를 받아서 출력해준다.

```bash
$ echo hello, world!
hello, world!
```
echo 는 셀 스크립트에서 사용하거나, 환경변수 출력에 사용

파일 내용을 출력하는 명령어 - cat, head, tail
- cat 은 항상 파일의 전체 내용을 출력
- head 는 파일의 앞부분을 출력
- tail 은 파일의 끝부분을 출력
- -n 옵션을 주면 출력할 line 의 수를 지정할 수 있음

```bash
$ head -n2 bashrc 또는 $ head -n 2 bashrc 
# System-wide .bashrc file for interactive bash(1) shells.
if [ -z "$PS1" ]; then
  
$ tail -n 2 bashrc
```

tail 은 -f 옵션과도 자주 사용
- 서버 프로세스의 로그 파일의 경우 로그 파일을 계속 업데이트 함
- 이 때 ```tail -f file``` 을 같이 실행하면 tail 프로그램이 종료되지 않고 업데이트 되는 내용을 바로 출력

### 헬프 옵션 : -h, -help // man으로 메뉴얼 보기

옵션 사용 방법
- 아무런 인자없이 명령어를 실행한다.
- -h 옵션을 붙여서 실행한다.
- --help 옵션을 붙여서 실행한다

-h 옵션이 없는 경우도 존재한다.
```bash
$ tail -h
tail: illegal option -- h
usage: tail [-F | -f | -r] [-q] [-b # | -c # | -n #] [file ...]
```

```bash
$ man grep
# 명령어를 입력하면 메뉴얼이 나오고 사용방법도 나온다.

$ grep shell /etc/bashrc
# System-wide .bashrc file for interactive bash(1) shells.
```

**'-' 를 사용할 경우 여러개의 옵션을 한 번에 사용할 수 있음**


### 리눅스 시그널

stty -e 명령어를 사용하면 터미널에서 입력할 수 있는 특수문자 확인이 가능

```bash
$ stty -e
speed 9600 baud; 48 rows; 84 columns;
lflags: icanon isig iexten echo echoe -echok echoke -echonl echoctl
	-echoprt -altwerase -noflsh -tostop -flusho pendin -nokerninfo
	-extproc
iflags: -istrip icrnl -inlcr -igncr ixon -ixoff ixany imaxbel iutf8
	-ignbrk brkint -inpck -ignpar -parmrk
oflags: opost onlcr -oxtabs -onocr -onlret
cflags: cread cs8 -parenb -parodd hupcl -clocal -cstopb -crtscts -dsrflow
	-dtrflow -mdmbuf
discard dsusp   eof     eol     eol2    erase   intr    kill    lnext   
^O      ^Y      ^D      <undef> <undef> ^?      ^C      ^U      ^V      
min     quit    reprint start   status  stop    susp    time    werase  
1       ^\      ^R      ^Q      ^T      ^S      ^Z      0       ^W     
```

```bash
$ sleep 10000
^Z
[1]+  Stopped                 sleep 10000

$ bg
[1]+ sleep 10000 &

# 프로세스 ID 확인
$ jobs -l
[1]+ 71168 Running                 sleep 10000 &

$ kill 71165
-bash: kill: (71165) - No such process # 오타남..

$ kill 71168
[1]+  Terminated: 15          sleep 10000
$ jobs

```

```kill -9 <PID> ``` 를 이용하면 프로세스 강제 종료 가능

### 라인 앞 뒤로 이동 - option + 화살표

문자 그대로 option + 화살표로 이동 가능

### 명령어 히스토리 찾기 - history + ^r
````bash
# 이전 명령어 기록을 숫자만큼 출력
history + 숫자

# 명령어 실행을 복사하지 않고 바로 할 수 있음
!숫자

# history + ^r 을 쓸 경우 기록이 역순으로 출력됨 + 검색
# fzf 를 쓰고 있음
```


