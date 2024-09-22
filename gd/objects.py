class Level:
    def __init__(self, raw_str: str):
        if not isinstance(raw_str, str):
            raise ValueError("Level string must be a str!")\
            
        self.raw = raw_str
    
    def __str__(self) -> str:
        return self.raw