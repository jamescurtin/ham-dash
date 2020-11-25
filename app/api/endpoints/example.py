from fastapi import APIRouter

router = APIRouter()


@router.get("/{example_id}")
def example(example_id: int, q: str = None):
    return {"example_id": example_id, "q": q}
