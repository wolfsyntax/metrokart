# Guide
## Installing requirements:
1. Python

2. Virtual Environment<br/>
a. VirtualEnv<br/>
 ```pip install virtualenv```<br/>
b. PipEnv<br/>
  ```pip install pipenv```

3.1 Using pipenv<br/>
    ```pipenv shell```
    
3.2 Using VirtualEnv
- Create virtual python environment with ```virtualenv```<br>
    ```virtualenv env_name```<br/>
    
- Activate virtual python environment (Windows)<br/>
```env_name/Scripts/activate```
 
4. Additional modules
```pip install -r  requirements.txt```

5. Create MySQL Database with default configuration <br/>
```http://127.0.0.1/phpmyadmin/server_databases.php```<br/>
    Database Name: metrokart<br/>
6. Creating Table using ```migrate``` command<br/>
```python manage.py migrate```<br/>

7. Creating superuser/administrator account<br/>
```python manage.py createsuperuser```