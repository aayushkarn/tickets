# Steps

```bash
pip install -r requirements.py
```


```bash
python run.py
```
We use `python run.py` at first to initialize all our DB models. After this is done we do this:
```bash
python create_superuser.py
```
Note: Update location of db in create_superuser.py if the DB is in different location
```python
# I have my DB in instance folder
connection = sqlite3.connect("instance/db.sqlite3")
```
If you don't want to use ``create_superuser.py`` then you can simply register a user in app and then manually edit the ``users`` database's ``is_superuser`` to ``1`` 

Also setup ``.env`` file and place it inside `main` folder. Add following data to the file
```python
SECRET_KEY = "YOUR-SECRET-KEY"
KHALTI_TEST_PUBLIC_KEY = "KHALTI-TEST-PUBLIC-KEY"
KHALTI_TEST_SECRET_KEY = "KHALTI-TEST-SECRET-KEY"
KHALTI_LIVE_PUBLIC_KEY = "KHALTI-LIVE-PUBLIC-KEY"
KHALTI_LIVE_SECRET_KEY = "KHALTI-LIVE-SECRET-KEY"
```
