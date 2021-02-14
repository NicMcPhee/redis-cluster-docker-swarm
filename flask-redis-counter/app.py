from flask import Flask
from redis import Redis
from redis.sentinel import Sentinel

app = Flask(__name__)

sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)
master = sentinel.master_for('redismaster', socket_timeout=0.1)
slave = sentinel.slave_for('redismaster', socket_timeout=0.1)

@app.route('/inc')
def inc_count():
    count = master.incr('hits')
    return 'After incrementing it, the counter value is {} as report by {} with ID {}.\n'.format(count, master.client_getname(), master.client_id())

@app.route('/')
def get_count():
    count = slave.get('hits')
    return 'The current counter value is {} as reported by {} with ID {}.\n'.format(count, slave.client_getname(), slave.client_id())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
