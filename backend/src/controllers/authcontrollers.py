from fastapi import HTTPException, status, Response, Depends
from src.db.db import user_collection, session_collection, spam_emails_list, spam_domain_list
from src.utils.sessionConfig import hash_password, verify_password, create_session
from src.models.models import UserCreate
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import Request



def create_user(user: UserCreate, response: Response):
    email = user.email 
    domain = email.split("@")[-1]

    if spam_emails_list.find_one({"email": email}) or spam_domain_list.find_one({"domain": domain}):
        raise HTTPException(status_code=400, detail="The email is a spam email. Please check the email.")



    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
       
    }

    result = user_collection.insert_one(user_data)

    session_data = create_session(str(result.inserted_id))
    session_collection.insert_one(session_data)

    # Set the session token in cookies
    # response.set_cookie(
    #     key="session_token",
    #     value=session_data["session_token"],
    #     httponly=True,
    #     secure=False,  # Set this to True when using HTTPS in production
    #     max_age=3600  # Optional: Set an expiration time for the session token cookie (1 hour in this case)
    # )


    return {"message": "User created successfully", "user_id": str(result.inserted_id)}




def user_login(data):
   
    user = user_collection.find_one({"email": data.email})  
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password. please check the password!")

   
    session_data = create_session(str(user["_id"]))
    session_collection.insert_one(session_data)

   
    response = Response(content="Login successful")
    response.set_cookie(
        key="session_token",
        value=session_data["session_token"],
        httponly=True,
        secure=False, 
        max_age=3600  
    )
    return response





def get_user_by_session(request: Request):
 
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session token is expired")

    session = session_collection.find_one({"session_token": session_token})
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    user = user_collection.find_one({"_id": ObjectId(session["user_id"])})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
 
    return {
        "username": user["username"],
        "email": user["email"]
    }
