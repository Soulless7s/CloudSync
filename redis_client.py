import redis
import json

class RedisClient:
    def __init__(self, host, port, password=None):
        self.r = redis.Redis(host=host, port=port, password=password, decode_responses=True)

    def cache_log(self, log_data):
        """
        使用 Redis 的 Sorted Set 保存日志记录，以 timestamp 作为分数(score)
        key 固定为 "logs"，value 为 JSON 格式的日志数据。
        """
        key = "logs"
        score = log_data.get("timestamp")
        value = json.dumps(log_data)
        self.r.zadd(key, {value: score})

    def query_logs(self, min_timestamp, max_timestamp):
        """
        按照时间范围查询日志记录，返回 JSON 格式列表
        """
        key = "logs"
        results = self.r.zrangebyscore(key, min_timestamp, max_timestamp)
        return [json.loads(item) for item in results]
