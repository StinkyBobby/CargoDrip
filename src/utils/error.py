from fastapi import HTTPException
from starlette import status

Forbidden = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access is forbidden, try to use Admin account"
)

Created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="Element was created"
)

