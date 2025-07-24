from flask import Flask

from app.storage import URLStorage
from app.routes import register_routes

# App + storage init
app = Flask(__name__)
storage = URLStorage()


# Register all routes with access to storage
register_routes(app, storage)

if __name__ == '__main__':
    app.run(debug=True)
