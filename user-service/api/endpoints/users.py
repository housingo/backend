from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_409_CONFLICT
from passlib.hash import bcrypt
import jwt
from pydantic import BaseModel
import os
from ..database.db_mongo import (
    queryByEmail,
    queryByUser,
    addAccount,
    queryByEmailOrUsername,
    updateEmail,
    updatePassword,
    endSubscription,
)
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

router = APIRouter()
auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


class RegisterAccount(BaseModel):
    password: str
    email: str
    username: str


class LoginAccount(BaseModel):
    username: str
    password: str


class ChangePass(BaseModel):
    password: str


class ChangeEmail(BaseModel):
    email: str


jwt_secret = os.environ["JWT_SECRET"]


@router.post("/register")
def registerMongo(account: RegisterAccount):

    checkDB = queryByEmailOrUsername(account.email, account.username)
    if checkDB is not None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User already registered"
        )

    if checkDB is None:
        userDict = {
            "username": account.username,
            "password": bcrypt.hash(account.password),
            "email": account.email,
            "tier": "free",
            "isActive": "true",
            "dateCreated": str(datetime.now()),
            "dateUpdated": str(datetime.now()),
            "stripe_id": "",
            "phone": "",
        }
        addAccount(userDict)
        return "User created succesfully!", 200


@router.post("/login")
def login(account: LoginAccount):
    user = queryByUser(account.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username!",
        )

    if bcrypt.verify(account.password, user["password"]):
        user_obj = {
            "email": user["email"],
            "username": user["username"],
            "isActive": user["isActive"],
            "tier": user["tier"],
        }
        token = jwt.encode(user_obj, jwt_secret)

        return {"access_token": token, "token_type": "bearer"}
    else:
        return "Invalid password!"


@router.get("/me")
def get_me(token: str = Depends(auth2_scheme)):
    payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    user = queryByEmail(payload.get("email"))

    return user


@router.put("/password")
def changePass(password: ChangePass, token: str = Depends(auth2_scheme)):
    payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    new_pass = bcrypt.hash(password.password)
    return updatePassword(payload.get("email"), new_pass)


@router.put("/email")
def changeEmail(email: ChangeEmail, token: str = Depends(auth2_scheme)):
    payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    return updateEmail(payload.get("email"), email.email)


@router.put("/subscription")
def cancel(token: str = Depends(auth2_scheme)):
    payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    print(payload.get("email"))
    return endSubscription(payload.get("email"))
