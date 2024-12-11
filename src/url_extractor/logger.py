# src/url_extractor/logger.py
import logging.config
import yaml
import os
from pathlib import Path


def setup_logging():
    """Initialize logging configuration"""
    config_path = Path(__file__).parent.parent.parent / 'config' / 'logging_config.yaml'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Ensure logs directory exists
        log_dir = Path(__file__).parent.parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    return logging.getLogger('url_extractor')
