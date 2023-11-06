from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask import Flask, render_template, request, send_file
from flask import Flask, render_template, request, flash, send_file
import sqlite3
from matrix2 import run, write, missing, read
from matrix import run, write, find_allocated_room
from flask import render_template
import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/About")
def about():
    return render_template("aboutus.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        if email == "admin@gmail.com" and password == "admin":
            return redirect(url_for('admin'))
        else:
            error = "INVALID DETAILS"
    return render_template("login.html", error=error)


@app.route("/student_login", methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        roll_number = request.form['rollNumber']

    return render_template("student_login.html", error=error)


@app.route("/login-success")
def login_success():
    return "Login Successful!"


@app.route("/faculty_login", methods=['GET', 'POST'])
def faculty_login():
    error = None
    if request.method == 'POST':
        faculty_name = request.form['facultyName']
        faculty_department = request.form['facultyDepartment']

        # Here, you can add code to validate faculty credentials or check them against a database.
        # If they are valid, you can perform any necessary actions.
        # For simplicity, let's assume faculty login is successful.
        # Store the faculty name in the session
        session['faculty_name'] = faculty_name
        return redirect(url_for('faculty_allocation'))

    return render_template("faculty_login.html", error=error)


@app.route('/faculty_allocation')
def faculty_allocation():
    faculty_name = session.get('faculty_name')
    if faculty_name:
        try:
            myconn = sqlite3.connect("room_details.db")
            with myconn:
                cursor = myconn.cursor()
                cursor.execute(
                    "SELECT room FROM faculty WHERE name = ?", (faculty_name,))
                allocated_room = cursor.fetchone()
                if allocated_room:
                    room_number = allocated_room[0]
                    return f"Welcome, {faculty_name}! You are allocated to room {room_number}"
                else:
                    return "You are not allocated to any room."
        except sqlite3.Error as e:
            # Handle SQLite exceptions
            flash(f"Database error: {str(e)}", "error")

    return "Faculty not logged in or allocation information not found."


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
def admin():
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
        data = cursor.execute("SELECT * FROM room")
        data = cursor.fetchall()
    return render_template("admin.html", data=data)


@app.route("/addroom", methods=['GET', 'POST'])
def addroom():
    data = None
    error = None
    if request.method == 'POST':
        room_no = request.form['room_no']
        row = request.form['row']
        col = request.form['col']
        seat = request.form['seat']
        block_name = request.form['block_name']  # New block name field

        print(f"Trying to add room {room_no} in block {block_name}")

        myconn = sqlite3.connect("room_details.db")
        if int(seat) <= int(row) * int(col):
            with myconn:
                cursor = myconn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
                temp_room = cursor.execute(
                    "SELECT room_no from room where room_no=? AND block_name=?", [room_no, block_name])
                temp_room = cursor.fetchone()

            print(f"temp_room: {temp_room}")

            if temp_room is None:
                with myconn:
                    cursor = myconn.cursor()
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
                    cursor.execute("INSERT INTO room VALUES(?,?,?,?,?)", [
                                   room_no, col, row, seat, block_name])
                    error = f"Room {room_no} in block {block_name} is added"
            else:
                error = f"Room {room_no} in block {block_name} already exists"
        else:
            error = "Invalid number of seat"

        print(f"Error: {error}")
    return render_template("addroom.html", error=error, data=data)

# ... (other routes)
# ... (previous code)


@app.route("/Generate", methods=['GET', 'POST'])
def generate():
    error = None
    myconn = sqlite3.connect("room_details.db")

    with myconn:
        cursor = myconn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
        room_data_rows = cursor.execute("SELECT room_no, block_name FROM room")
        room_data = room_data_rows.fetchall()

        selected_room = None  # Initialize selected_room
        selected_room_no = None  # Initialize selected_room_no
        selected_block_name = None
    if request.method == 'POST':
        # Retrieve the selected room number and block name as a single value (e.g., "304 cse")
        selected_room = request.form['room']
        # Split the selected value into room number and block name
        selected_room_parts = selected_room.split()
        if len(selected_room_parts) == 2:
            selected_room_no, selected_block_name = selected_room_parts
        it_start = request.form['it_start']
        it_end = request.form['it_end']
        ec_start = request.form['ec_start']
        ec_end = request.form['ec_end']
        el_start = request.form['el_start']
        el_end = request.form['el_end']
        r_missing = request.form['missing']

        with myconn:
            cursor = myconn.cursor()
            row = cursor.execute(
                "SELECT row FROM room WHERE room_no = ?", [selected_room_no])
            row = cursor.fetchone()
            row = row[0]
            col = cursor.execute(
                "SELECT col FROM room WHERE room_no = ?", [selected_room_no])
            col = cursor.fetchone()
            col = col[0]
            seat = cursor.execute(
                "SELECT seat FROM room WHERE room_no = ?", [selected_room_no])
            seat = cursor.fetchone()
            seat = seat[0]

        it_start = int(it_start)
        it_end = int(it_end)
        ec_start = int(ec_start)
        ec_end = int(ec_end)
        el_start = int(el_start)
        el_end = int(el_end)
        r_missing = r_missing.split()
        for i in range(len(r_missing)):
            r_missing[i] = int(r_missing[i])

        it_list = list(range(it_start, it_end + 1))
        it_list = missing(r_missing, it_list)
        ec_list = list(range(ec_start, ec_end + 1))
        ec_list = missing(r_missing, ec_list)
        el_list = list(range(el_start, el_end + 1))
        el_list = missing(r_missing, el_list)

        check = len(el_list) + len(ec_list) + len(it_list)

        if check <= int(seat):
            data = run(el_list, ec_list, it_list, row, col, selected_room)
            write(data, selected_room_no)
            error = "Seating Arrangement For " + selected_room_no + " Is generated"
        else:
            error = "Total Number of students is not more than " + \
                str(seat) + " " + str(check)

    return render_template("generate.html", room_data=room_data, selected_room_no=selected_room_no, selected_block_name=selected_block_name, error=error)


@app.route('/result', methods=['GET', 'POST'])
def show():
    data = None
    filename = None
    error = None
    myconn = sqlite3.connect("room_details.db")

    with myconn:
        cursor = myconn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
        room_data_rows = cursor.execute("SELECT room_no, block_name FROM room")
        room_data = room_data_rows.fetchall()

        selected_room = None  # Initialize selected_room
        selected_room_no = None  # Initialize selected_room_no
        selected_block_name = None

    if request.method == 'POST':
        # Retrieve the selected room number and block name as a single value (e.g., "304 cse")
        selected_room = request.form['room']
        # Split the selected value into room number and block name
        selected_room_parts = selected_room.split()
        if len(selected_room_parts) == 2:
            selected_room_no, selected_block_name = selected_room_parts
        data = read(selected_room_no)
        data = data.to_html()
        filename = '/static/execl/' + selected_room_no + '.xlsx'

    return render_template("show_result.html", data=data, room_data=room_data, selected_room_no=selected_room_no, selected_block_name=selected_block_name, error=error, filename=filename)


@app.route('/delete/<int:id1>/<string:id2>')
def delete(id1, id2):
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
        cursor.execute(
            "DELETE FROM room WHERE room_no=? AND block_name=?", (id1, id2))
    return redirect(url_for('admin'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    error = None
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        data = cursor.execute("SELECT * FROM room WHERE room_no = ?", [id])
        data = cursor.fetchmany()
    room_no = data[0][0]
    col = data[0][1]
    row = data[0][2]
    seat = data[0][3]
    block_name = data[0][4]

    if request.method == 'POST':
        new_room_no = request.form['room_no']
        new_row = request.form['row']
        new_col = request.form['col']
        new_seat = request.form['seat']
        new_block_name = request.form['block_name']

        if int(new_seat) <= int(new_row) * int(new_col):
            with myconn:
                cursor = myconn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
                cursor.execute("UPDATE room SET room_no=?, col=?, row=?, seat=?, block_name=? WHERE room_no=?",
                               [new_room_no, new_col, new_row, new_seat, new_block_name, id])
                error = "Room details updated"
        else:
            error = "Invalid number of seat"

    return render_template("addroom.html", error=error, room=room_no, col=col, row=row, seat=seat, block_name=block_name)


@app.route('/faculty', methods=['GET', 'POST'])
def faculty():
    error = None
    room_data = []

    try:
        myconn = sqlite3.connect("room_details.db")

        with myconn:
            cursor = myconn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS faculty(name text, department text, room text)")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS room(room_no integer(10), col integer(10), row integer(10), seat integer(10), block_name text)")
            room_data_rows = cursor.execute(
                "SELECT room_no, block_name FROM room")
            room_data = room_data_rows.fetchall()

        if request.method == 'POST':
            print(request.form, "form data")
            faculty_name = request.form['faculty_name']
            department = request.form['department']  # Get the department
            room_number = request.form['room']  # Get the room number
            print(room_number)
            # Fetch the block_name of the selected room
            with myconn:
                cursor = myconn.cursor()
                cursor.execute(
                    "SELECT block_name FROM room WHERE room_no = ?", (room_number,))
                room_block = cursor.fetchone()
                if room_block:
                    block_name = room_block[0]
                else:
                    block_name = ""

            # Concatenate the room number and block_name
            room_department = f"{room_number}"

            with myconn:
                cursor = myconn.cursor()
                cursor.execute("INSERT INTO faculty (name, department, room) VALUES (?, ?, ?)", [
                               faculty_name, department, room_department])
                error = f"{faculty_name} is added"
    except sqlite3.Error as e:
        # Handle any SQLite exceptions here
        error = f"Database error: {str(e)}"
    finally:
        # Close the database connection after all operations
        if myconn:
            myconn.close()

    return render_template("faculty.html", error=error, room_data=room_data)

    #     if request.method == 'POST':
    #        faculty_name = request.form['faculty_name']
    #        department = request.form['department']
    #        room = request.form['room']  # Get the room

    # # Concatenate the room and department
    #        room_department = f"{room} {department}"

    #     with myconn:
    #        cursor = myconn.cursor()
    #        cursor.execute("INSERT INTO faculty (name, department, room) VALUES (?, ?, ?)", [faculty_name, department, room_department])
    #        error = f"{faculty_name} is added"

    # except sqlite3.Error as e:
    #     # Handle any SQLite exceptions here
    #     error = f"Database error: {str(e)}"
    # finally:
    #     # Close the database connection after all operations
    #     if myconn:
    #         myconn.close()

    # return render_template("faculty.html", error=error, room_data=room_data, faculty_name="", department="")
    #     if request.method == 'POST':
    #         faculty_name = request.form['faculty_name']
    #         department = request.form['department']
    #         room = request.form['room']  # Get the room

    #         # Concatenate the room and department
    #         room_department = f"{room} {department}"

    #         with myconn:
    #             cursor = myconn.cursor()
    #             cursor.execute("INSERT INTO faculty (name, department, room) VALUES (?, ?, ?)", [faculty_name, department, room_department])
    #             error = f"{faculty_name} is added"
    # except sqlite3.Error as e:
    #     # Handle any SQLite exceptions here
    #     error = f"Database error: {str(e)}"
    # finally:
    #     # Close the database connection after all operations
    #     if myconn:
    #         myconn.close()

    # return render_template("faculty.html", error=error, room_data=room_data, faculty_name=faculty_name, department="")


# ... (other imports and code) ...


# ... (other route functions) ...


# ... (other route functions) ...


# ... (other route functions)
# ... (your existing imports and code)


@app.route('/faculty_reports')
def faculty_reports():
    try:
        myconn = sqlite3.connect("room_details.db")
        with myconn:
            cursor = myconn.cursor()
            cursor.execute("SELECT name, department, room, rowid FROM faculty")
            faculty_data = cursor.fetchall()
            # Add this line to check data retrieval
            print("Fetched faculty data:", faculty_data)
    except sqlite3.Error as e:
        # Handle SQLite exceptions
        flash(f"Database error: {str(e)}", "error")
        faculty_data = []
        print(faculty_data)

    return render_template("faculty_reports.html", faculty_data=faculty_data)


# ... (other routes and code)
@app.route('/delete_faculty', methods=['POST'])
def delete_faculty():
    faculty_id = request.form.get('faculty_id')

    try:
        myconn = sqlite3.connect("room_details.db")
        with myconn:
            cursor = myconn.cursor()
            cursor.execute("DELETE FROM faculty WHERE rowid=?", [faculty_id])
            flash("Faculty record deleted successfully", "success")
    except sqlite3.Error as e:
        # Handle SQLite exceptions
        flash(f"Failed to delete faculty record: {str(e)}", "error")

    return redirect(url_for('faculty_reports'))

# ... (other routes and code)


# ... (your existing imports and code)

@app.route('/download_excel', methods=['POST'])
def download_excel():
    try:
        myconn = sqlite3.connect("room_details.db")
        with myconn:
            cursor = myconn.cursor()
            cursor.execute("SELECT name, department, room FROM faculty")
            faculty_data = cursor.fetchall()

        excel_file_path = generate_excel_file(faculty_data)
        return send_file(excel_file_path, as_attachment=True, download_name='faculty_report.xlsx')
    except sqlite3.Error as e:
        # Handle SQLite exceptions
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for('faculty_reports'))

# ... (your other route functions)


# ... (other routes and code) ...
@app.route('/download/<filename>')
def download_file(filename):
    # ... (your existing code to handle file download) ...
    return send_file(filepath, as_attachment=True)

# ... (rest of your code)


# ... (your existing imports and code)

def generate_excel_file(faculty_data):
    # Define the directory where you want to save the Excel file
    directory = 'static/excel/'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    excel_file_path = os.path.join(directory, 'faculty_report.xlsx')

    # Rest of your code remains the same
    df = pd.DataFrame(faculty_data, columns=[
                      'Faculty Name', 'Department', 'Room'])
    df.to_excel(excel_file_path, index=False, engine='xlsxwriter')
    return excel_file_path


if __name__ == "__main__":
    app.run(debug=True)
