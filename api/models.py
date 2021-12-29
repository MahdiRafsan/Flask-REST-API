from api import db


class User(db.Model):
    """
    create a database table for users
    """
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    todo = db.relationship("ToDo", backref="user", lazy=True)

    def __repr__(self):
        return "User({}, {}, {})".format(self.name, self.public_id, self.admin)

class ToDo(db.Model):
    """
    create a database table to store todo items 
    """
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "Todo({}, {})".format(self.item, self.complete)
