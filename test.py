from datetime import datetime, timedelta, UTC

from dateutil.relativedelta import relativedelta

 

now = datetime.now(UTC)
date1 = now - timedelta(days=20)
print(now)

# print(now + timedelta(days=30))
print(now + relativedelta(months=1))
print(date1)
print(date1 + relativedelta(months=1))