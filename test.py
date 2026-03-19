from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# date_diff = datetime.strptime("2026-03-22", "%Y-%m-%d").date() - datetime.now(ZoneInfo("Asia/Kolkata")).date()
# if timedelta(days=0) < date_diff <= timedelta(days=3):
#     print("Date is within the next 3 days.")

# import uuid

# user_id = str(uuid.uuid4())
# print(user_id)

# t = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
# print(t)

t = datetime.strptime("2026-03-22", "%Y%m%d")
print(t)