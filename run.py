#For executing from ubuntu
import sys
sys.path.insert(0, '/var/www/html/body-by-science/')

from src.app import app

if __name__ == '__main__':
    app.run(debug=True) # option to specify the port