from app import app
import uvicorn
import multiprocessing
import os

# Determine environment: "development" or "production"
ENV = os.getenv("ENV", "development")
reload_flag = ENV != "production"

# Use a heuristic for the number of workers
max_workers = max(1, multiprocessing.cpu_count() // 2)
print(f"Max workers: {max_workers}")

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        workers=max_workers, 
        reload=reload_flag,
        log_level="info"
    )
