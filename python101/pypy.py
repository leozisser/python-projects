from flask import Flask 
import python1 as py1

application = Flask(__name__)

@application.route('/hello')
def lol():
    a =  py1.query()
    return a

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3000)