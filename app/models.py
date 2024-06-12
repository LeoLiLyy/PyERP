from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    EmployeeID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=True)
    Dept = db.Column(db.String(30), nullable=True)
    Email = db.Column(db.String(30), unique=True, nullable=False)
    Password = db.Column(db.String(90), nullable=False)
    session_token = db.Column(db.String(100), nullable=True)


class Inventory(db.Model):
    ItemID = db.Column(db.Integer, primary_key=True)
    I_Name = db.Column(db.String(20), nullable=True)
    I_Disc = db.Column(db.String(500), nullable=True)
    InDate = db.Column(db.String(10), nullable=True)
    OutDate = db.Column(db.String(10), nullable=True)
    Warehouse_Num = db.Column(db.Integer, nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)


class Project(db.Model):
    ProjectID = db.Column(db.Integer, primary_key=True)
    P_Name = db.Column(db.String(20), nullable=True)
    P_Disc = db.Column(db.String(500), nullable=True)
    Deadline = db.Column(db.String(10), nullable=True)
    Products = db.Column(db.String(500), nullable=True)
    Customer = db.Column(db.String(100), nullable=True)


class Design(db.Model):
    DesignID = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    design_details = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.ProjectID'), nullable=False)
    file_path = db.Column(db.String(200), nullable=True)
    project = db.relationship('Project', backref=db.backref('designs', lazy=True))