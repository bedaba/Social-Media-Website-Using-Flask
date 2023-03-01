#from flaskproject import routes ##external suggestion
from flaskproject import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)