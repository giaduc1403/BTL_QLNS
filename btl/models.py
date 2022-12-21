from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from btl import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Sách giáo khoa')
        # c2 = Category(name='Truyện tranh')
        # c3 = Category(name='Sách lịch sử')
        #
        # # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # p1 = Product(name='Sách giáo khoa lớp 12', description='Sách giáo khoa, lớp 12', price=240000,
        #              image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015422-1.jpg',
        #              category_id=1)
        # p2 = Product(name='Sách giáo khoa lớp 11', description='Sách giáo khoa, lớp 11', price=340000,
        #              image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015415-1.jpg',
        #              category_id=1)
        # p3 = Product(name='Sách tham khảo học tốt Văn 11', description='Văn, lớp 11', price=48000,
        #              image='https://cdn0.fahasa.com/media/catalog/product/i/m/image_237828.jpg',
        #              category_id=2)
        # p4 = Product(name='Sách giáo khoa lớp 10', description='Sách giáo khoa lớp 10', price=280000,
        #              image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015392-1.jpg',
        #              category_id=1)
        # p5 = Product(name='Học tốt Hóa', description='Hóa, lớp 11', price=32000,
        #              image='https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_49050.jpg',
        #              category_id=2)
        #
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='giaduc', username='giaduc14', password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://haycafe.vn/wp-content/uploads/2021/11/Anh-avatar-dep-chat-lam-hinh-dai-dien.jpg')
        # db.session.add(u)
        # db.session.commit()
        #
        # c1 = Comment(content='Good', user_id=1, product_id=1)
        # c2 = Comment(content='Nice', user_id=1, product_id=1)
        # db.session.add_all([c1, c2])
        # db.session.commit()