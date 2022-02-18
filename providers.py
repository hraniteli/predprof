from main import db
from model import *
from datetime import datetime


def add_data(sn, t_start, t_stop, cos_a, cos_b, cos_c, p_a, p_b,
             p_c, q_a, q_b, q_c, ef):
    try:
        if db.session.query(Akes.sn).filter_by(sn=sn).scalar() is None:
            akes = Akes(sn=sn)
            db.session.add(akes)
            db.session.flush()

        data = Data(sn=sn, t_start=t_start, t_stop=t_stop, cos_a=cos_a, cos_b=cos_b, cos_c=cos_c, p_a=p_a, p_b=p_b,
                    p_c=p_c,
                    q_a=q_a, q_b=q_b, q_c=q_c, ef=ef)
        db.session.add(data)
        db.session.flush()
        db.session.commit()
    except Exception as ex:
        print(ex)
        db.session.rollback()


def get_data(date):
    now = datetime.now()
    if date == 'day':
        return Data.query.filter(now.replace(hour=0, minute=0, second=0,
                                             microsecond=0) < Data.t_start).filter(Data.t_start < now).all()
    return Data.query.filter(datetime.now().replace(day=datetime.now().day - 7, hour=0, minute=0, second=0,
                                                    microsecond=0) < Data.t_start).filter(
        Data.t_start < datetime.now()).all()


def add_user_in_db(uid):
    if User.query.filter(User.uid == uid).scalar() is None:
        user = User(uid=uid, admin=False)
        db.session.add(user)
        db.session.commit()
    else:
        return 0


def add_user_to_akes(uid, sn):
    if Akes.query.filter_by(sn=sn).scalar() is None:
        return -1
    if sn in [akes.sn for akes in User.query.filter_by(uid=uid).first().akes]:
        return 0
    else:
        db.session.execute(user_akes.insert(), params={'user_uid': uid, 'akes_sn': sn})
