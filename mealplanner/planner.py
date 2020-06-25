from dataclasses import dataclass, field
from typing import List

@dataclass
class Meal:
    name: str = ''
    category: str = ''
    fileloc: str = ''
    ingredients: List[str] = field(default_factory=list)
    
