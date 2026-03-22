import redis
from INewApp.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=6379,
    db=0,
    decode_responses=True
)