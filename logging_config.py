import logging
import sys

class FlushingStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            FlushingStreamHandler(sys.stdout)
        ]
    )