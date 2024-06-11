# app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db


class Employee(UserMixin, db.Model):
    __tablename__ = 'employee'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=True)
    Dept = db.Column(db.String(30), nullable=True)
    Email = db.Column(db.String(30), unique=True, nullable=True)
    Password = db.Column(db.String(90), nullable=True)
    session_token = db.Column(db.String(100), nullable=True)

    def get_id(self):
        return str(self.EmployeeID)


# model for inventory
class Inventory(db.Model):
    __tablename__ = 'inventory'
    ItemID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    I_Name = db.Column(db.String(20), nullable=True)
    I_Disc = db.Column(db.String(500), nullable=True)
    InDate = db.Column(db.String(10), nullable=True)
    OutDate = db.Column(db.String(10), nullable=True)
    Warehouse_Num = db.Column(db.Integer, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)

    def get_id(self):
        return str(self.ItemID)


class Project(db.Model):
    ProjectID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    P_Name = db.Column(db.String(100), nullable=False)
    P_Disc = db.Column(db.String(500), nullable=True)
    Deadline = db.Column(db.String(10), nullable=True)
    Products = db.Column(db.String(500), nullable=True)
    Customer = db.Column(db.String(500), nullable=True)

    def get_id(self):
        return str(self.ProjectID)


class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    design_details = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=True)

    def get_id(self):
        return str(self.id)
