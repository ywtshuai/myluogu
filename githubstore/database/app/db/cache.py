from functools import wraps
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL)


def cache_result(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
        result = redis_client.get(cache_key)

        if result is not None:
            return result

        result = await func(*args, **kwargs)
        redis_client.setex(cache_key, 300, result)  # 缓存5分钟
        return result

    return wrapper