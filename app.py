from flask import Flask, render_template, jsonify
import MySQLdb

class ReimbursementApp:
    def __init__(self, db_config):
        # 1. Initialize Flask app and set up database connection
        self.app = Flask(__name__)
        self.db = MySQLdb.connect(
            host=db_config['host'],
            user=db_config['user'],
            passwd=db_config['passwd'],
            db=db_config['db']
        )
        self.cursor = self.db.cursor()

        # 2. Define routes
        self.setup_routes()

    def setup_routes(self):
        # Route for the home page
        @self.app.route('/')
        def index():
            return render_template('index.html')

        # Route to get data from the database and return it as JSON
        @self.app.route('/data')
        def data():
            query = """
            SELECT 
                r.Nomor AS No_Reimburse,           # Reimbursement number
                rd.Tanggal,                        # Date of the reimbursement
                r.Nama_Karyawan AS Nama,           # Name of the employee
                r.Status,                          # Status of the reimbursement (reject/accept)
                p.Nomor AS Project,                # Project number
                p.Customer,                        # Customer name
                rd.Keterangan,                     # Description of the expense
                rd.Jumlah                          # Amount of the reimbursement
            FROM 
                Tabel_Reimburse_Detail rd           # Reimbursement detail table
            JOIN 
                Tabel_Reimburse r ON rd.Reimburse_Id = r.Id  # Join with reimbursement table
            JOIN 
                Tabel_Project p ON rd.Project_Id = p.Id;     # Join with project table
            """
            self.cursor.execute(query)  # Execute the SQL query
            results = self.cursor.fetchall()  # Fetch all the results from the executed query
            return jsonify(results)  # Return the results as a JSON response

    def run(self, debug=True):
        # Run the Flask application
        self.app.run(debug=debug)

if __name__ == '__main__':
    # Configuration for the database connection
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'passwd': '',
        'db': 'reimbursements'
    }

    # Create an instance of the ReimbursementApp class and run the app
    app = ReimbursementApp(db_config)
    app.run(debug=True)
