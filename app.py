from flask import Flask, render_template, Response
from pykafka import KafkaClient

# local kafka broker 불러오기
def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

# 앱 생성
app = Flask(__name__)

# 메인 라우트 생성
@app.route('/')
def index():
    # 랜덤 텍스트 리턴
    return(render_template('index.html'))

# Consumer API (컨슈머 불러오는 별도의 라우트)
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()
    # consume messages from topics = Consumer
    def events():
        # kafka broker에서 topicname으로 접근
        # Topic에 계속 접근하여 message 받아옴
        for i in client.topics[topicname].get_simple_consumer():
            # generator(yield)를 사용하여 메세지가 새로 들어올 때 마다 출력하도록
            # 메세지는 바이트로 들어오기 때문에 decode 필요
            yield 'data:{0}\n\n'.format(i.value.decode())
    # events 함수를 Response로 호출
    # event-stream 으로 결과를 받고 브라우저에 계속 리턴해줌 
    return Response(events(), mimetype='text/event-stream')
# 앱 실행시키기
if __name__ == '__main__':
    # debug=True 라고 해놓으면 후에 리턴하는 텍스트 값을 수정시 바로 적용이 됨
    app.run(debug=True, port= 5001)

