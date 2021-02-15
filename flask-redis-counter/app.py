import platform
from flask import Flask
from redis import Redis
from redis.sentinel import Sentinel

hostname = platform.node()

app = Flask(__name__)

sentinel = Sentinel([('redis-sentinel', 26379)], socket_timeout=0.1)
master = sentinel.master_for('redismaster', socket_timeout=0.1)
slave = sentinel.slave_for('redismaster', socket_timeout=0.1)

@app.route('/inc')
def inc_count():
    count = master.incr('hits')
    (master_ip, port) = sentinel.discover_master('redismaster')
    return 'After incrementing it, the counter value is {}.\nThe Redis IP is {}.\nThe Python host is {}.\n'.format(count, master_ip, hostname)

@app.route('/')
def get_count():
    count = slave.get('hits')
    return 'The current counter value is {}.\nThe Python host is {}.\n'.format(count, hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
