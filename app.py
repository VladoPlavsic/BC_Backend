from lib import app
from lib.core.config import PORT

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)