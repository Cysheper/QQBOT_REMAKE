import json
import random
from pydantic import BaseModel
import os
from Modules.core import Status
from typing import Any

class database:
    def __init__(self, db_name):
        self.db_name = db_name
        if not os.path.exists(f"{db_name}.json"):
            with open(f"{db_name}.json", "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
            

    def insert(self, key: str, payload: Any) -> Status:
        try:
            data = self.getAll()
            
            if key not in data:
                data[key] = [payload]
            
            else: data[key].append(payload)

            with open(f"{self.db_name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return Status(code="ok", message="Insert successful")
        
        except Exception as e:
            return Status(code="error", message=f"Insert failed: {str(e)}")

    
    def random(self, key: str):
        return random.choice(self.getAll()[key])
    
    def getAll(self):
        with open(f"{self.db_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        return data
 
            
        
        

    
    