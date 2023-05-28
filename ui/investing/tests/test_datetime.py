import datetime

# print(datetime.timedelta.)
print(datetime.datetime.now())

today = datetime.date.today()

thirty_day_ago = today - datetime.timedelta(days=30)

print(f'today: {today}')
print(f'thirty_day_ago: {thirty_day_ago}')

print(f'startdate: {today.month}/{today.day}/{today.year}')