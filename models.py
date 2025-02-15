from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewsHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<NewsHistory {self.url}>'
