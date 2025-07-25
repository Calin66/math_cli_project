import threading
import queue
import json

from logic import calc_pow, calc_fibonacci, calc_factorial
from database import save_request

task_queue = queue.Queue()

worker_thread = None

def worker():
    print("[Worker] Worker started and waiting for tasks...", flush=True)
    while True:
        print("[Worker] Waiting for task from queue...", flush=True)
        task = task_queue.get()

        if task is None:
            print("[Worker] Shutdown signal received. Exiting worker...", flush=True)
            task_queue.task_done()
            break

        task_type, request = task
        print(f"[Worker] Got task: {task_type} - {request}", flush=True)

        try:
            if task_type == 'power':
                result = calc_pow(request.base, request.exp)
            elif task_type == 'fibonacci':
                result = calc_fibonacci(request.n)
            elif task_type == 'factorial':
                result = calc_factorial(request.n)
            else:
                result = 'Invalid operation'

            print("[DEBUG] Result calculated: ", result, flush=True)

            try:
                save_request(task_type, request.json(), str(result))
            except Exception as e:
                print(f"[Worker] ERROR during save_request: {e}", flush=True)

            print(f"[Worker] {task_type}({request.dict()}) = {result}", flush=True)

        except Exception as e:
            print(f"[Worker] Error while processing task: {e}", flush=True)

        task_queue.task_done()

def start_worker():
    global worker_thread
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

def wait_for_worker():
    if worker_thread:
        worker_thread.join()
