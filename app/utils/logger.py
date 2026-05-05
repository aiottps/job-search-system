import logging
import sys
import os

def setup_logger(name: str = "job_search_assistant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler (Optional, logs to project root if local)
        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"), encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            # Silently fail if log directory can't be created (e.g. CI)
            pass
            
    return logger

logger = setup_logger()
