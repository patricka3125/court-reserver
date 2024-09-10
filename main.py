import datetime
import datetime as dt
import multiprocessing as mp
import os
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from scheduler import Scheduler

usernames = os.environ["USERS"].split(',')
passwords = os.environ["PASSWORDS"].split(',')
target_dt = datetime.datetime.now() + datetime.timedelta(days=8)
weekday_to_time_map = {
    0: (19, 40),  # Monday
    1: (19, 40),  # Tuesday
    2: (19, 40),  # Wednesday
    3: (19, 40),  # Thursday
    4: (17, 10),  # Friday
    5: (19, 40),  # Saturday
    6: (17, 40),  # Sunday
}
target_dt = target_dt.replace(
    hour=weekday_to_time_map[target_dt.weekday()][0],
    minute=weekday_to_time_map[target_dt.weekday()][1],
    second=0,
    microsecond=0
)
# start_dt = dt.datetime.now().replace(hour=11, minute=59, second=50, microsecond=0)
start_dt = dt.datetime.now()


def get_user_id(session: requests.Session) -> Optional[int]:
    url = "https://lt.clubautomation.com/user/get-member-info"

    response = session.get(url, verify=False)
    response.raise_for_status()

    return response.json()["info"]["id"]


def get_login_token() -> (Optional[str], requests.Session):
    url = "https://lt.clubautomation.com/"
    s = requests.Session()
    response = s.get(url, verify=False)
    response.raise_for_status()

    parsed_html = BeautifulSoup(response.text, features="html.parser")

    return parsed_html.body.find('input', attrs={'id': 'login_token'}).attrs['value'], s


def login(session: requests.Session, login_token: str, username: str, password: str) -> None:
    url = "https://lt.clubautomation.com/login/login"
    payload = "email={0}&password={1}&login_token={2}".format(username, password, login_token)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = session.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    try:
        js = response.json()
        if "isValid" not in js or js["isValid"] == False:
            print("login failed, not valid response")
            exit(1)
    except requests.exceptions.JSONDecodeError:
        print("login failed, body isn't json")
        exit(1)


def send_reserve_request(session: requests.Session, user_id: int) -> bool:
    url = "https://lt.clubautomation.com/event/reserve-court-new-do?ajax=true"
    payload = ("user_id={0}&component=42&club=4&court=-1&host={0}&date={1}%2F{2}%2F{3}&interval=120&"
               "time-reserve={4}&location-reserve=27&is_confirmed=1"
               .format(user_id, target_dt.month, target_dt.day,
                       target_dt.year, int(target_dt.timestamp())))
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    response = session.post(url, headers=headers, data=payload, verify=False)

    if "Reservation Completed" in response.text:
        print("reservation complete, " + response.text)
        return True
    elif "you don't have permission to reserve" in response.text:
        print("invalid cookie")
    elif "not allowed to reserve Court so far ahead" in response.text:
        print("failed: too early")
    elif ("Unable to find any available Court" in response.text or
          "reservation at this time is no longer available" in response.text):
        print("failed: no available courts")
    elif "already has 1 primary reservation" in response.text:
        print("failed: already reserved")
        return True
    else:
        print(response.text)

    return False


def loop_reserve(session: requests.Session, user_id: int) -> None:
    for i in range(100):
        # stop once the reservation is complete or the account already has a court booked for that day
        if send_reserve_request(session, user_id):
            break


def start_pool(data=None) -> None:
    pool = mp.Pool(mp.cpu_count())
    pool.starmap(loop_reserve, data)


def main():
    data: list[tuple[requests.Session, int]] = []  # list of tuples of session and user_ids like [(session1, 123456), (session2, 654321), ...]
    if len(usernames) != len(passwords):
        print("length of usernames and passwords don't match")
        exit(1)

    # login sessions and get user_ids
    for i in range(len(usernames)):
        login_token, session = get_login_token()
        if login_token is None or login_token == "":
            print("failed to get login_token")
            exit(1)

        login(session, login_token, usernames[i], passwords[i])
        user_id = get_user_id(session)
        if not user_id:
            print("failed to get user_id")
            exit(1)

        data.append((session, user_id))

    if not data or len(data) == 0:
        print("no data")
        exit(1)

    schedule = Scheduler()
    schedule.once(start_dt, start_pool, kwargs={"data": data})
    while True:
        schedule.exec_jobs()
        print(schedule)
        time.sleep(1)
        os.system("clear")


if __name__ == "__main__":
    main()
