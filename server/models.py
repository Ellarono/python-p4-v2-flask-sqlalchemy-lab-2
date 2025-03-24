from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Establish a relationship with the Review model
    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reviews": [review.to_dict_basic() for review in self.reviews],
            "items": [
                {"id": item.id, "name": item.name} for item in self.items if item
            ]
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Establish a relationship with the Review model
    reviews = db.relationship('Review', back_populates='item')
    customers = association_proxy('reviews', 'customer')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "reviews": [review.to_dict_basic() for review in self.reviews],
            "customers": [
                {"id": customer.id, "name": customer.name} for customer in self.customers if customer
            ]
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def to_dict(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "customer": self.customer.to_dict_basic() if self.customer else None,
            "item": self.item.to_dict_basic() if self.item else None
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "comment": self.comment
        }

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

# Utility methods `to_dict_basic` are added for lightweight representations when nested serialization is needed.
