import re
from abc import ABC


class Helper(ABC):

    @classmethod
    def pascal_to_camel_plural(cls):
        # Use regex to split the class name at capital letters
        words = re.findall("[A-Z][a-z]*", cls.__name__)

        # Join the words with underscores
        camel_case_plural = "_".join(words).lower()

        # Pluralize the last word
        if words:
            last_word = words[-1]
            if last_word.endswith("s") or last_word.endswith("x"):
                camel_case_plural += "es"
            else:
                camel_case_plural += "s"

        return camel_case_plural

    @classmethod
    def drop_table(cls, CONN, CURSOR):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                        DROP TABLE IF EXISTS {cls.pascal_to_camel_plural()};
                    """
                )
        except Exception as e:
            CONN.rollback()
            return e

    @classmethod
    def get_all(cls, CONN, CURSOR):
        try:
            with CONN:
                result = CURSOR.execute(f"SELECT * FROM {cls.pascal_to_camel_plural()}")
                rows = result.fetchall()
                return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            return e