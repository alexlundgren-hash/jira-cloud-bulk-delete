# Bulk delete users

Copy the example environment file.
```
cp .env-example .env
```
Add credentials to `.env` file.

Create and activate a virtual environment.
```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.
```
pip install -r requirements.txt
```

Run the scripts to read generate the user list.
```
python read_users.py
```

Run the script to delete users.
```
python delete_users.py
```
