# Django Update Counter Demo

This app demonstrates how to update a counter and return the number to users.
Three methods are implemented in ``counter/views.py``.

``counter1()`` simply load the counter from database, add by one, and save the
counter back to the database.  This is incorrect.  The database values will be
incorrect and the users will get incorrect values.

``counter2()`` and ``counter3()`` use **F()-expression** to update the database
and reload the value with ``refresh_from_db()``.  However, this is incorrect
either.  Although the database value will be correct, the value retrieved by
``refresh_from_db()`` is the latest value in the database not the value updated
by ``save()``.  Users may get the value updated by other transactions.
``counter3()`` demonstrates the race condition by sleeping randomly.

``counter4()`` uses ``select_for_update()`` to lock the row.  Since the row is
locked, it is guaranteed that no one will update the row between SELECT and
UPDATE.  If two ``select_for_update()`` select the same row, the later one will
wait until the lock is released.  This ensures the local variable
``num_visited`` is the value for that request.


## Test

Install Python packages:

```
pip install -r requirements.txt
```

Set up the database in ``counter_demo/settings.py``:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'counter_demo',
        'USER': '[user]',
        'PASSWORD': '[password]',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Migrate the database:

```
./manage.py migrate
```

Launch the server with ``gunicorn``:

```
gunicorn -w 10 counter_demo.wsgi
```

And then, run the stress test with:

```
./stress_test.py http://localhost:8000/counter1
./stress_test.py http://localhost:8000/counter2
./stress_test.py http://localhost:8000/counter3
./stress_test.py http://localhost:8000/counter4
```
