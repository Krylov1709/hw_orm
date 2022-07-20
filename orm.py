import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pprint import pprint
import json

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")
    
class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)
 
class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Открываем файл для заполнения таблиц
with open ("tests_data.json") as open_file:
    load_table = json.load(open_file)

# pprint (load_table)    

user = ''
password = ''
name_db = ''

engine = sqlalchemy.create_engine(f'postgresql://{user}:{password}@localhost:5432/{name_db}')

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Заполняем таблицы данными из файла
for data in load_table:
    if data['model'] == 'publisher':
        session.add(Publisher(name=data['fields']['name']))
        session.commit()
    elif data['model'] == 'book':
        session.add(Book(title=data['fields']['title'],
                         id_publisher=data['fields']['id_publisher']))
        session.commit()
    elif data['model'] == 'shop':
        session.add(Shop(name=data['fields']['name']))
        session.commit()
    elif data['model'] == 'stock':
        session.add(Stock(count=data['fields']['count'],
                          id_book=data['fields']['id_book'],
                          id_shop=data['fields']['id_shop']))
        session.commit()
    elif data['model'] == 'sale':
        session.add(Sale(price=data['fields']['price'],
                        id_stock=data['fields']['id_stock'],
                        date_sale=data['fields']['date_sale'],
                        count=data['fields']['count']))
        session.commit()

number = input(f'Введите ID автора: ')
for i in session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == number).all():
    print(i.name)

session.close()

