#For executing from ubuntu
import sys
sys.path.insert(0, '/var/www/html/body-by-science/')

from src.app import app

if __name__ == '__main__':
    app.run(port=4996, debug=True) # option to specify the port