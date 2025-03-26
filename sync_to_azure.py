import json
import time
from redis_client import RedisClient
from azure.storage.blob import BlobServiceClient

# 配置 Azure Blob Storage（请替换为实际连接字符串和容器名称）
AZURE_CONNECTION_STRING = "your_connection_string"
CONTAINER_NAME = "logs-container"

redis_client = RedisClient(host="localhost", port=6379, password="redis_password")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def sync_logs_to_azure():
    # 从 Redis 查询所有日志（可根据需求调整时间范围）
    logs = redis_client.query_logs(0, int(time.time()))
    log_data = json.dumps(logs, indent=2)
    # 生成一个唯一的 blob 名称，例如使用当前时间戳
    blob_name = f"logs_{int(time.time())}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(log_data)
    print(f"Synced {len(logs)} logs to Azure Blob Storage as {blob_name}")

if __name__ == '__main__':
    # 示例：每次运行时同步一次
    sync_logs_to_azure()
