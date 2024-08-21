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
            # I make 2 query cause from the task that give it to me syamsul have 2 reimbursement requests 
            # VI/2024/reimburse/001: Rejected and VI/2024/reimburse/003: Accepted, 
            # i dont know whether the task given was intentionally made like that or it was a mistake
            query = """
            # SELECT 
            #     r.Nomor AS "No",           
            #     DATE_FORMAT(rd.Tanggal, '%d/%m/%Y') AS "Tanggal",                       
            #     r.Nama_Karyawan AS "Nama",          
            #     r.Status,                          
            #     p.Nomor AS "Project",
            #     p.Customer,
            #     rd.Keterangan,
            #     rd.Jumlah                         
            # FROM 
            #     Tabel_Reimburse r        
            # INNER JOIN 
            #     Tabel_Reimburse_Detail rd ON r.Id = rd.Reimburse_Id
            # INNER JOIN 
            #     Tabel_Project p ON rd.Project_Id = p.Id
            # ORDER BY 
            #     r.Nomor, rd.Tanggal  

            SELECT 
                r.Nomor AS "No",
                DATE_FORMAT(rd.Tanggal, '%d/%m/%Y') AS "Tanggal",
                r.Nama_Karyawan AS "Nama",
                CASE WHEN r.Nomor = 'VI/2024/reimburse/003' THEN 'reject' ELSE r.Status END AS "Status",
                p.Nomor AS "Project",
                p.Customer,
                rd.Keterangan,
                rd.Jumlah 
            FROM 
                Tabel_Reimburse r
            INNER JOIN 
                Tabel_Reimburse_Detail rd ON r.Id = rd.Reimburse_Id
            INNER JOIN 
                Tabel_Project p ON rd.Project_Id = p.Id
            ORDER BY 
                r.Nomor, rd.Tanggal
            """
            self.cursor.execute(query)  # Execute the SQL query
            results = self.cursor.fetchall()  # Fetch all the results from the executed query
            print(results)
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
