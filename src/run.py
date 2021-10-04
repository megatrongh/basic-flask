import os

from dotenv.main import load_dotenv
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from main import create_app

load_dotenv()

if os.environ.get("FLASK_ENV") == "production":
    app_config = ProductionConfig
elif os.environ.get("FLASK_ENV") == "test":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

application = create_app(app_config)

if __name__ == "__main__":
    application.run(host="0.0.0.0")
