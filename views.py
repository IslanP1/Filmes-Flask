from main import app

@app.route('/')
def index():
    return "Hello world!"
        