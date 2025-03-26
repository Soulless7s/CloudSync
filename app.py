from flask import Flask, request, jsonify
import time
import json
from db import MySQLDatabase
from redis_client import RedisClient

app = Flask(__name__)

# 配置项（请根据实际情况修改）
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "db_user",
    "password": "db_password",
    "database": "logs_db",
    "port": 3306
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "password": "redis_password"
}

# 初始化数据库连接模块和 Redis 模块
mysql_db = MySQLDatabase(**MYSQL_CONFIG)
redis_client = RedisClient(**REDIS_CONFIG)

@app.route('/upload_log', methods=['POST'])
def upload_log():
    """
    接受 POST 请求上传日志，要求 JSON 格式数据包含：
      - level: 日志级别（如 INFO、ERROR）
      - message: 日志内容
      - category: 日志类别
    系统自动使用当前 Unix 时间戳作为 timestamp。
    """
    data = request.get_json()
    required_fields = ["level", "message", "category"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # 使用当前时间戳（秒级）
    current_timestamp = int(time.time())
    log_entry = {
        "timestamp": current_timestamp,
        "level": data.get("level"),
        "message": data.get("message"),
        "category": data.get("category")
    }

    try:
        # 写入 MySQL
        mysql_db.insert_log(log_entry)
    except Exception as e:
        return jsonify({"error": f"MySQL insert error: {str(e)}"}), 500

    try:
        # 缓存到 Redis
        redis_client.cache_log(log_entry)
    except Exception as e:
        return jsonify({"error": f"Redis cache error: {str(e)}"}), 500

    return jsonify({"status": "Log received", "log": log_entry}), 200

@app.route('/query_logs', methods=['GET'])
def query_logs():
    """
    提供查询接口，支持通过 URL 参数传入 min 与 max 时间戳来查询 Redis 中的日志记录。
    示例：/query_logs?min=1680000000&max=1680003600
    """
    min_ts = request.args.get("min", default=0, type=int)
    max_ts = request.args.get("max", default=int(time.time()), type=int)
    logs = redis_client.query_logs(min_ts, max_ts)
    return jsonify({"logs": logs}), 200

if __name__ == '__main__':
    # 监听所有 IP，端口 5000，调试模式开启
    app.run(host='0.0.0.0', port=5000, debug=True)
