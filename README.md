# court-reserver

Conditions for the script to work:
* Need a login session cookie granted by PHP. Two options:
  a. Manually login to an account on the browser before the session cookie expiration.
  b. Simulate browser behavior with login keystrokes
* Need a cloudflare token that is stored in cookie. It should be provided once account login is successful.

## Payload Information

A HTTP POST request will be sent out once the user selects a time to reserve the court. 

POST request header
General --

Request URL:
https://lt.clubautomation.com/event/reserve-court-new-do?ajax=true

Request Method:
```bash
POST
Status Code:
200 OK
Remote Address:
[2606:4700::6812:c10]:443
Referrer Policy:
strict-origin-when-cross-origin
```

Request Headers --
```bash
:authority:
lt.clubautomation.com
:method:
POST
:path:
/event/reserve-court-new-do?ajax=true
:scheme:
https
Accept:
*/*
Accept-Encoding:
gzip, deflate, br, zstd
Accept-Language:
en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6,fr;q=0.5
Content-Length:
310
Content-Type:
application/x-www-form-urlencoded; charset=UTF-8
Cookie:
PHPSESSID=foja1ncb6re98aba8mtkq174pk; isLoggedIn=1; __cf_bm=yA5TRCeO3_.P5eDdyA3r7guWAB4C0Gbr51nMROT0KsI-1721200537-1.0.1.1-2LkBdwKuX5zMF65nv007IiDjLCHWQrr.kEsSPpwb2uYB5wDZi_yA4zrhMFDuyS_.Q2wGcKoMsTYCumMh4P_Cow; SessionExpirationTime=1721229601
Origin:
https://lt.clubautomation.com
Priority:
u=1, i
Referer:
https://lt.clubautomation.com/event/reserve-court-new
Sec-Ch-Ua:
"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"
Sec-Ch-Ua-Mobile:
?0
Sec-Ch-Ua-Platform:
"Windows"
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-origin
User-Agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
X-Requested-With:
XMLHttpRequesta
```

Request Payload --

```bash
reservation-list-page: 1 # leave as 1
user_id: 147865
event_member_token_reserve_court: a772d1bc5fe08838ca5d015b8a939b18 # probably token retrieved on login. hexadecimal
current_guest_count: 0 # leave as 0
component: 42 # seems to always be 42
club: -1 # not sure what this does yet
host: 147865 # not sure what this does yet
date: 07/25/2024
interval: 120 # set to 120 always
time-reserve: 1721947800 
location-reserve: 27 # always set to 27 (prolly sunnyvale)
surface-reserve: 0 # always 0
courtsnotavailable: # leave null
join-waitlist-case: 1 # not sure what this is. 0 or 1
```

sample un-encoded payload:
```bash
reservation-list-page=1&user_id=147865&event_member_token_reserve_court=a772d1bc5fe08838ca5d015b8a939b18&current_guest_count=0&component=42&club=-1&host=147865&date=07%2F25%2F2024&interval=120&time-reserve=1721947800&location-reserve=27&surface-reserve=0&courtsnotavailable=&join-waitlist-case=1
```

when I hit confirm

ajax request payload

```bash
reservation-list-page: 1
user_id: 147865
event_member_token_reserve_court: a772d1bc5fe08838ca5d015b8a939b18
current_guest_count: 0
component: 42
club: -1
host: 147865
date: 07/25/2024
interval: 120
time-reserve: 1721947800
location-reserve: 27
surface-reserve: 0
courtsnotavailable: 
join-waitlist-case: 1
is_confirmed: 1
```
