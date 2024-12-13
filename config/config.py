import os

MONGO_CONFIG = {
    "host": os.getenv("MONGO_HOST", "localhost"),
    "port": int(os.getenv("MONGO_PORT", 27017)),
    "username": os.getenv("MONGO_USER", ""),
    "password": os.getenv("MONGO_PASSWORD", ""),
    "authSource": os.getenv("MONGO_AUTH_SOURCE", "admin"),
    "database": os.getenv("MONGO_DB_NAME", "wb-products"),
}

# MongoDB URI
if MONGO_CONFIG["username"] and MONGO_CONFIG["password"]:
    MONGO_URI = (
        f"mongodb://{MONGO_CONFIG['username']}:{MONGO_CONFIG['password']}@"
        f"{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}/{MONGO_CONFIG['authSource']}/"
    )
else:
    MONGO_URI = f"mongodb://{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}/"

# Application Settings
APP_CONFIG = {
    "app_name": "Wildberries Analytics GUI",
    "version": "1.0.0",
    "default_export_dir": os.path.join(os.getcwd(), "exports"),
    "default_import_dir": os.path.join(os.getcwd(), "imports"),
    "logs_dir": os.path.join(os.getcwd(), "logs"),
}

# Debug Mode
DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]
