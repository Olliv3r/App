from app import app, db
from app.models import Tool, User


with app.app_context():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Tool': Tool, 'User': User}
