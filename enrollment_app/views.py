from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student, Advisor, Admin, StudentDoc
from datetime import datetime
import os
from django.conf import settings
import MySQLdb

def home(request):
    return render(request, 'login.html')

def redirect_to_media(request, path):
    return redirect(settings.MEDIA_URL + path)

def save_blob_as_pdf(blob_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        file.write(blob_data)
        
def LoadAdvisorData(user_id):
    db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
    cursor = db.cursor()
    query_advisor = "SELECT * FROM advisor WHERE advisor_id = %s;"
    cursor.execute(query_advisor, (user_id,))
    advisor_data = cursor.fetchone()
                    
    student_adv_query = f"SELECT D.document, S.name, S.student_id FROM student S, document D, Enrollment E WHERE S.advisor_id = '{user_id}' AND S.student_id = D.student_ID AND D.advisor_ID = '{user_id}' AND D.semester = '{CurrentSem()}' AND E.Student_ID = S.student_ID AND E.status = 'Yet to be Approved';"
    cursor.execute(student_adv_query)
    studentDoc_data = cursor.fetchall()
    student_submitted = []
                    
    for data in studentDoc_data:
        studentDoc = StudentDoc()
        studentDoc.Name = data[1]
        studentDoc.ID = data[2]
        save_blob_as_pdf(bytes(data[0]), f'uploads/{data[2]}.pdf')
        studentDoc.Document = f'{data[2]}.pdf'
        student_submitted.append(studentDoc)
                
    student_adv_query = f"SELECT D.document, S.name, S.student_id FROM student S, document D, Enrollment E WHERE S.advisor_id = '{user_id}' AND S.student_id = D.student_ID AND D.advisor_ID = '{user_id}' AND D.semester = '{CurrentSem()}' AND E.Student_ID = S.student_ID AND E.status = 'Approved';"
    cursor.execute(student_adv_query)
    studentDoc_data = cursor.fetchall()
    student_approved = []

    for data in studentDoc_data:
        studentDoc = StudentDoc()
        studentDoc.Name = data[1]
        studentDoc.ID = data[2]
        save_blob_as_pdf(bytes(data[0]), f'uploads/{data[2]}.pdf')
        studentDoc.Document = f'{data[2]}.pdf'
        student_approved.append(studentDoc)

    student_adv_query = f"SELECT S.name, S.student_id FROM Student S, document D WHERE S.advisor_id = '{user_id}' AND S.student_id NOT IN (SELECT D.student_ID FROM Document D WHERE D.semester = '{CurrentSem()}' AND D.advisor_ID = '{user_id}');"
    cursor.execute(student_adv_query)
    studentDoc_data = cursor.fetchall()
    student_no_doc = []
                    
    for data in studentDoc_data:
        student = Student()
        student.Name = data[0]
        student.RollNumber = data[1]
        student_no_doc.append(student)
    return [student_submitted, student_approved, student_no_doc]

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

def student_dashboard(request):
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            user_id = request.GET.get('user_id')
            cursor = db.cursor()
            query_student = "SELECT * FROM student WHERE student_id = %s;"
            cursor.execute(query_student, (user_id,))
            student_data = cursor.fetchone()

            student = Student()
            student.RollNumber=user_id
            student.Name=student_data[1]
            student.CurrentSemester= CurrentSem()
            student.RegStatus='File not submitted'
                
            return render(request, 'enroll.html', {'student': student})
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()

def advisor_dashboard(request):
    if request.method == 'GET':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            cursor = db.cursor()
            user_id = request.GET.get('user_id')
            query_advisor = "SELECT * FROM advisor WHERE advisor_id = %s;"
            print(user_id)
            cursor.execute(query_advisor, (user_id,))
            advisor_data = cursor.fetchone()
            advisor = Advisor()
            advisor.Advisor_ID=user_id
            advisor.Name=advisor_data[1]
                    
            data = LoadAdvisorData(user_id)

            return render(request, 'advisor_dashboard.html', {'advisor': advisor, 'student_submitted': data[0], 'student_approved' : data[1], 'student_no_doc':data[2]})
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()

def admin_dashboard(request):
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            cursor = db.cursor()
            user_id = request.GET.get('user_id')

            query_admin = "SELECT * FROM admin WHERE admin_id = %s;"
            cursor.execute(query_admin, (user_id,))
            admin_data = cursor.fetchone()

            admin = Admin()
            admin.Admin_ID=user_id
            admin.Name=admin_data[1]

            return render(request, 'admin_dashboard.html',  {'admin': admin})
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()
    


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
                    return HttpResponseRedirect(f'/student/dashboard/?user_id={user_id}')
                
                elif advisor_data:
                    return HttpResponseRedirect(f'/advisor/dashboard/?user_id={user_id}')

                elif admin_data:
                    return HttpResponseRedirect(f'/admin/dashboard/?user_id={user_id}')
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


def advisor_approve(request):
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(
                host="localhost",
                user='root',
                password='Pr@navmysql',
                database='Enrollment'
            )
            cursor = db.cursor()
            student_id = request.POST.get("student_id")
            advisor_id = request.POST.get("advisor_id")

            query_advisor = "SELECT * FROM advisor WHERE advisor_id = %s;"
            cursor.execute(query_advisor, (advisor_id,))
            advisor_data = cursor.fetchone()

            advisor = Advisor()
            advisor.Advisor_ID=advisor_id
            advisor.Name=advisor_data[1]
            
            update_query = f"UPDATE Enrollment SET status = 'Approved' WHERE student_ID = '{student_id}' AND semester = '{CurrentSem()}';"
            cursor.execute(update_query)
            db.commit()

            data = LoadAdvisorData(advisor_id)
            return redirect(reverse('advisor_dashboard') + f'?user_id={advisor_id}')  
            
        except MySQLdb.Error as e:
            messages.error(request, f'MySQL Error: {e}')
        finally:
            cursor.close()
            db.close()
    
    return redirect('login')
    
        

    