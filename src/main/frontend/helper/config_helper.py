import json
import logging
import os
from typing import Any, Dict


class ConfigHelper:
    logger = logging.getLogger(__name__)
    _config_cache: Dict[str, Any] = {}

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from a JSON file and cache it."""
        if not ConfigHelper._config_cache:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            config_path = os.path.join(project_root, "tests/config/config.json")
            ConfigHelper.logger.info(f"Checking config file at: {config_path}")

            if os.path.exists(config_path):
                ConfigHelper.logger.info("Config file found. Attempting to read...")
                try:
                    with open(config_path) as f:
                        ConfigHelper._config_cache = json.load(f)
                    ConfigHelper.logger.debug(f"Config loaded: {ConfigHelper._config_cache}")
                except json.JSONDecodeError as e:
                    ConfigHelper.logger.error(f"Error parsing {config_path}: {e}")
            else:
                ConfigHelper.logger.warning(f"Config file not found at {config_path}.")

        return ConfigHelper._config_cache

    @staticmethod
    def get_key(key: str) -> Any:
        """Retrieve a configuration value from the config file or environment variables."""
        config = ConfigHelper.load_config()
        value = config.get(key)
        if value is None:
            ConfigHelper.logger.warning(
                f"Key '{key}' not found in config file. Checking environment variables..."
            )
            value = os.getenv(key)
            ConfigHelper.logger.info(f"Retrieved from environment: {value}")
        if value is None:
            error_msg = f"Key '{key}' not found in config file or environment variables"
            ConfigHelper.logger.error(error_msg)
            raise KeyError(error_msg)
        return value