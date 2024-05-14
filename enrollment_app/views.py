from django.shortcuts import render
from django.contrib import messages
from .models import Student, Advisor, Admin
from datetime import datetime
import MySQLdb

def home(request):
    return render(request, 'login.html')

def CurrentSem():
    current_sem = ''
    year = datetime.now().year
    month = datetime.now().month
    if month == 12:
        year+=1
        current_sem += 'JAN-MAY ' + str(year)
    else:
        current_sem += 'JUL-NOV ' + str(year)
    
    return current_sem
def login(request):
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            cursor = db.cursor()

            user_id = request.POST.get("RollNumber")
            password = request.POST.get("Password")

            query = "SELECT * FROM user WHERE user_id = %s;"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user and user[1] == password:

                query_student = "SELECT * FROM student WHERE student_id = %s;"
                cursor.execute(query_student, (user_id,))
                student_data = cursor.fetchone()

                query_advisor = "SELECT * FROM advisor WHERE advisor_id = %s;"
                cursor.execute(query_advisor, (user_id,))
                advisor_data = cursor.fetchone()

                query_admin = "SELECT * FROM admin WHERE admin_id = %s;"
                cursor.execute(query_admin, (user_id,))
                admin_data = cursor.fetchone()

                if student_data:
                    student = Student()
                    student.RollNumber=user_id
                    student.Name=student_data[1]
                    student.CurrentSemester= CurrentSem()
                    student.RegStatus='File not submitted'
                    
                    return render(request, 'enroll.html', {'student': student})
                elif advisor_data:
                    advisor = Advisor()
                    advisor.Advisor_ID=user_id
                    advisor.Name=advisor_data[1]
                    
                    return render(request, 'adv.html', {'advisor': advisor})
                elif admin_data:
                    admin = Admin()
                    admin.Admin_ID=user_id
                    admin.Name=admin_data[1]
                    
                    return render(request, 'adm.html', {'admin': admin})
            else:
                messages.error(request, 'Invalid username or password')
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()

    return render(request, 'login.html')



def enroll(request):
    student = Student()
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            cursor = db.cursor()
            user_id = request.POST.get("user_id")
            file = request.FILES.get("pdf_file")

            if file:
                file_content = file.read()
                
                query_student = f"SELECT * FROM student WHERE student_id = '{user_id}';"
                cursor.execute(query_student)
                student_data = cursor.fetchone()

                query_insert = "INSERT INTO Document(document, status, semester, Comments, Student_ID, Advisor_ID, Admin_ID) VALUES (%s, 'File Submitted', %s, '', %s, %s, %s);"
                cursor.execute(query_insert, (file_content, CurrentSem(), user_id, student_data[3], student_data[4]))
                db.commit()

                query_insert_enrollment = "INSERT INTO Enrollment(semester, Status, Comments, Student_ID) VALUES (%s,'Yet to be Approved', '', %s);"
                cursor.execute(query_insert_enrollment, (CurrentSem(),user_id,))
                db.commit()

            student.RollNumber = user_id
            student.Name = student_data[1]
            student.CurrentSemester = CurrentSem()
            student.RegStatus = 'File Submitted, Yet to be Approved'
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()

    return render(request, 'enroll.html', {'student': student})
