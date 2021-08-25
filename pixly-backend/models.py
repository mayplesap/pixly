"""Models for Pixly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database to provided Flask app"""

    db.app = app
    db.init_app(app)

class Pixly(db.Model):
    """Pixly."""

    __tablename__ = "pixly"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Text,
                           nullable=False)
    # TODO: metadata

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by
        }