from app import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Filename {}>'.format(self.filename)
