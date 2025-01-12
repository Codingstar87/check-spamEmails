from fastapi import FastAPI , BackgroundTasks
from src.routes.authroutes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.mails.spamEmails import fetch_spem_data
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"  ],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"], 
)



app.include_router(auth_router, prefix="/auth", tags=["auth"])


def schedule_spam_update():
    print("Updating spam lists...")
    fetch_spem_data()
    print("Spam lists updated.")

scheduler = BackgroundScheduler()
scheduler.add_job(schedule_spam_update, 'interval', days=7)
scheduler.start()

@app.on_event("startup")
async def startup_event():

    fetch_spem_data()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
