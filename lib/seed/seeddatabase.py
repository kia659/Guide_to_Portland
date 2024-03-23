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

        # Opens the CSV file for reading as a text file, ensuring it is UTF-8 encoded, and handling newline characters appropriately
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            # Creates a CSV reader object (reader) using DictReader, which interprets each row of the CSV file as a dictionary where keys are column headers and values are cell values
            reader = csv.DictReader(file)
            cursor = self.connection.cursor()

            for row in reader:
                cursor.execute(
                    "INSERT INTO activities (name, description, activity_type, website, address, neighborhood) VALUES (?, ?, ?, ?, ?, ?)",
                    (row['name'], row['description'], row['activity_type'], row['website'], row['address'], row['neighborhood'])
                )
                self.connection.commit()

# Checks if the script is being run directly as the main program
if __name__ == "__main__":
    db_file = "database.db"
    csv_file = "lib/seed/portland_guide_seed_data.csv"

    with SeedDatabase(db_file) as seed_db:
        seed_db.seed_from_csv(csv_file)