from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from src.routes.authroutes import router as auth_router
from src.mails.spamEmails import fetch_spem_data
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://check-spamemails-client.onrender.com"],  
    allow_credentials=True,                  
    allow_methods=["*"],                  
    allow_headers=["*"],                   
)




app.include_router(auth_router, prefix="/auth", tags=["auth"])



def threaded_fetch_spam_data():
    try:
        print("Fetching spam data in a separate thread...")
        fetch_spem_data()
        print("Spam data fetched successfully.")
    except Exception as e:
        print(f"Error while fetching spam data: {e}")


def schedule_spam_update():
    try:
        print("Running scheduled spam data fetch...")
        thread = threading.Thread(target=threaded_fetch_spam_data)
        thread.start()
        thread.join()  
    except Exception as e:
        print(f"Error in scheduled spam data fetch: {e}")


scheduler = BackgroundScheduler(
    executors={"default": ThreadPoolExecutor(1)} 
)
scheduler.add_job(schedule_spam_update, "interval", days=7)

@app.on_event("startup")
async def startup_event():
    try:
        print("Starting the application...")
        if not scheduler.running: 
            scheduler.start()
        print("Scheduler started.")
        print("Fetching spam data on startup...")
        threading.Thread(target=threaded_fetch_spam_data).start()
        print("Startup task triggered.")
    except Exception as e:
        print(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        print("Shutting down scheduler...")
        if scheduler.running:
            scheduler.shutdown(wait=False) 
        print("Scheduler shut down.")
    except Exception as e:
        print(f"Error during shutdown: {e}")

@app.get("/fetch-spam-data")
async def fetch_spam_data_manually():
    try:
        print("Manual fetch request received.")
        threading.Thread(target=threaded_fetch_spam_data).start()
        return {"status": "Success", "message": "Spam data fetch triggered manually."}
    except Exception as e:
        return {"status": "Error", "message": f"Failed to trigger spam data fetch: {e}"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
