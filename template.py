import os
from pathlib import Path
import logging
import json
from pythonjsonlogger import jsonlogger

# ======================
# 1. Enhanced Logging Setup
# ======================
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()

# JSON Formatter with additional context
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)  # Explicitly set level

# ======================
# 2. Directory/File Creation
# ======================
list_of_files = [
    "src/__init__.py",  # Fixed typo (init_.py → __init__.py)
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create directory if needed (with existence check)
    if filedir != "":
        try:
            os.makedirs(filedir, exist_ok=True)  # Changed to makedirs
            logger.info(
                "Directory operation",
                extra={
                    "action": "create_directory",
                    "status": "success" if not Path(filedir).exists() else "already_exists",
                    "directory": str(filedir),
                    "for_file": filename
                }
            )
        except Exception as e:
            logger.error(
                "Directory operation failed",
                extra={
                    "error": str(e),
                    "directory": str(filedir)
                }
            )
            continue  # Skip file creation if directory fails

    # Create file if needed
    try:
        if not filepath.exists() or filepath.stat().st_size == 0:
            filepath.touch()  # More Pythonic than open()+close()
            logger.info(
                "File operation",
                extra={
                    "action": "create_file",
                    "status": "created",
                    "filepath": str(filepath)
                }
            )
        else:
            logger.info(
                "File operation",
                extra={
                    "action": "check_file",
                    "status": "already_exists",
                    "filepath": str(filepath),
                    "size_bytes": filepath.stat().st_size
                }
            )
    except Exception as e:
        logger.error(
            "File operation failed",
            extra={
                "error": str(e),
                "filepath": str(filepath)
            }
        )