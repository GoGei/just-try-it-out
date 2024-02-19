# just-try-it-out
## Project where I try to code something, nothing special

# Requirements
* Python 3.10
* Redis 7.2.3
* PostgreSQL 12.17
* MongoDB 7.0.0

# Install
## Local setup

### Clone
```bash
git clone https://github.com/GoGei/just-try-it-out.git
```

### Add hosts
* Ubuntu: /etc/hosts
* Windows: c:\Windows\System32\Drivers\etc\hosts
* MacOS: /private/etc/hosts
```bash
127.0.0.1               just-try-it-out.local
127.0.0.1           api.just-try-it-out.local
127.0.0.1         admin.just-try-it-out.local
```

### Create DB
```postgresql
create user just_try_it_out with encrypted password 'just_try_it_out' superuser createdb;
create database just_try_it_out with owner just_try_it_out;
```

### Copy settings
```bash
cp configs/example.py configs/settings.py
```

### Setup env
```bash
cd just-try-it-out/
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```