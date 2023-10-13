from app import app, db
from app.models import Tool, User

app.app_context().push()
db.create_all()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Tool': Tool, 'User': User}
