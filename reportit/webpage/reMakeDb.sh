cd /Users/whoami/Documents/Github/ReportIt/reportit
rm db.sqlite3
cd webpage
rm -rf __pycache__
cd ..

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
python3 manage.py loaddata saved_data.json