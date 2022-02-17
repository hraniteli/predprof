from main import db
from model import *


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