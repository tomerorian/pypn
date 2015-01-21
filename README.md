# pypn
push notifications using python (with apn)

# Requirements

- python 2.7
- apn

# Usage

usage: pypn.py [-h] [--msg MSG] [--cert CERT] [--token TOKEN] {regular,silent}

Sends push notifications

positional arguments:
  {regular,silent}      Type of push

optional arguments:
  -h, --help            show this help message and exit
  --msg MSG, -m MSG     Message to send
  --cert CERT, -c CERT  Certificate to use
  --token TOKEN, -t TOKEN
                        Token to use