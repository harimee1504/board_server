import os
from api.main import app

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT")) 