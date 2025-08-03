import threading
import queue
import json

from logic import calc_pow, calc_fibonacci, calc_factorial
from database import save_request

task_queue = queue.Queue()

worker_thread = None

from logging_config import setup_logging
import logging
setup_logging()

def worker():
    logging.info("[Worker] Worker started and waiting for tasks...")
    while True:
        logging.info("[Worker] Waiting for task from queue...")
        task = task_queue.get()

        if task is None:
            logging.info("[Worker] Shutdown signal received. Exiting worker...")
            task_queue.task_done()
            break

        task_type, request = task
        logging.info(f"[Worker] Got task: {task_type} - {request}")

        try:
            if task_type == 'power':
                result = calc_pow(request.base, request.exp)
            elif task_type == 'fibonacci':
                result = calc_fibonacci(request.n)
            elif task_type == 'factorial':
                result = calc_factorial(request.n)
            else:
                result = 'Invalid operation'

            logging.info(f"[DEBUG] Result calculated: {result}")

            try:
                save_request(task_type, request.json(), str(result))
            except Exception as e:
                logging.info(f"[Worker] ERROR during save_request: {e}")

            logging.info(f"[Worker] {task_type}({request.dict()}) = {result}")

        except Exception as e:
            logging.info(f"[Worker] Error while processing task: {e}")

        task_queue.task_done()

def start_worker():
    global worker_thread
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

def wait_for_worker():
    if worker_thread:
        worker_thread.join()
