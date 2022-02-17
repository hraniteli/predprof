from main import db


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer(), primary_key=True)
    sn = db.Column(db.Integer(), db.ForeignKey('akes.sn'), nullable=False)
    t_start = db.Column(db.DateTime(), nullable=False)
    t_stop = db.Column(db.DateTime(), nullable=False)
    cos_a = db.Column(db.Float(), nullable=False)
    cos_b = db.Column(db.Float(), nullable=False)
    cos_c = db.Column(db.Float(), nullable=False)
    p_a = db.Column(db.Float(), nullable=False)
    p_b = db.Column(db.Float(), nullable=False)
    p_c = db.Column(db.Float(), nullable=False)
    q_a = db.Column(db.Float(), nullable=False)
    q_b = db.Column(db.Float(), nullable=False)
    q_c = db.Column(db.Float(), nullable=False)
    ef = db.Column(db.Float(), nullable=False)


user_akes = db.Table('user_akes',
                     db.Column('user_uid', db.Integer, db.ForeignKey('users.uid')),
                     db.Column('akes_sn', db.Integer, db.ForeignKey('akes.sn'))
                     )


class Akes(db.Model):
    __tablename__ = 'akes'
    sn = db.Column(db.Integer(), primary_key=True)
    user_uid = db.relationship('User', secondary=user_akes, backref='akes')
    data = db.relationship('Data', backref='akes')


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer(), primary_key=True)
    admin = db.Column(db.Boolean(), nullable=False)


if len(db.engine.table_names()) == 0:
    db.create_all()
