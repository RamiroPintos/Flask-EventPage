# Flask-EventPage

## Installation

1- Create a virtual environmen:
```
python3 -m venv venv
```

2- Activate:
```
source venv/bin/activate
```

3- Intall requirements:
```
pip3 install -r requirements.txt
```

4- Create environment variables:
```
export DB_CONNECTION="yourUser:yourPassword"
export MAIL_USERNAME="yourEmail"
export MAIL_PASSWORD="yourPassEmail"
```

5- Create data base(From the python terminal):
```
>>> from models.models import db
>>> db.create_all()
```

6- Run:
```
python3 app.py
```


## API commands

### USER:

GET by ID:
```
curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/user/id
```

GET all:
```
curl -H "Accept:application/json" http://localhost:5000/api/users
```

DELETE:
```
curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/user/id
```

### EVENT:

GET by ID:
```
curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/event/id
```

GET all:
```
curl -H "Accept:application/json" http://localhost:5000/api/event/
```

PUT:
```
curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:5000/api/event/id -d '{"title":"", "type":""}'
```

Delete:
```
curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/event/id
```

Approve event:
```
# curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:5000/api/event/id/approve
```

### COMMENT:

GET by ID:
```
curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comment/id
```

GET by Events:
```
curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comments/id
```

DELETE:
```
curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/comment/id
```
