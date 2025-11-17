from pydantic import BaseModel, EmailStr, constr


class ContactRequest(BaseModel):
    name: constr(min_length=2)
    email: EmailStr
    message: constr(min_length=10)
