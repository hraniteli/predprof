from datetime import datetime
from main import db
from model import Data, user_akes, Akes, User


def data_wrapper(func):
    def wrapper(sn, message, date=None):
        now = datetime.now()
        if isinstance(func(sn, message), str):
            return func(sn, message)
        if date == 'day':
            return func(sn, message, date).filter(now.replace(
                hour=0, minute=0, second=0, microsecond=0) < Data.t_start).filter(Data.t_start < now).all()
        if date == 'week':
            return func(sn, message, date).filter(now.replace(
                day=datetime.now().day - 7, hour=0, minute=0, second=0, microsecond=0) < Data.t_start).filter(
                Data.t_start < datetime.now()).all()
        return func(sn, message).all()

    return wrapper


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


@data_wrapper
def get_data(sn, message, date=None):
    if Akes.query.filter_by(sn=sn).first() is None:
        return 'Нет АКЭС'
    user = User.query.get(message.chat.id)
    users_akes = user.akes
    if sn in [akes.sn for akes in users_akes] or user.admin:
        return Data.query.filter(sn == sn).filter(Data.ef != -1)
    return 'Нет доступа'


def check_user_exist(uid):
    if User.query.filter_by(uid=uid).first() is None:
        return False
    return True


def check_user_admin(uid):
    if check_user_exist(uid):
        if User.query.filter_by(uid=uid).first().admin == 1:
            return True
        return False


def add_user_in_db(uid, admin=False):
    if User.query.filter(User.uid == uid).scalar() is None:
        user = User(uid=uid, admin=admin)
        db.session.add(user)
        db.session.commit()
    else:
        return 0


def add_user_to_akes(uid, sn):
    if User.query.filter(User.uid == uid).scalar() is None:
        return 1
    if Akes.query.get(sn) is None:
        return -1
    if sn in [akes.sn for akes in User.query.filter_by(uid=uid).first().akes]:
        return 0
    else:
        db.session.execute(user_akes.insert(), params={'user_uid': uid, 'akes_sn': sn})
        db.session.commit()


def del_user_from_akes(uid, sn):
    if Akes.query.get(sn) is None:
        return -1
    if sn not in [akes.sn for akes in User.query.filter_by(uid=uid).first().akes]:
        return 0
    else:
        db.session.execute(user_akes.delete(), params={'user_uid': uid, 'akes_sn': sn})
        db.session.commit()


def check_akes(sn):
    if Akes.query.get(sn) is None:
        return False
    return True
