from app import db, create_app
from app.models import Employee, Inventory, Project, Design
from sqlalchemy import inspect, text

# Create the Flask application context
app = create_app()
app.app_context().push()


# Function to apply database updates without deleting data
def update_database():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    with app.app_context():
        if 'employee' not in tables:
            db.create_all()
        else:
            # Check if the session_token column exists in the employee table
            columns = [column['name'] for column in inspector.get_columns('employee')]
            if 'session_token' not in columns:
                db.session.execute(text('''
                    ALTER TABLE employee ADD COLUMN session_token VARCHAR(100);
                '''))
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS inventory (
                    ItemID INT AUTO_INCREMENT PRIMARY KEY,
                    I_Name VARCHAR(20) NULL,
                    I_Disc VARCHAR(500) NULL,
                    InDate VARCHAR(10) NULL,
                    OutDate VARCHAR(10) NULL,
                    Warehouse_Num INT NULL,
                    Quantity INT NULL
                );
            '''))
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS project (
                    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
                    P_Name VARCHAR(20) NULL,
                    P_Disc VARCHAR(500) NULL,
                    Deadline VARCHAR(10) NULL,
                    Products VARCHAR(500) NULL,
                    Customer VARCHAR(100) NULL
                );
            '''))
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS design (
                    DesignID INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    design_details TEXT NULL,
                    project_id INT NOT NULL,
                    file_path VARCHAR(200) NULL,
                    FOREIGN KEY (project_id) REFERENCES project(ProjectID)
                );
            '''))
            db.session.commit()

if __name__ == "__main__":
    update_database()
    print("Database updated successfully!")