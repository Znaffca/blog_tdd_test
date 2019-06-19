# Sample blog app based on django tdd tutorial
### link: https://test-driven-django-development.readthedocs.io/

The idea of this code sample was a simple wish to learn about testing django apps. I used python coverage to check if all the test will give a 100% cover of the code.

That was also a good practice for me before i will start create my own blog apps. 


To get this app works:
1. Clone the repository and download to your PC
2. install requirements from file `requirements.txt` using 
    ```pip install -r requirements.txt``` in your virtualenv
3. Apply all migrations - run ```python manage.py migrate```
4. create superuser for your database using `python manage.py createsupersuser`
5. Run app in your local server and add some entries in admin panel. 

Enjoy.