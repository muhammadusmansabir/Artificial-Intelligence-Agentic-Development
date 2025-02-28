**FastAPI To-Do App with Alembic and PostgreSQL**

## Installation
To set up the project with Alembic and PostgreSQL, install the required dependencies:

```python
uv add alembic
uv add psycopg2-binary
```
**New Project Setup**
Follow these steps to initialize Alembic and configure it for database migrations:

**Initialize Alembic**

uv run alembic init alembic
**Set the Database URL**

Locate the alembic.ini file.
Modify the sqlalchemy.url entry to point to your PostgreSQL database, e.g.:
sqlalchemy.url = postgresql+psycopg2://user:password@localhost/dbname
Create SQLAlchemy Model

Define a SQLAlchemy model for your table, for example:
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

```python
Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
```
**Set Target Metadata in Alembic**

Open alembic/env.py and update the target metadata:
from models import Base  # Import the model base
target_metadata = Base.metadata
Running Migrations
Whenever you make changes to your models, run the following commands:

**Generate Migration Script**

`uv run alembic revision --autogenerate -m "create todos table"`
**Apply Migrations**

`uv run alembic upgrade head`
This will create and apply the necessary database schema changes based on your models.