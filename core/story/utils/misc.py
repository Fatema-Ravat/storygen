from .redis_client import redis_client 
from datetime import datetime, timedelta


def can_user_generate(user_id,daily_limit):
    #key format for redis : daily_usage:{user_id}:{YYYYMMDD}
    today = datetime.now().strftime("%Y%m%d")
    redis_key = f"daily_usage:{user_id}:{today}"

    usage = redis_client.get(redis_key)
    usage = int(usage) if usage else 0

    if usage>=daily_limit:
        return False #limit reached

    # increament usage
    pipeline = redis_client.pipeline()
    pipeline.incr(redis_key)
    pipeline.expireat(redis_key,datetime.utcnow().replace(hour=23,minute=59,second=59))
    pipeline.execute()

    return True