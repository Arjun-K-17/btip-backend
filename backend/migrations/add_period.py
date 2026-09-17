import sqlite3
from pathlib import Path


# =========================================================
# Database Location
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "btip.db"


# =========================================================
# Migration
# =========================================================

def add_period_column():
    print("BTIP Database Migration")
    print("========================")

    print(f"Database: {DATABASE_PATH}")

    if not DATABASE_PATH.exists():
        print("Database file was not found.")
        print("No migration was performed.")
        return

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # Check existing columns
        # -------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(financial_data)"
        )

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]

        # -------------------------------------------------
        # Add period if missing
        # -------------------------------------------------

        if "period" in column_names:
            print(
                "✓ 'period' column already exists."
            )

        else:
            print(
                "Adding 'period' column..."
            )

            cursor.execute(
                """
                ALTER TABLE financial_data
                ADD COLUMN period VARCHAR(50)
                """
            )

            connection.commit()

            print(
                "✓ 'period' column added successfully."
            )

        # -------------------------------------------------
        # Verify
        # -------------------------------------------------

        cursor.execute(
            "PRAGMA table_info(financial_data)"
        )

        updated_columns = cursor.fetchall()

        updated_column_names = [
            column[1]
            for column in updated_columns
        ]

        if "period" in updated_column_names:
            print(
                "✓ Migration verification successful."
            )
        else:
            print(
                "✗ Migration verification failed."
            )

    except Exception as error:
        connection.rollback()

        print(
            "✗ Migration failed:"
        )

        print(error)

        raise

    finally:
        connection.close()


# =========================================================
# Run Migration
# =========================================================

if __name__ == "__main__":
    add_period_column()