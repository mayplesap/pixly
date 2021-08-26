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
    category = db.Column(db.Text)
    uploaded_by = db.Column(db.Text,
                           nullable=False)
    img_link = db.Column(db.Text,
                         nullable=False)
    # TODO: metadata

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "uploaded_by": self.uploaded_by,
            "img_link": self.img_link
        }