# py-ip-log

## Quick start

1. clone repository, install libs check outdated

```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip list --outdated  # show outdated libs
```

2. get and log IP to fie

```sh
python log_ip_to_file.py
```

3. add new cron job

```shell
crontab -e 
0 * * * * cd /home/funker/git/py-ip-log && $(which python3) log_ip_to_file.py >> cron-log.log 2>&1
```
