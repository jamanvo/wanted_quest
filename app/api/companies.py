from fastapi import APIRouter

router = APIRouter()

# @router.post("/", response_model=UserResponse)
# def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
#     return create_user(db, user_data)
