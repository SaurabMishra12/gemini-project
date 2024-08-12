from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Achievement {self.title}>'
