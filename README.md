# books

Simple Books CRUD (Flask + PostgreSQL)

Quick steps:

1. Create a PostgreSQL database, e.g. `booksdb` and a user.
2. Set `DATABASE_URL` environment variable, for example:

```
export DATABASE_URL=postgresql://user:pass@localhost:5432/booksdb
set DATABASE_URL=postgresql://user:pass@localhost:5432/booksdb  # Windows cmd
```

3. (Optional) set `FLASK_SECRET` for session security.
4. Install deps:

```bash
python -m pip install -r requirements.txt
```

5. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000/ and use the UI.
