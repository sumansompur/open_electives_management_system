from OEMS import app
from OEMS import db

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        db.close()