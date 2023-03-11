import configparser
import os.path

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import sqlalchemy


def get_data():
    config = configparser.ConfigParser()
    dirname = os.path.dirname(__file__)
    path = dirname + '/setting.ini'
    config.read(path)
    name_user = config['DATABASE']['USER']
    password = config['DATABASE']['PASSWORD']
    name_db = config['DATABASE']['NAME_DB']
    token_vk = config['DATABASE']['TOKEN_VK']
    return name_user, password, name_db, token_vk


Base = declarative_base()

DSN = f'postgresql://{get_data()[0]}:{get_data()[1]}@localhost:5432/{get_data()[2]}'
engine = sqlalchemy.create_engine(DSN)


class User(Base):
    __tablename__ = "users"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.Text, unique=True, nullable=False)


class Favorit(Base):
    __tablename__ = "favorites"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    name = sq.Column(sq.String(length=40), nullable=False)
    surname = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.Text, unique=True, nullable=False)
    photo = sq.Column(sq.Text, unique=True, nullable=False)
    user = relationship(User, backref="favorites")


class Black_list(Base):
    __tablename__ = "black_list"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable=False)
    vk_id = sq.Column(sq.Text, unique=True, nullable=False)
    user = relationship(User, backref="black_list")

def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)



def add_user(name, link, engine=engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    check_user = session.query(User).filter(User.link == link)
    if session.query(check_user.exists()).scalar() == False:
        user = User(name=name, link=link)

        session.add(user)
        session.commit()


    session.close()




if __name__ == '__main__':
    create_tables(engine)
    # drop_tables(engine)
    # add_user('Павел', 'https://vk.com/559261802')
