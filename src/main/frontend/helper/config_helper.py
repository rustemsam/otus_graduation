import os
import json
import logging


class ConfigHelper:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_key(key):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../..")
        )

        config_path = os.path.join(project_root, "tests/config/config.json")

        print(f"Checking config file at: {config_path}")

        api_key = None
        if os.path.exists(config_path):
            print("Config file found. Attempting to read...")
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    print(f"Config loaded: {config}")
                    api_key = config.get(key)
                    print(f"Retrieved key '{key}': {api_key}")
            except json.JSONDecodeError:
                ConfigHelper.logger.error(f"Error parsing {config_path}")

        if not api_key:
            print(
                f"Key '{key}' not found in config.json. Checking environment variables..."
            )
            api_key = os.getenv(key)
            print(f"Retrieved from environment: {api_key}")

        assert api_key, f"Key {key} not found in config.json or environment variables"
        return api_key
