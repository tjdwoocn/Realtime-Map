# Building Realtime Maps (3)

## Create First Kafka Producer in Python with Pykafka library
- 아래의 그림과 같은 구조를 형성할것임
![screenshot](./RM_img/screenshot46.png)

---

## Start both Zookeeper and Kafka
- 일단 저번에 했던것과 동일하게 zookeeper와 kafka를 실행시켜야함
### Zookeeper 실행
- 설정완료 후 kafka/bin/windows/ 에 있는 'zookeeper-server-start.bat' 파일 실행하기
  - 프롬프트 창을 열어 경로를 windows 폴더로 이동   
  - 아래 명령어 입력
  ```linux
  zookeeper-server-start.bat ../../config/zookeeper.properties
  ```
---
### Kafka 실행
- kafka/bin/windows 경로의 'kafka-server-start.bat' 파일을 실행할 것임
- zookeeper가 실행중인 프롬프트 말고 새로운 프롬프트를 실행시킴
-  아래 커맨드 입력   
    ```linux
    kafka-server-start.bat ../../config/server.properties
    ```
    ![screenshot](./RM_img/screenshot47.png)   
    - 둘 다 실행완료

---
## 새로운 토픽 생성하기

- 아래 명령어 입력   
    ```linux
    kafka-topics.bat --zookeeper localhost:2181 --topic testBusdata --create --partitions 1 --replication-factor 1
    ---
- localhost:2181 port에 접속하고, 'testBusdata' 라는 topic을 생성   
![screenshot](./RM_img/screenshot48.png)

---

## Pykafka library 설치 및 기본구조 설정하기
    -   Python 과 Kafka를 같이 쓰기위한 패키지인 Pykafka를 설치하고 사용 할 것임

### busdata.py 파일 생성
- 일단 busdata.py 라는 이름의 파이썬 파일을 하나 만들어 둠
- 현재 사용중인 **Visual Studio Code**로 해당 폴더에 생성   
![screenshot](./RM_img/screenshot49.png)

### Pykafka library 검색 및 설치
- 구글에 pykafka 검색 또는 해당 링크 접속   
https://pykafka.readthedocs.io/en/latest/   
![screenshot](./RM_img/screenshot50.png)

- 새 프롬프트창에서 'pip install pykafka' 를 입력하여 설치      
![screenshot](./RM_img/screenshot51.png)
- 설치 완료

### Importing Kafka client form Pykafka
- 만들어둔 busdata.py 파일에 아래 코드들 작성   
    ```python
    from pykafka import KafkaClient
    client = KafkaClient(hosts="localhost:9092")
    ```   
    ![screenshot](./RM_img/screenshot52.png)
- KafkaClient 를 임포트하고 호출
- Kafka broker가 실행중인 나의 clients 설정 (localhost)
- localhost에 최소 하나 이상의 kafka instance가 작동하고 있어야 함

### localhost 내의 topic 확인
- 아래 코드 입력하여 결과 확인
    ```python
    from pykafka import KafkaClient
    client = KafkaClient(hosts="localhost:9092")

    print(client)
    print(client.topics)
    ```
    ![screenshot](./RM_img/screenshot53.png)
    - localhost에 있는 모든 topic 확인가능
  
- 아래 코드 추가
  ```python
  print(client.topics['testBusdata'])
  ```
    ![screenshot](./RM_img/screenshot54.png)

    - testBusdata topic에 접근

---

## Producer 생성, 메세지 보내기 + Consumer 확인
- 파이썬으로 producer 생성, 메세지 보내기를 한 뒤 consumer에서 받은 메세지 확인할 것임   
  ```python
  # producer 생성
  producer = topic.get_sync_produer()
  # message 보내기
  producer.produce('test message')
  ```   
- 아래 명령어로 topic이 'testBusdata;인 consumer에 접속후 메세지 확인
    ```linux
    kafka-console-consumer --bootstrap-server localhost:9092 --topic testBusdata --from-beginning
    ```
- Consumer 실행 뒤 'busdata.py'를 실행 시키면!! .... 아래와 같은 에러메세지가 나옵니다   
    ![screenshot](./RM_img/screenshot55.png)
    - Producer.produce 는 bytes object를 메세지로서 받는데 우리가 보낸것은 str 클래스의 문자라서 그런것임!   
  ---> encoding 필요, 아래와 같이 수정
    ```python
    producer.produce('test message'.encode('utf8')) # utf8 말고 ascii 등 다른것도 사용가능
    ```
    ![screenshot](./RM_img/screenshot56.png)
    - 메세지 전송 및 수신 완료!
    - 코드   
    ![screenshot](./RM_img/screenshot57.png)

### [번외] while을 사용하여 메세지 무한히 생성
- 아래 코드를 넣고 실행시켜서 producer가 계속 메세지 보내고 consumer가 계속 메세지 받는 모습 확인해보기
```python
# message 생성
count = 1
while true:
    message = ('hello-' + str(count)).encode('utf8')
    producer.produce(message)
    print(message)
    count += 1
```   
![screenshot](./RM_img/screenshot58.png)
- 10초도 안되는 사이에 2000이 넘는 메세지가 생성/전송/확인 됨
---


