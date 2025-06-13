# debug_import.py
import sys
import os

print("--- sys.path ---")
for p in sys.path:
    print(p)

print("\n--- Attempting to import app.database ---")
try:
    from app import database
    print(f"Module 'app.database' imported successfully.")
    print(f"Location of loaded app.database: {database.__file__}")

    # Try to access 'engine'
    if hasattr(database, 'engine'):
        print(f"'engine' found in app.database: {database.engine}")
    else:
        print(f"'engine' NOT found in app.database via hasattr().")
        print("Contents of the loaded database file (first 500 chars):")
        with open(database.__file__, 'r') as f:
            print(f.read(500))

except ImportError as e:
    print(f"ImportError caught: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\n--- Done ---")