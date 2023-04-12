import uuid

class FilenameGenerator:
    
    @classmethod
    def generate(
        cls, 
        user_id: int,
        original_filename: str
        ) -> str:
        return f'{uuid.uuid4().__str__()}-{user_id}-{original_filename}'
    