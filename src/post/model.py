from src import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    imgLink = db.Column(db.String(255), nullable=False)
    unixTime = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    __table_args__ = (
        db.Index('posts_unixTime_idx', unixTime.desc()),
    )
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}