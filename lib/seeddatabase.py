import csv
import sqlite3

class SeedDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def seed_from_csv(self, csv_file):
        if not self.connection:
            raise RuntimeError("Database connection not established.")

        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            cursor = self.connection.cursor()

            for row in reader:
                # Assuming the CSV has columns corresponding to the tables
                cursor.execute(
                    "INSERT INTO Activities (activity_name, activity_description, activity_type, activity_website, activity_address, activity_neighborhood) VALUES (?, ?, ?, ?, ?, ?)",
                    (row['activity_name'], row['activity_description'], row['activity_type'], row['activity_website'], row['activity_address'], row['activity_neighborhood'])
                )
                self.connection.commit()

                # You can similarly insert data into other tables if needed

if __name__ == "__main__":
    # Example usage
    db_file = "database.db"
    csv_file = "portland_guide_seed_data.csv"

    with SeedDatabase(db_file) as seed_db:
        seed_db.seed_from_csv(csv_file)