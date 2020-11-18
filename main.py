from datetime import date

from flask import Flask, request ,render_template
import flask_mysqldb
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root@1234'
app.config['MYSQL_DB'] = 'employeemanagementcasestudy'
mysql = flask_mysqldb.MySQL(app)


def extractAge(age):

    input_dob = age.split('-')
    input_doy = int(input_dob[0])
    input_dom = int(input_dob[1])
    input_dod = int(input_dob[2])

    today_date = str(date.today())
    list_today_date = today_date.split('-')
    this_year = int(list_today_date[0])
    this_month = int(list_today_date[1])
    this_day = int(list_today_date[2])

    diff = this_year - input_doy

    if this_month < input_dom:

        diff = diff - 1

    elif this_month == input_dom:

        if this_day < input_dod:

            diff = diff-1

    return diff

@app.route('/searchemployee.html', methods = ["GET", "POST"])
def searchemployee():

    if request.method == 'GET' :
        result = ""
        return render_template('allemployees.html' , result = result)

    elif request.method == 'POST' :

        searchType = request.form.get("empSea")
        searchText = request.form.get("searchtext")
        if searchType == "empId":

            emp_id = searchText

            try:

                cur= mysql.connection.cursor()
                cur.execute('SELECT * FROM `employeetable` WHERE `employ_id` = %s', (emp_id,))
                data = cur.fetchall()

                length = len(data)

                if len(data) == 0:

                    result = "No such records found..."
                    return render_template('allemployees.html', length = length , result=result, status=0)

                else:

                    result =  "Search results for employee id: " +emp_id

                    cur.close()

                    return render_template('allemployees.html', data=data, length = length , result=result, status=1)

            except Exception as e:

                print(e)
                result = "System has encountered some error, please try again later!"
                return render_template('allemployees.html', data=data, length = length ,result=result, status=0)


        elif searchType == "empNam":

            emp_name = searchText

            try:

                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM `employeetable` WHERE LOWER(`ename`) LIKE %s', (emp_name.lower()+"%",))
                data = cur.fetchall()

                length = len(data)

                if len(data) == 0:
                    result = "No such records found..."
                    return render_template('allemployees.html', length=length, result=result, status=0)
                else:

                    result = "Search results for employee name: " + emp_name
                    return render_template('allemployees.html', length=length, data=data, result=result, status=1)

                cur.close()



            except Exception as e:

                print(e)
                result = "System has encountered some error, please try again later!"
                return render_template('allemployees.html', length=length, result=result , status = 0)


        elif searchType == "empAge":

            age = searchText

            try:

                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM `employeetable`', )
                empList = cur.fetchall()

                # print("\n\nYour Results.... \n\n")

                data = []

                for emp in empList:


                    if extractAge(str(emp[2])) == int(age):

                        data.append(emp)

                length = len(data)

                if len(data) == 0:

                    result = "No such records found..."
                    return render_template('allemployees.html', length=length, result=result,status = 0)


                else:

                    result =  "Search results for age: " + age

                    return render_template('allemployees.html', data=data, length=length, result=result, status=1)

                cur.close()



            except Exception as e:

                print(e)
                result = "System has encountered some error, please try again later!"
                return render_template('allemployees.html', length=length, result=result , status = 0)


@app.route('/deleteemployee.html', methods = ["GET","POST"])
def deleteemployee():

    if request.method == 'GET' :
        result = ""
        return render_template('deleteemployee.html' , result = result)

    elif request.method == 'POST' :

        emp_id = request.form.get("empID")

        result = ""

        try:

            cur = mysql.connection.cursor()

            cur.execute('SELECT * FROM `employeetable` WHERE `employ_id` = %s', (emp_id,))
            empList = cur.fetchall()

            if len(empList) == 0:

                result = "No such record found"
                status = 0

            else:

                query = "DELETE FROM `employeetable` WHERE `employ_id` = %s"
                param = (emp_id,)
                cur.execute(query, param)

                mysql.connection.commit()

                #print("\n\n\nStatus : Deletion Successful")

                result = "Employee record deleted successfully!"
                status = 1

        except Exception as e:

            print(e)
            result = "System has encountered some error, please try again later!"
            mysql.connection.rollback()
            status =0

        cur.close()

        return render_template('deleteemployee.html', result = result , status = status)






@app.route('/updateemployee.html/', methods = ["GET","POST"])
def updateemployee():
    cur = mysql.connection.cursor()
    empid = request.args.get("empid")
    if empid:
        print(empid)
        try :
            cmd = "select * from employeetable where employ_id = {empid} ".format(empid=empid)
            print(cmd)
            cur.execute( cmd)
            data = cur.fetchone()
            print(data)
            return render_template('updateemployee.html',data=data,result="")
        except Exception as e:
            print(e)
    if request.method == 'POST':
        print(request.form)
        empID = request.form.get('empId')
        email = request.form.get('empEmail')
        dob = request.form.get('empDob')
        mob = request.form.get('empNum')
        adr = request.form.get('empAdd')
        ename = request.form.get('empName')

        try:
            cur.execute(
                "update employeeTable set  edob = %s ,ename = %s ,email = %s ,mob =%s ,adress = %s where employ_id =%s",(dob, ename, email, mob, adr,empID))
            mysql.connection.commit()
            result = "Employee Updated Succefully!"
            try:
                cur.execute('select * from employeetable')
                data = cur.fetchall()
                return  render_template('allemployees.html' , data=data, result= result , status = 1)
            except Exception as e:
                print(e)

        except Exception as e:
            print('error')
            print(e)




@app.route('/')
@app.route('/allemployees.html',methods = ['GET' , 'POST'])
def all_employee():
    cur = mysql.connection.cursor()
    try :
        cur.execute('select * from employeetable')
        data = cur.fetchall()
        return render_template('allemployees.html', data=data )
    except Exception as e:
        print (e)
    return render_template('allemployees.html',update = "SERVER ERROR" , status = 0)




@app.route('/addemployee.html',methods = ['GET','POST'])
def addemployee():
    cur = mysql.connection.cursor()
    result = ""
    if request.method == 'POST' :
        print(request.form)
        empID = request.form.get('empId')
        email = request.form.get('empEmail')
        dob = request.form.get('empDob')
        mob = request.form.get('empNum')
        adr = request.form.get('empAdd')
        ename = request.form.get('empName')


        try :
            cur.execute(
                "INSERT INTO employeeTable ( employ_id  , edob , ename , email ,mob, adress  ) VALUES (%s,%s,%s,%s,%s,%s)",
                (empID, dob, ename, email, mob, adr))
            mysql.connection.commit()
            result = "Employee added Succefully!"
            try:
                cur.execute('select * from employeetable')
                data = cur.fetchall()
                return  render_template('allemployees.html' , data=data, result= result ,  status = 1)
            except Exception as e:
                print(e)
        except MySQLdb._exceptions.IntegrityError :
            result = "Employee Id already Exist , Please use different employee ID"
            return render_template('addemployee.html', result=result, status=0)


    if request.method == 'GET' :
        result = ""

    return render_template('addemployee.html' , result = result )

if __name__ == '__main__' :
    app.run()

