"""
Database models for the civic waste-reporting platform.

We use SQLAlchemy (an ORM) so each row in the database is represented
as a Python object. This keeps the code readable and means we never
write raw SQL strings by hand for ordinary operations.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# One shared SQLAlchemy instance, initialised against the app in app.py.
db = SQLAlchemy()

# The fixed set of categories a report can have. Keeping this in one
# place means the form, the filter view and the (future) ML classifier
# all agree on the same list.
CATEGORIES = [
    "Fly-tipping",
    "Overflowing bin",
    "Litter",
    "Graffiti",
    "Broken glass",
    "Other",
]

# The lifecycle a report moves through once submitted.
STATUSES = ["New", "In progress", "Resolved"]


class Report(db.Model):
    """A single waste issue reported by a resident."""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Geospatial fields: every report is a point on the map.
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(20), nullable=False, default="New")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Serialise a report to plain data for the map's JSON endpoint."""
        return {
            "id": self.id,
            "category": self.category,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }
