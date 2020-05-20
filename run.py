from main.controllers.category import *
from main.controllers.item import *
from main.controllers.user import *


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from main.db import db
    app.run(port=5000, debug=True)
