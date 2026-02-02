import sqlite3
from typing import Optional, List, Tuple, Any
import datetime

class Database:
    def __init__(self, db_name: str = "terminij.db"):
        self.db_name = db_name
        self.init_db()

        def get_connetion(self):
            return sqlite3.connect(self.db_name)
        
        def init_db(self):