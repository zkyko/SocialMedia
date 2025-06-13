from sqlalchemy import create_engine, inspect
from app.database import SQLALCHEMY_DATABASE_URL

def check_tables():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    inspector = inspect(engine)
    print("Tables in the database:")
    print(inspector.get_table_names())
    
    # Check if alembic_version table exists and its content
    with engine.connect() as conn:
        try:
            result = conn.execute("SELECT * FROM alembic_version")
            print("\nAlembic version:")
            for row in result:
                print(f"Version: {row[0]}")
        except Exception as e:
            print(f"\nError checking alembic_version: {e}")

if __name__ == "__main__":
    check_tables()
