# Steps

```bash
pip install -r requirements.py
```


```bash
pip run.py
```
We use pip run.py at first to initialize all our DB models. After this is done we do this:
```bash
python create_superuser.py
```
Note:Update location of db in create_superuser.py if the DB is in different location
```python
# I have my DB in instance folder
connection = sqlite3.connect("instance/db.sqlite3")
```
If you dont want to use ``create_superuser.py`` then you can simply register a user in app and then manually edit the ``users`` database's ``is_superuser`` to ``1`` 
