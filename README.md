## venv
```
python3 -m venv venv
source venv/bin/activate
deactivate 
```

## django
```
python manage.py createsuperuser
python manage.py makemigration [[PROJECT_NAME]] #change schema
python manage.py migrate #apply
python manage.py loaddata urls #from /fixtures/urls.py
```

## docker
```
docker ps
docker build -t portfolio .
docker run -p 8000:8000 portfolio
docker-compose up -d
docker exec -it [[CONTAINER_ID]] [[COMMAND]]
```

## docker
```
psql -U [[db_username]]
\dt #list tables
```