
<p align="left"> <b>Page Pluse(Bookify)</b> is a book store built in Django.
  
<h3 align="left"> Features</p></h3>

<ul>
<li style="font-weight:normal;">Front Page</li>
<li style="font-weight:normal;">Books by Category</li>
<li>Single Book Page</li>
<li>User Login and Registration</li>
<li>User Cart</li>
<li>Checkout System</li>
<li>User Dashboard(View Order, edit profile)</li>
</ul>

<h2 align="left"> Installation:</h2>
<h4>Step 1: clone the repo <br></h4>
<h4>Step 2: install python and pip<br></h4>
<h4>Step 3: install required liberies <br> </h4>

```python
pip install -r requirements.txt
```

<h4> 4. Step 4: Run migrations and create a db. from cmd type </h4>

```python
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
```

<h4> Step 5: create an admin account</h4>

```python
python manage.py createsuperuser
```
