from models.__init__ import CONN, CURSOR
import re
from abc import ABC



class Helper(ABC):

    @classmethod
    def pascal_to_camel_plural(cls):
        words = re.findall("[A-Z][a-z]*", cls.__name__)
        camel_case_plural = "_".join(words).lower()
        if words:
            last_word = words[-1]
            if last_word.endswith("s") or last_word.endswith("x"):
                camel_case_plural += "es"
            elif last_word.endswith("y"):
                camel_case_plural = camel_case_plural[:-1] + "ies"
            else:
                camel_case_plural += "s"

        return camel_case_plural

    @classmethod
    def drop_table(cls):
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
    def get_all(cls):
        try:
            with CONN:
                result = CURSOR.execute(f"SELECT * FROM {cls.pascal_to_camel_plural()}")
                rows = result.fetchall()
                return [cls.instance_from_db(row) for row in rows]
        except Exception as e:
            return e

    @classmethod
    def find_by_id(cls, id):
        try:
            with CONN:
                CURSOR.execute(
                    f"""
                    SELECT * FROM {cls.pascal_to_camel_plural()}
                    WHERE id = ?;
                    """,
                    (id,),
                )
                row = CURSOR.fetchone()
                return cls.instance_from_db(row) if row else None
        except Exception as e:
            print(f"Error finding record by id: {e}")
        return None
