from functools import wraps
import json
import hashlib
import redis
from typing import Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings

class Cache:
    """
    缓存管理类
    支持Redis缓存
    """
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.default_timeout = 300  # 默认缓存时间5分钟

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """
        生成缓存键
        """
        # 将参数转换为字符串并排序，确保相同参数生成相同的键
        key_parts = [
            func_name,
            str(sorted(str(args).items()) if isinstance(args, dict) else args),
            str(sorted(kwargs.items()))
        ]
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """
        设置缓存值
        """
        try:
            timeout = timeout or self.default_timeout
            return self.redis_client.setex(
                key,
                timeout,
                json.dumps(value)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        删除缓存
        """
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    def clear_all(self) -> bool:
        """
        清除所有缓存
        """
        try:
            return self.redis_client.flushall()
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False

cache = Cache()

def cache_result(timeout: Optional[int] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 直接调用原函数，不进行缓存
            return await func(*args, **kwargs)
        return wrapper
    return decorator
