## How to run
Make sure you already installed **python3** in your machine

1. Create your virtualenv and activate
2. Install library `pip install -r requirements.txt`
3. init flask migrate file location `python3 migrate.py db init`
    <br> `python3 migrate.py db upgrade`
    <br> if you wanna update table from models `python3 migrate.py db migrate`
4. create your start-app.sh file and run server command `sh ./start-app.sh`
