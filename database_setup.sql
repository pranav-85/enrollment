CREATE DATABASE Enrollment;

USE Enrollment;

CREATE TABLE user (
    user_id VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(100)
);


CREATE TABLE student (
    student_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    email_id VARCHAR(100),
    advisor_id VARCHAR(50),
    admin_id VARCHAR(50),
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id)
);


CREATE TABLE advisor (
    advisor_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    email_id VARCHAR(100)
);


CREATE TABLE admin (
    admin_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    email_id VARCHAR(100)
);


CREATE TABLE document (
    Document_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    document BLOB,
    status VARCHAR(100),
    semester VARCHAR(100),
    Comments VARCHAR(200),
    Student_ID VARCHAR(50),
    Advisor_ID VARCHAR(50),
    Admin_ID VARCHAR(50),
    FOREIGN KEY (Student_ID) REFERENCES student(student_id),
    FOREIGN KEY (Advisor_ID) REFERENCES advisor(advisor_id),
    FOREIGN KEY (Admin_ID) REFERENCES admin(admin_id)
);


CREATE TABLE enrollment (
    Enrollment_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    semester VARCHAR(100),
    Status VARCHAR(100),
    Comments VARCHAR(100),
    Student_ID VARCHAR(50),
    FOREIGN KEY (Student_ID) REFERENCES student(student_id)
);


CREATE TABLE verification (
    Verification_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    semester VARCHAR(100),
    Status VARCHAR(100),
    Comments VARCHAR(100),
    Student_ID VARCHAR(50),
    FOREIGN KEY (Student_ID) REFERENCES student(student_id)
);


CREATE TABLE Notification (
    Notification_ID INT AUTO_INCREMENT PRIMARY KEY,
    student_ID VARCHAR(50),
    sender_ID VARCHAR(50),
    date_sent DATE,
    message VARCHAR(200),
    read_status VARCHAR(100),
    FOREIGN KEY (student_ID) REFERENCES student(student_id)
);

