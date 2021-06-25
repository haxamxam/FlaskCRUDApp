from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html");


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                query = cur.execute("INSERT into Employees (name, email, address) values (?,?,?)", (name, email, address))
                print(query.arraysize)
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/updatedetails", methods=["POST", "GET"])
def updateDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["old_name"]
            new_name = request.form["new_name"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("update Employees set name = (?) where name = (?) ", (new_name, name))
                con.commit()
                msg = "Employee successfully Updated"
        except:
            con.rollback()
            msg = "We can not Update the employee to the list"
        finally:
            cur.execute("SELECT * FROM Employees WHERE name=?", (new_name,))
            rows = cur.fetchall()
            return render_template("updatesuccess.html", msg=msg, rows=rows)
            con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)