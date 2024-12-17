from pydantic import BaseModel, Field
from typing import Optional


class BookRequest(BaseModel):
    """
    Request model for book data validation
    """
    id: Optional[int] = Field(
        default=None, description="id not needed at create")
    title: str = Field(max_length=20)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 0,
                'title': 'Animals',
                'author': 'John',
                'description': 'Animals Book',
                'rating': 1
            }
        }
    }
