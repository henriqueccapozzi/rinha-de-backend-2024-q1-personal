ls -la
python3 manage.py migrate
ls -la
python3 manage.py dumpdata bank.Client --indent 2 > initial_data.json
python3 manage.py loaddata initial_data.json 
python3 manage.py loaddata initial_data.json 
cat initial_data.json 
python3 manage.py createsuperuser 
python3 manage.py dumpdata 
exit
python manage.py loaddata initial_data
python3 manage.py migrate
python manage.py loaddata initial_data
