from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from src.routes.authroutes import router as auth_router
from src.mails.spamEmails import fetch_spem_data
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
    try:
        print("Updating spam lists...")
        fetch_spem_data()
        print("Spam lists updated.")
    except Exception as e:
        print(f"Error updating spam lists: {e}")

scheduler = BackgroundScheduler(
    executors={"default": ThreadPoolExecutor(1)}  
)
scheduler.add_job(schedule_spam_update, "interval", days=7)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    print("Fetching spam data on startup...")
    await fetch_spem_data()  
    print("Startup task completed.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down scheduler...")
    scheduler.shutdown()
    print("Scheduler shut down.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
