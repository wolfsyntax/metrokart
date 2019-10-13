# Guide
#### Installing requirements:
1. Python (version 3.7.4)
https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe
2. XAMPP / WAMP

#### Commands
1. Virtual Environment<br/>
a. VirtualEnv<br/>
 ```pip install virtualenv```<br/>
b. PipEnv<br/>
  ```pip install pipenv```

2.1 Using pipenv<br/>
    ```pipenv shell```
    
2.2 Using VirtualEnv
- Create virtual python environment with ```virtualenv```<br>
    ```virtualenv env_name```<br/>
    
- Activate virtual python environment (Windows)<br/>
```env_name/Scripts/activate```
 
3. Additional modules
```pip install -r  requirements.txt```

4. Create MySQL Database with default configuration <br/>
```http://127.0.0.1/phpmyadmin/server_databases.php```<br/>
    Database Name: metrokart<br/>
    
5. Creating Table using ```migrate``` command<br/>
```python manage.py migrate```<br/>

6. Creating superuser/administrator account<br/>
```python manage.py createsuperuser```


#### Error Fixed
mysql-client error installation, go to ```fix``` directory then execute this command:<br/>

```pip install mysqlclient-1.4.1-cp37-cp37m-win32.whl```
