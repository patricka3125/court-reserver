import datetime
import datetime as dt
import multiprocessing as mp
import os
import time

import requests
from scheduler import Scheduler

user_id = os.environ["USER_ID"]
cookie = os.environ["COOKIE"]
target_datetime = datetime.datetime.now() + datetime.timedelta(days=9)
target_datetime = target_datetime.replace(hour=20, minute=0, second=0, microsecond=0)


def send_reserve_request():
    url = "https://lt.clubautomation.com/event/reserve-court-new-do?ajax=true"
    payload = ("user_id={0}&component=42&club=4&court=-1&host={0}&date={1}%2F{2}%2F{3}&interval=120&"
               "time-reserve={4}&location-reserve=27&is_confirmed=1"
               .format(user_id, target_datetime.month, target_datetime.day,
                       target_datetime.year, int(target_datetime.timestamp())))
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Origin': 'https://lt.clubautomation.com',
        'Referer': 'https://lt.clubautomation.com/event/reserve-court-new',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if "Reservation Completed" in response.text:
        print("reservation complete")
    elif "you don't have permission to reserve" in response.text:
        print("invalid cookie")
    elif "not allowed to reserve Court so far ahead" in response.text:
        print("failed: too early")
    elif ("Unable to find any available Court" in response.text or
          "reservation at this time is no longer available" in response.text):
        print("failed: no available courts")
    else:
        print(response.text)


def loop_reserve(x):
    for i in range(x):
        send_reserve_request()


def start_pool():
    print("start pool at ", dt.datetime.now())
    pool = mp.Pool(mp.cpu_count())
    pool.map(loop_reserve, range(0, 100))

def main():
    schedule = Scheduler()
    schedule.once(dt.datetime.now().replace(hour=23, minute=59, second=45), start_pool)
    while True:
        schedule.exec_jobs()
        print(schedule)
        time.sleep(1)
        os.system("clear")


if __name__ == "__main__":
    main()
