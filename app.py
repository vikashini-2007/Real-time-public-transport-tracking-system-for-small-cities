from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Vikashini@1989",   # change this
        database="bus_tracking"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("login.html")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Login ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# ---------------- ADD ROUTE ----------------
@app.route('/add_route', methods=['GET', 'POST'])
def add_route():

    if request.method == 'POST':

        source = request.form.get('source')
        destination = request.form.get('destination')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO routes(source,destination) VALUES(%s,%s)",
            (source, destination)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("dashboard.html")

    return render_template("add_route.html")


# ---------------- ADD BUS ----------------
@app.route('/add_bus', methods=['GET', 'POST'])
def add_bus():

    if request.method == 'POST':

        bus_number = request.form.get('bus_number')
        driver_name = request.form.get('driver_name')
        route_id = request.form.get('route_id')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO buses
            (bus_number,driver_name,route_id)
            VALUES(%s,%s,%s)
            """,
            (bus_number, driver_name, route_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("dashboard.html")

    return render_template("add_bus.html")


# ---------------- VIEW BUSES ----------------
@app.route('/buses')
def buses():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        bus_number,
        driver_name,
        latitude,
        longitude
        FROM buses
        """
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "buses.html",
        buses=data
    )


# ---------------- SEARCH BUS ----------------
@app.route('/search_bus', methods=['GET', 'POST'])
def search_bus():

    bus = None

    if request.method == 'POST':

        bus_number = request.form.get('bus_number')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            bus_number,
            driver_name,
            latitude,
            longitude
            FROM buses
            WHERE bus_number=%s
            """,
            (bus_number,)
        )

        bus = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template(
        "search_bus.html",
        bus=bus
    )


# ---------------- BUS DETAILS ----------------
@app.route('/bus_details', methods=['GET', 'POST'])
def bus_details():

    bus = None

    if request.method == 'POST':

        bus_number = request.form.get('bus_number')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            buses.bus_number,
            buses.driver_name,
            routes.source,
            routes.destination,
            buses.latitude,
            buses.longitude
            FROM buses
            JOIN routes
            ON buses.route_id = routes.route_id
            WHERE buses.bus_number=%s
            """,
            (bus_number,)
        )

        bus = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template(
        "bus_details.html",
        bus=bus
    )


# ---------------- UPDATE LOCATION ----------------
@app.route('/update_location', methods=['GET', 'POST'])
def update_location():

    if request.method == 'POST':

        bus_number = request.form.get('bus_number')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE buses
            SET latitude=%s,
                longitude=%s
            WHERE bus_number=%s
            """,
            (latitude, longitude, bus_number)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return "Location Updated Successfully ✅"

    return render_template("update_location.html")


# ---------------- MAP ----------------
@app.route('/map')
def map_page():
    return render_template("map.html")


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)