from tkinter.messagebox import askyesno
import datetime
import customtkinter
import mysql.connector
from tkinter import *
from tkinter import messagebox
import tkinter as tK
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
from dateutil.relativedelta import relativedelta

"""
LOAN MANAGEMENT SYSTEM
=====================

Available Functions:
------------------

1. Authentication & User Management:
   - sigin(): Handle user login
   - register(): Display registration form
   - registerdb(): Create new user account
   
2. Document Handling:
   - view_image(photo): Display uploaded image
   - converttobinary(filename): Convert file to binary
   - convertbtof(binarydata): Convert binary to file
   
3. File Upload Functions:
   - get_fileadar(): Upload Aadhar card
   - get_filepan(): Upload PAN card
   - get_filepassbook(): Upload bank passbook
   - get_filedoc1/2/3/4(): Upload additional documents
   - get_fileuser_photo(): Upload user photo
   
4. Document View Functions:
   - view_adarfile(): View Aadhar card
   - view_panfile(): View PAN card
   - view_passbookfile(): View passbook
   - view_doc1/2/3/4file(): View additional documents
   - view_user_photofile(): View user photo
   
5. Loan Processing:
   - penalty_checker(): Check and calculate penalties
   - fill_rec_details(): Create loan application form
   - fill_rec_details_db(): Save loan application
   - load_loan_sch(): Load loan schemes
   - adding_to_database(): Submit loan application
   
6. Admin Operations:
   - admin_page(): Display admin dashboard
   - update_company(): Update company details
   - edit_comp(): Edit company information
   - loandetails(): Display loan schemes
   - view_new_users(): Display new applications
   - view_active_users(): Display active loans
   - view_history(): Display transaction history
   
7. Loan Scheme Management:
   - load_sch_tb(): Load loan schemes table
   - add_sch_db(): Add new loan scheme
   - add_schemes(): Create loan scheme form
   - update_sch_db(): Update loan scheme
   - upd_schemes(): Edit loan scheme form
   - delete_sch_db(): Delete loan scheme
   
8. User Interface:
   - on_enterpho(e): Handle phone field focus
   - on_leavepho(e): Handle phone field blur
   - on_enterpass(e): Handle password field focus
   - on_leavepass(e): Handle password field blur
   
9. Navigation:
   - start(): Initialize application
   - exitfunc(): Exit application
   - go_back_to_admin(): Return to admin page
   - go_back_to_userpage(): Return to user page
   
10. Table Management:
    - view_new_user_table(): Load new applications table
    - view_active_user_table(): Load active loans table
    - pay_histry_table_load(): Load payment history table
"""

# Admin credentials - Can be moved to database or environment variables for production
ADMIN_USERNAME = "1"  # Change this for production
ADMIN_PASSWORD = "1"  # Change this for production
# Note: For better security, store admin credentials in database:
# CREATE TABLE admin_credentials (username VARCHAR(100), password VARCHAR(255));
# INSERT INTO admin_credentials VALUES ('admin', 'hashed_password');

# Database connection
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    port='3306',
    database='finance_for_need',
)

# Initialize main window
root = Tk()
root.title('Login')
root.geometry('1535x780')
root.configure(bg="#fff")
frame = frame1 = 0
img1 = 0

s = ttk.Style(root)
s.theme_use("clam")


###################################### for image view
def view_image(photo):
    global image_window

    image_window = Toplevel()
    image = Image.open(photo)
    resize_image = image.resize((1000, 600))
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image_window, image=img)
    label1.image = img
    label1.pack()


def converttobinary(filename):
    try:
        with open(filename, "rb") as file:
            binarydata = file.read()
        return binarydata
    except:
        return filename


def convertbtof(binarydata):
    try:
        file1='photo1.png'
        with open(file1, "wb") as file:
            file.write(binarydata)
        return file1
    except:
        messagebox.showerror("Invalid", "No Document Found")
        return -1


def penalty_checker():
    cur = con.cursor()
    query = """select * from customer where not customer_name = 'refrence'"""
    cur.execute(query, )
    myresult = cur.fetchall()
    result = list(myresult)
    for i in range(len(myresult)):
        date = datetime.date.today()
        last_pay_date = result[i][18]
        check_date = last_pay_date + relativedelta(months=1)

        if (check_date < date):
            emi = result[i][10]
            penalty = result[i][14] / 12
            if penalty > 0:
                extra_pay = int(float(emi) * float(penalty) * 0.01)
                principal = result[i][4] + extra_pay
                tenur_in_months = result[i][9]
                interest = result[i][12]
                total_amount = result[i][5]
                total_amount = total_amount + extra_pay
                remaining_amount = result[i][6]
                remaining_amount += extra_pay
                loan_end_date = result[i][16]
                last_pay_date = check_date

                r_of_int = interest / 12 / 100
                emi = principal * r_of_int * (
                        (pow((1 + r_of_int), tenur_in_months)) / ((pow((1 + r_of_int), tenur_in_months)) - 1))
                emi = int(emi)

                cur = con.cursor()
                query = '''update customer set  principal_amount = %s, total_amount = %s, remaining_amount = %s, 
                loan_end_date = %s, last_pay_date = %s, EMI = %s where customer_mobie = %s and customer_name = %s '''
                cur.execute(query, (
                    principal, total_amount, remaining_amount, loan_end_date, check_date, emi, result[i][2],
                    result[i][1]))
                con.commit()




######################################## for pdf view


def sigin():
    userpho1 = loginphone1.get()
    password1 = loginpassword.get()
    if (userpho1 != "" and password1 != ""):

        cur = con.cursor()
        query = """select * from users Where userphone1 = %s and password = %s"""
        cur.execute(query, (userpho1, password1))
        myresult = temp = cur.fetchone()

        if userpho1 == ADMIN_USERNAME and password1 == ADMIN_PASSWORD:  # Using predefined constants
            messagebox.showinfo("Success", "Login Success")
            admin_page()

        elif myresult != None:
            userfirstpage(myresult[1], myresult[3])
        else:
            messagebox.showerror("Invalid", "invalid username and password")
    else:
        messagebox.showerror("Invalid", "Enter all the required details")


################################# user Frame


def fill_rec_details_db(name, phone1, val, fathername, intfather_phone, mothername, intmother_phone,
                        longadar_number, adar_photo1, pannumber
                        , pan_photo1, intfamily_income, email, permanentaddress, officeadress,
                        intpincode, rec_amount, no_of_years,
                        ibank_acc_number, bankifsc, passbook_photo1, user_photo1, doc11, doc21, doc31, doc41):
    cur = con.cursor()
    query = '''UPDATE users set loanscheme = %s, fathername = %s, userphone2 = %s, mothername = %s, motherphonenumber = 
    %s, adharnumber = %s, adharcardphoto = %s, pannumber = %s, pancardphoto = %s, familyincome = %s, useremail = %s, 
    useraddress1 = %s, useraddress2 = %s, pincode = %s, amountrec = %s, tenure = %s, bankaccnumber = 
    %s, bankifsc = %s, passbookphoto = %s, photo = %s, doc1 = %s, doc2 = %s, doc3 = %s, doc4 = %s, submitdate = %s  where username = %s and 
    userphone1 = %s '''
    adar_photo1 = converttobinary(adar_photo1)
    pan_photo1 = converttobinary(pan_photo1)
    user_photo1 = converttobinary(user_photo1)
    passbook_photo1 = converttobinary(passbook_photo1)
    if doc11 != 0:
        doc11 = converttobinary(doc11)
    if doc21 != 0:
        doc21 = converttobinary(doc21)
    if doc31 != 0:
        doc31 = converttobinary(doc31)
    if doc11 != 0:
        doc41 = converttobinary(doc41)

    date = datetime.datetime.now()

    cur.execute(query, (
        val, fathername, intfather_phone, mothername, intmother_phone, longadar_number, adar_photo1, pannumber,
        pan_photo1,
        intfamily_income, email, permanentaddress, officeadress, intpincode, rec_amount, no_of_years, ibank_acc_number,
        bankifsc, passbook_photo1, user_photo1, doc11, doc21, doc31, doc41, date, name, phone1))
    con.commit()

    messagebox.showinfo("Success", "Application Submitted ")
    userfirstpage(name, phone1)


adar_photo, pan_photo, passbook_photo, doc1, doc2, doc3, doc4, user_photo = 0, 0, 0, 0, 0, 0, 0, 0


def fill_rec_details(name, phone1, val):
    global adar_photo, pan_photo, passbook_photo, doc1, doc2, doc3, doc4, user_photo
    adar_photo, pan_photo, passbook_photo, doc1, doc2, doc3, doc4, user_photo = 0, 0, 0, 0, 0, 0, 0, 0

    def userfirstpage1():
        userfirstpage(name, phone1)

    def get_fileadar():
        global adar_photo
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        adar_photo = filedialog.askopenfilename(filetypes=f_types)

    def view_adarfile():
        global adar_photo
        if adar_photo != 0:
            view_image(adar_photo)
        else:
            messagebox.showerror("Invalid", "Upload the Aadhar First")

    def get_filepan():
        global pan_photo
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        pan_photo = filedialog.askopenfilename(filetypes=f_types)

    def view_panfile():
        global pan_photo
        if pan_photo != 0:
            view_image(pan_photo)
        else:
            messagebox.showerror("Invalid", "Upload the Pan First")

    def get_filepassbook():
        global passbook_photo
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        passbook_photo = filedialog.askopenfilename(filetypes=f_types)

    def view_passbookfile():
        global passbook_photo
        if passbook_photo != 0:
            view_image(passbook_photo)
        else:
            messagebox.showerror("Invalid", "Upload the Income Certificate First")

    def get_filedoc1():
        global doc1
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        doc1 = filedialog.askopenfilename(filetypes=f_types)

    def view_doc1file():
        global doc1
        if doc1 != 0:
            view_image(doc1)
        else:
            messagebox.showerror("Invalid", "Upload the Document First")

    def get_filedoc2():
        global doc2
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        doc2 = filedialog.askopenfilename(filetypes=f_types)

    def view_doc2file():
        global doc2
        if doc2 != 0:
            view_image(doc2)
        else:
            messagebox.showerror("Invalid", "Upload the Document First")

    def get_filedoc3():
        global doc3
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        doc3 = filedialog.askopenfilename(filetypes=f_types)

    def view_doc3file():
        global doc3
        if doc3 != 0:
            view_image(doc3)
        else:
            messagebox.showerror("Invalid", "Upload the Document First")

    def get_filedoc4():
        global doc4
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        doc4 = filedialog.askopenfilename(filetypes=f_types)

    def view_doc4file():
        global doc4
        if doc4 != 0:
            view_image(doc4)
        else:
            messagebox.showerror("Invalid", "Upload the Document First")

    def get_fileuser_photo():
        global user_photo
        f_types = [('Jpg files ', '.jpg'), ('PNG files ', '.png')]
        user_photo = filedialog.askopenfilename(filetypes=f_types)

    def view_user_photofile():
        global user_photo
        if user_photo != 0:
            view_image(user_photo)
        else:
            messagebox.showerror("Invalid", "Upload the Photo First")

    def adding_to_database():
        global adar_photo, pan_photo, passbook_photo, doc1, doc2, doc3, doc4, user_photo
        fathername = father_name.get()
        mothername = mother_name.get()
        fatherphone = father_phone.get()
        motherphone = mother_phone.get()
        adarnumber = adar_number.get()
        pannumber = pan_number.get()
        familyincome = family_income.get()
        email = email_user.get()
        permanentaddress = perm_address.get(1.0, "end-1c")
        officeadress = office_address.get(1.0, "end-1c")
        pincodeval = pincode.get()
        rec_amount = amount_rec.get()
        no_of_years = tenure.get()
        bankaccnumber = bank_acc_number.get()
        bankifsc = bank_ifsc.get()

        if (fathername != "" and mothername != "" and len(motherphone) == 10 and pannumber != "" and len(
                fatherphone) == 10 and adar_photo != 0 and pan_photo != 0 and email != ""
                and permanentaddress != "" and officeadress != "" and pincodeval != "" and rec_amount != "" and bankaccnumber != ""
                and bankifsc != "" and passbook_photo != 0 and len(adarnumber) == 16 and len(pannumber) == 10):
            try:

                intfather_phone = int(fatherphone)
                intmother_phone = int(motherphone)
                longadar_number = int(adarnumber)
                intfamily_income = int(familyincome)
                intpincode = int(pincodeval)
                ibank_acc_number = int(bankaccnumber)
                rec_amount = int(rec_amount)
                no_of_years = int(no_of_years)

                check = askyesno("Conform", "Do you want to Submit the Form : ")
                if (check):
                    fill_rec_details_db(name, phone1, val, fathername, intfather_phone, mothername, intmother_phone,
                                        longadar_number, adar_photo, pannumber
                                        , pan_photo, intfamily_income, email, permanentaddress, officeadress,
                                        intpincode, rec_amount, no_of_years,
                                        ibank_acc_number, bankifsc, passbook_photo, user_photo, doc1, doc2, doc3, doc4)

            except:
                messagebox.showerror("Invalid", "Enter proper numerical Values")
        else:
            messagebox.showerror("Invalid", "Enter proper and Complete detail")

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)
    Label(frame, text='Fill the required details for ' + val, fg='Green', bg='white', border=1,
          font=('times new roman', 20, 'bold')).place(x=550, y=20)

    customtkinter.CTkButton(frame, width=120, height=40, text='Back', font=('times new roman', 15),
                            command=userfirstpage1).place(x=1385, y=10)

    Label(frame, text='Father Name : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=100)
    father_name = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    father_name.place(x=350, y=100)

    Label(frame, text='Mother Name : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=150)
    mother_name = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    mother_name.place(x=350, y=150)

    Label(frame, text='Father Phone : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=200)
    father_phone = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    father_phone.place(x=350, y=200)

    Label(frame, text='Mother Phone : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=250)
    mother_phone = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    mother_phone.place(x=350, y=250)

    Label(frame, text='Aadhar Number : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=300)
    adar_number = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    adar_number.place(x=350, y=300)

    Label(frame, text='Upload Aadhar : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=350)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_fileadar).place(x=400, y=350)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_adarfile).place(x=510, y=350)

    Label(frame, text='PAN Number : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=400)
    pan_number = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    pan_number.place(x=350, y=400)

    Label(frame, text='Upload PAN : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filepan).place(x=400, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_panfile).place(x=510, y=450)

    Label(frame, text='Family Income(in Numbers): ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=500)
    family_income = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    family_income.place(x=350, y=500)

    Label(frame, text='Email : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=550)
    email_user = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    email_user.place(x=350, y=550)

    Label(frame, text='Permanent Address : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=600)
    perm_address = tK.Text(frame, width=30, height=4, fg='black', border=1, bg="white",
                           font=('times new roman', 13))
    perm_address.place(x=350, y=600)

    Label(frame, text='Upload Your Photo : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_fileuser_photo).place(x=400, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_user_photofile).place(x=510, y=700)

    Label(frame, text='Office Address : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=100)
    office_address = tK.Text(frame, width=30, height=4, fg='black', border=1, bg="white",
                             font=('times new roman', 13))
    office_address.place(x=1050, y=100)

    Label(frame, text='Pincode : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=200)
    pincode = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    pincode.place(x=1050, y=200)

    Label(frame, text='Amount Required : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=250)
    amount_rec = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    amount_rec.place(x=1050, y=250)

    Label(frame, text='No of Years : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=300)
    tenure = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    tenure.place(x=1050, y=300)

    Label(frame, text='Bank Account number : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=350)
    bank_acc_number = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    bank_acc_number.place(x=1050, y=350)

    Label(frame, text='Bank IFSC code : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=400)
    bank_ifsc = Entry(frame, width=30, fg='black', border=1, bg="white", font=('times new roman', 13))
    bank_ifsc.place(x=1050, y=400)

    Label(frame, text='Upload Bank Passbook : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filepassbook).place(x=1100, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_passbookfile).place(x=1210, y=450)

    Label(frame, text='Upload Remaining Documents : (Optional)', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=500)

    Label(frame, text='Documents 1 : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=550)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filedoc1).place(x=1100, y=550)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc1file).place(x=1210, y=550)

    Label(frame, text='Documents 2 : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=600)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filedoc2).place(x=1100, y=600)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc2file).place(x=1210, y=600)

    Label(frame, text='Documents 3 : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=650)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filedoc3).place(x=1100, y=650)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc3file).place(x=1210, y=650)

    Label(frame, text='Documents 4 : ', fg='blue', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='Upload', font=('times new roman', 15),
                            command=get_filedoc4).place(x=1100, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc4file).place(x=1210, y=700)

    customtkinter.CTkButton(frame, width=120, height=40, text='SUBMIT', font=('times new roman', 15),
                            command=adding_to_database).place(x=1385, y=70)


def load_loan_sch(name, phone1, val):
    global frame

    def fill_rec_details1():
        fill_rec_details(name, phone1, val)

    if val != "Select":
        cur = con.cursor()
        query = "select * from loan WHERE name = %s "
        cur.execute(query, (val,))
        myresult = cur.fetchone()

        temp_am = str(myresult[2])
        Label(frame, text='MAX AMOUNT    : ' + temp_am, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=150, y=400)

        temp_NA = str(myresult[1])
        Label(frame, text='LOAN NAME   : ' + temp_NA, fg='green', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=600, y=250)

        temp_intrate = str(myresult[3])
        Label(frame, text='INTEREST RATE   : ' + temp_intrate, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=150, y=450)

        temp_inttype = str(myresult[4])
        Label(frame, text='INTEREST TYPE   : ' + temp_inttype, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=150, y=500)

        temp_loantenue = str(myresult[5])
        Label(frame, text='LOAN TENURE                  : ' + temp_loantenue, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=700, y=400)

        temp_prepayment = str(myresult[6])
        Label(frame, text='PRE PAYMENT PENALTY     : ' + temp_prepayment, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=700, y=450)

        temp_latepayemntint = str(myresult[7])
        Label(frame, text='LATE PAYMENT INTEREST   : ' + temp_latepayemntint, fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=700, y=500)

        temp_recdocment = str(myresult[8])
        Label(frame, text='DOCUMENTS REQUIRED   :', fg='blue', bg='white', border=1,
              font=('times new roman', 25, 'bold')).place(x=150, y=600)
        goals_val = Message(frame, text=temp_recdocment, width=500, fg='blue', bg='white',
                            font=('times new roman', 25, "bold"))
        goals_val.place(x=600, y=595)
        customtkinter.CTkButton(frame, width=120, height=40, text='Proceed', font=('times new roman', 15),
                                command=fill_rec_details1).place(
            x=1300, y=650)

    else:
        messagebox.showerror("Invalid", "PLEASE SELECT THE LOAN REQUIRED")


def view_users_details(name, phone1):
    phone = phone1
    username = name
    cur = con.cursor()
    query = '''select * from users where userphone1 = %s and username = %s'''
    cur.execute(query, (phone, username))
    myresult = cur.fetchone()

    def view_adarfile():
        view_image(convertbtof(myresult[12]))

    def view_panfile():
        view_image(convertbtof(myresult[11]))

    def view_passbookfile():
        view_image(convertbtof(myresult[21]))

    def view_doc1file():
        if convertbtof(myresult[22]) != -1:
            view_image(convertbtof(myresult[22]))

    def view_doc2file():
        if convertbtof(myresult[23]) != -1:
            view_image(convertbtof(myresult[23]))

    def view_doc3file():
        if convertbtof(myresult[24]) != -1:
            view_image(convertbtof(myresult[24]))

    def view_doc4file():
        if convertbtof(myresult[25]) != -1:
            view_image(convertbtof(myresult[25]))

    def view_user_photofile():
        view_image(convertbtof(myresult[10]))

    def go_back_to_userpage():
        userfirstpage(name, phone1)

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)
    Label(frame, text='Complete Details of User ' + myresult[1], fg='Green', bg='white', border=1,
          font=('times new roman', 20, 'bold')).place(x=550, y=20)

    customtkinter.CTkButton(frame, width=120, height=40, text='Back', font=('times new roman', 15),
                            command=go_back_to_userpage).place(x=1385, y=10)

    Label(frame, text='Father Name : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=100)
    Label(frame, text=myresult[14], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=100)

    Label(frame, text='Mother Name : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=150)
    Label(frame, text=myresult[15], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=150)

    Label(frame, text='Father Phone : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=200)
    Label(frame, text=myresult[6], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=200)

    Label(frame, text='Mother Phone : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=250)
    Label(frame, text=myresult[16], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=250)

    Label(frame, text='Aadhar Number : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=300)
    Label(frame, text=myresult[8], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=300)

    Label(frame, text='Aadhar Photo: ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=350)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_adarfile).place(x=350, y=350)

    Label(frame, text='PAN Number : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=400)
    Label(frame, text=myresult[9], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=400)

    Label(frame, text='PAN Photo: ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_panfile).place(x=350, y=450)

    Label(frame, text='Family Income(in Numbers): ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=500)
    Label(frame, text=str(myresult[17]), fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=500)

    Label(frame, text='Email : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=550)
    Label(frame, text=myresult[7], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=350, y=550)

    Label(frame, text='Permanent Address : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=600)
    perm_address = Message(frame, text=myresult[4], width=500, fg='Green', bg='white',
                           font=('times new roman', 13))
    perm_address.place(x=350, y=600)

    Label(frame, text='User Photo : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=100, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_user_photofile).place(x=350, y=700)

    Label(frame, text='Office Address : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=100)
    office_address = Message(frame, text=myresult[5], width=500, fg='Green', bg='white',
                             font=('times new roman', 13))
    office_address.place(x=1050, y=100)

    Label(frame, text='Pincode : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=200)
    Label(frame, text=str(myresult[18]), fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=1050, y=200)

    Label(frame, text='Amount Required : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=250)
    Label(frame, text=str(myresult[26]), fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=1050, y=250)

    Label(frame, text='No of Years : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=300)
    Label(frame, text=str(myresult[27]), fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=1050, y=300)

    Label(frame, text='Bank Account number : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=350)
    Label(frame, text=myresult[19], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=1050, y=350)

    Label(frame, text='Bank IFSC code : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=400)
    Label(frame, text=myresult[20], fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=1050, y=400)

    Label(frame, text='Bank Passbook : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=450)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_passbookfile).place(x=1050, y=450)

    Label(frame, text='Remaining Documents : (Optional)', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=500)

    Label(frame, text='Documents 1 : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=550)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc1file).place(x=1050, y=550)

    Label(frame, text='Documents 2 : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=600)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc2file).place(x=1050, y=600)

    Label(frame, text='Documents 3 : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=650)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc3file).place(x=1050, y=650)

    Label(frame, text='Documents 4 : ', fg='Green', bg='white', border=1,
          font=('times new roman', 15, 'bold')).place(x=800, y=700)
    customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                            command=view_doc4file).place(x=1050, y=700)


def remaining_instalment_details(name, phone1, id):
    global frame

    def remaining_instalment_table_load():
        cur = con.cursor()
        query = '''select last_pay_date, remaing_tenure_number, remaining_amount, total_amount_paid, interest, 
        principal_amount from customer where customer_name = %s and customer_mobie = %s '''
        cur.execute(query, (name, phone1))
        result = cur.fetchone()

        datee = result[0]
        tenure = result[1]
        remaining_amount = result[2]
        total_amount_paid = result[3]
        interest = result[4]
        principal = result[5]
        r = interest / 12 / 100

        while (tenure > 0):
            emi = principal * r * (
                    (pow((1 + r), tenure)) / ((pow((1 + r), tenure)) - 1))
            emi = int(emi)
            intrest_paid = int(principal * r)
            princial_paid = emi - intrest_paid
            principal -= princial_paid
            datee = datee + relativedelta(months=1)
            print_date = datee.strftime("%d-%B-%Y")
            tenure -= 1
            remaining_amount -= emi
            if (tenure == 0):
                remaining_amount = 0;
            total_amount_paid += emi

            remaining_instalment_table.insert("", "end", values=(
                str(print_date), str(tenure), str(remaining_amount), str(total_amount_paid),
                str(intrest_paid), str(princial_paid), str(emi)))

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    Label(frame, text="User Name : ", fg='Green', bg='white', font=('times new roman', 30, "bold")). \
        place(x=500, y=10)
    Label(frame, text=str(name), fg='Green', bg='white', font=('times new roman', 30, "bold")). \
        place(x=750, y=10)

    ######### calculations
    def go_back_to_user():
        userfirstpage(name, phone1)

    def go_back_to_admin():
        admin_page()
        view_active_users()

    remaining_instalment_table = ttk.Treeview(frame, selectmode='browse')
    if id == 2:
        customtkinter.CTkButton(frame, width=100, height=40, text=' Back ', command=go_back_to_user).place(x=1385, y=10)
    else:
        customtkinter.CTkButton(frame, width=100, height=40, text=' Back ', command=go_back_to_admin).place(x=1385,
                                                                                                            y=10)

    remaining_instalment_table["columns"] = ("0", "1", "2", "3", "4", "5", "6",)
    remaining_instalment_table['show'] = 'headings'
    remaining_instalment_table.column("0", width=70, anchor=CENTER)
    remaining_instalment_table.column("1", width=100, anchor=CENTER)
    remaining_instalment_table.column("2", width=120, anchor=CENTER)
    remaining_instalment_table.column("3", width=120, anchor=CENTER)
    remaining_instalment_table.column("4", width=100, anchor=CENTER)
    remaining_instalment_table.column("5", width=100, anchor=CENTER)
    remaining_instalment_table.column("6", width=100, anchor=CENTER)

    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=remaining_instalment_table.yview)
    remaining_instalment_table.place(x=150, y=100, height=640, width=1170)
    scrollbarY.place(x=136, y=100, height=640)
    remaining_instalment_table.configure(yscrollcommand=scrollbarY.set)

    remaining_instalment_table.heading("0", text="Date")
    remaining_instalment_table.heading("1", text="Tenure Remaining")
    remaining_instalment_table.heading("2", text="Amount Remaining")
    remaining_instalment_table.heading("3", text="Amount Paid")
    remaining_instalment_table.heading("4", text="Interest Paid")
    remaining_instalment_table.heading("5", text="Principal Paid")
    remaining_instalment_table.heading("6", text="Total")

    for item in remaining_instalment_table.get_children():
        remaining_instalment_table.delete(item)
    remaining_instalment_table_load()


def view_pay_histroy(name, phone1, id):
    global frame

    def pay_histry_table_load():
        cur = con.cursor()
        query = '''select * from history where name = %s and phone = %s '''
        cur.execute(query, (name, phone1))
        result = cur.fetchall()
        result1 = list(result)

        for i in range(len(result)):
            remaining_instalment_table.insert("", "end",
                                              values=(
                                                  result1[i][3], result1[i][4], result1[i][5], result1[i][6],
                                                  result1[i][7], result1[i][8],
                                                  result1[i][9], result1[i][10]))

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    Label(frame, text="User Name : ", fg='Green', bg='white', font=('times new roman', 30, "bold")). \
        place(x=500, y=10)
    Label(frame, text=str(name), fg='Green', bg='white', font=('times new roman', 30, "bold")). \
        place(x=750, y=10)

    ######### calculations
    def go_back_to_user():
        userfirstpage(name, phone1)

    def go_back_to_admin():
        admin_page()
        view_active_users()

    remaining_instalment_table = ttk.Treeview(frame, selectmode='browse')
    if id == 2:
        customtkinter.CTkButton(frame, width=100, height=40, text=' Back ', command=go_back_to_user).place(
            x=1385, y=10)
    else:
        customtkinter.CTkButton(frame, width=100, height=40, text=' Back ', command=go_back_to_admin).place(
            x=1385,
            y=10)

    remaining_instalment_table["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7")
    remaining_instalment_table['show'] = 'headings'
    remaining_instalment_table.column("0", width=120, anchor=CENTER)
    remaining_instalment_table.column("1", width=100, anchor=CENTER)
    remaining_instalment_table.column("2", width=120, anchor=CENTER)
    remaining_instalment_table.column("3", width=70, anchor=CENTER)
    remaining_instalment_table.column("4", width=100, anchor=CENTER)
    remaining_instalment_table.column("5", width=100, anchor=CENTER)
    remaining_instalment_table.column("6", width=100, anchor=CENTER)
    remaining_instalment_table.column("7", width=100, anchor=CENTER)

    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=remaining_instalment_table.yview)
    remaining_instalment_table.place(x=150, y=100, height=640, width=1170)
    scrollbarY.place(x=136, y=100, height=640)
    remaining_instalment_table.configure(yscrollcommand=scrollbarY.set)

    remaining_instalment_table.heading("0", text="Loan Account Number")
    remaining_instalment_table.heading("1", text="Date Payed")
    remaining_instalment_table.heading("2", text="Loan Name")
    remaining_instalment_table.heading("3", text="EMI")
    remaining_instalment_table.heading("4", text="Principal Paid")
    remaining_instalment_table.heading("5", text="Interest Paid")
    remaining_instalment_table.heading("6", text="Remaining Amount")
    remaining_instalment_table.heading("7", text="Total Amount Paid")

    for item in remaining_instalment_table.get_children():
        remaining_instalment_table.delete(item)
    pay_histry_table_load()


def userfirstpage(name, phone1):
    root.title('User')
    global frame

    def restart_aplication():
        cur = con.cursor()
        query = "update users set status = 'NULL', userphone2 = 'NULL' WHERE username = %s AND userphone1 = %s"
        cur.execute(query, (name, phone1))
        con.commit()
        messagebox.showinfo("Success", "Your Application Restarted")
        userfirstpage(name, phone1)

    def load_loan_sch1():
        val = combx.get()
        load_loan_sch(name, phone1, val)

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    cur = con.cursor()
    query = "select userphone2, status, remark from users WHERE username = %s AND userphone1 = %s"
    cur.execute(query, (name, phone1))
    myresult1 = cur.fetchone()

    if myresult1[0] == "NULL" and myresult1[1] == "NULL":
        Label(frame, text="Well Come " + name, fg='#58a1f0', bg='white', border=1,
              font=('times new roman', 30, 'bold')).place(x=690, y=0)
        Label(frame, text="YOU DO NOT HAVE ANY LOAN ACCOUNT PLEASE FILL THE DETAILS TO CREATE ONE", fg='green',
              bg='white', border=1,
              font=('times new roman', 20, 'bold')).place(x=200, y=100)

        Label(frame, text="Select Your Loan Scheme", fg='green', bg='white',
              font=('times new roman', 20, 'bold')).place(x=50, y=200)
        cur = con.cursor()
        query = "select * from loan"
        cur.execute(query, )
        myresult = cur.fetchall()
        myresult = list(myresult)
        temp = ("Select",)
        temp2 = ()
        for i in range(len(myresult) - 1):
            # combx.insert(i+1,myresult[i][1])
            temp2 = (myresult[i][1], myresult[i + 1][1])
            i = i + 1
            temp = temp + temp2

        def delete_acc():
            check = askyesno("Conform", "Do you want to Pay : ")
            if (check):
                cur = con.cursor()
                query = '''delete from users where username = %s and userphone1 = %s'''
                cur.execute(query, (name, phone1))
                con.commit()
                messagebox.showinfo("Success", "Account Deleted Successfully")
                start()

        combx = ttk.Combobox(frame, values=temp, font=('times new roman', 15, 'bold'), state="readonly")
        combx.place(x=100, y=250)
        combx.current(0)
        customtkinter.CTkButton(frame, width=100, height=40, text='Quit', font=('times new roman', 15),
                                command=exitfunc).place(x=1380, y=10)
        customtkinter.CTkButton(frame, width=100, height=40, text='Log Out', font=('times new roman', 15),
                                command=start).place(x=1380, y=70)
        customtkinter.CTkButton(frame, width=120, height=40, text='Delete Account', font=('times new roman', 15),
                                command=delete_acc).place(x=1380, y=130)
        customtkinter.CTkButton(frame, width=100, height=40, text='Proceed', font=('times new roman', 15),
                                command=load_loan_sch1).place(x=200, y=300)

    elif myresult1[1] == "NO":

        customtkinter.CTkButton(frame, width=100, height=40, text='Quit', font=('times new roman', 15),
                                command=exitfunc).place(x=1380, y=10)
        customtkinter.CTkButton(frame, width=100, height=40, text='Log Out', font=('times new roman', 15),
                                command=start).place(x=1380, y=70)
        customtkinter.CTkButton(frame, width=100, height=40, text='RESTART APPLICATION', font=('times new roman', 30),
                                command=restart_aplication).place(x=650, y=400)

        Label(frame, text="Well Come " + name, fg='#58a1f0', bg='white', border=1,
              font=('times new roman', 30, 'bold')).place(x=690, y=0)

        Label(frame, text="YOUR APPLICATION HAS BEEN REJECTED ", fg='green', bg='white', border=1,
              font=('times new roman', 20, 'bold')).place(x=550, y=100)
        remark = Message(frame, text="Remarks : " + myresult1[2], fg='green', bg='white', border=1,
                         font=('times new roman', 20, 'bold'))
        remark.place(x=550, y=200)

    elif myresult1[1] == "YES":
        customtkinter.CTkButton(frame, width=100, height=40, text='Quit', font=('times new roman', 15),
                                command=exitfunc).place(x=1380, y=10)
        customtkinter.CTkButton(frame, width=100, height=40, text='Log Out', font=('times new roman', 15),
                                command=start).place(x=1380, y=70)
        Label(frame, text="Well Come " + name, fg='#58a1f0', bg='white', border=1,
              font=('times new roman', 30, 'bold')).place(x=690, y=0)
        Label(frame, text="YOUR APPLICATION HAS BEEN ACCEPTED ", fg='green', bg='white', border=1,
              font=('times new roman', 20, 'bold')).place(x=550, y=100)

        cur = con.cursor()
        query = '''select * from customer where customer_name = %s and customer_mobie = %s'''
        cur.execute(query, (name, phone1))
        result = cur.fetchone()

        loan_name = result[3]
        amount_rec = result[4]
        tenur = result[7]
        start_date = result[15]
        end_date = result[16]
        intrest = result[12]
        intrest_type = result[11]
        pre_pay_panalty = result[13]
        late_pay_intrest = result[14]
        remaining_amount = result[6]
        ######### calculations
        tenur_in_months = result[8]
        emi = result[10]
        total_amount = result[5]
        total_amount_paid = result[17]
        remaining_tenure = result[9]
        loan_acc_number = result[0]

        Label(frame, text="Loan Name :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=200)
        Label(frame, text=str(loan_name), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=200)

        Label(frame, text="Principle amount :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=250)
        Label(frame, text=str(amount_rec), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=250)

        Label(frame, text="Total Amount :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=300)
        Label(frame, text=str(total_amount), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=300)

        Label(frame, text="Loan Tenure in Months :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=350)
        Label(frame, text=str(tenur_in_months), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=350)

        Label(frame, text="Loan Tenure in Years :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=400)
        Label(frame, text=str(tenur), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=400)

        Label(frame, text="Interest per Year :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=450)
        Label(frame, text=str(intrest), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=450)

        Label(frame, text="Interest Type :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=500)
        Label(frame, text=str(intrest_type), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=500)

        Label(frame, text="Pre payment interest :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=550)
        Label(frame, text=str(pre_pay_panalty), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=550)

        Label(frame, text="Late Payment Interest :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=300, y=600)
        Label(frame, text=str(late_pay_intrest), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=550, y=600)

        Label(frame, text="Monthly EMI :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=200)
        Label(frame, text=str(emi), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=200)

        Label(frame, text="Remaining amount :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=250)
        Label(frame, text=str(remaining_amount), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=250)

        Label(frame, text="Remaining Tenure :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=300)
        Label(frame, text=str(remaining_tenure), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=300)

        Label(frame, text="Loan Start Date :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=350)
        Label(frame, text=str(start_date), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=350)

        Label(frame, text="Loan End Date :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=400)
        Label(frame, text=str(end_date), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=400)

        Label(frame, text="Total Amount Paid :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=450)
        Label(frame, text=str(total_amount_paid), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=450)

        Label(frame, text="Loan Account Number :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=500)
        Label(frame, text=str(loan_acc_number), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=500)

        Label(frame, text="Complete Name :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=550)
        Label(frame, text=str(result[1]), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=550)

        Label(frame, text="Phone Number :", fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=750, y=600)
        Label(frame, text=str(result[2]), fg="blue", bg="white", font=('times new roman', 15, "bold")). \
            place(x=1000, y=600)

        def view_users_details1():
            view_users_details(name, phone1)

        def remaining_instalment_details1():
            remaining_instalment_details(name, phone1, 2)

        def pay_amount():

            def pay_amount_db():
                check = askyesno("Conform", "Do you want to Pay : ")
                if (check):
                    loan_acc_number = result[0]
                    loan_name = result[1]
                    remaining_tenure = result[2]
                    emi = result[3]
                    last_pay_date = result[4]
                    interest = result[5]
                    principal = result[6]
                    remaining_amount = result[7]
                    total_amount_paid = result[8]
                    r = interest / 12 / 100

                    intrest_paid = int(principal * r)
                    princial_paid = emi - intrest_paid
                    principal -= princial_paid
                    remaining_tenure = remaining_tenure - 1
                    datee = last_pay_date + relativedelta(months=1)
                    remaining_amount -= emi
                    total_amount_paid += emi

                    cur = con.cursor()
                    query = '''update customer set principal_amount = %s, remaining_amount = %s, 
                    remaing_tenure_number = %s, total_amount_paid = %s, last_pay_date = %s where customer_name = %s 
                    and customer_mobie = %s '''
                    cur.execute(query, (
                        principal, remaining_amount, remaining_tenure, total_amount_paid, datee, Username, phone))
                    con.commit()

                    date = datetime.datetime.now()

                    cur = con.cursor()
                    query = '''insert into history (phone, name, acc_number, date_payed, loan_name, emi, principal_paid, interest_paid, remaining_amount, paid_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    cur.execute(query, (
                        phone, Username, loan_acc_number, date, loan_name, emi, princial_paid, intrest_paid,
                        remaining_amount, total_amount_paid))
                    con.commit()

                    messagebox.showinfo("Success", "Amount Paid Successfully")
                    userfirstpage(Username, phone)
                    add_window.destroy()
                else:
                    add_window.destroy()

            Username = name
            phone = phone1

            cur = con.cursor()
            query = '''select loan_acc_number, loan_name, remaing_tenure_number, EMI, last_pay_date, interest, principal_amount, remaining_amount, total_amount_paid from customer where customer_name = %s and customer_mobie = %s'''
            cur.execute(query, (Username, phone))
            result = cur.fetchone()

            loan_acc_number = result[0]
            loan_name = result[1]
            remaining_tenure = result[2]
            emi = result[3]
            last_pay_date = result[4]
            remaining_amount = result[7]

            if remaining_tenure != 0:

                add_window = Toplevel()
                Label(add_window, text="Loan Account Number : ", fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=0, column=0, padx=10, pady=5)
                Label(add_window, text=str(loan_acc_number), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=0, column=1, padx=10, pady=5)

                Label(add_window, text="User Name : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=1, column=0, padx=10, pady=5)
                Label(add_window, text=str(Username), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=1, column=1, padx=10, pady=5)

                Label(add_window, text="User Mobile Number : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=2, column=0, padx=10, pady=5)
                Label(add_window, text=str(phone), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=2, column=1, padx=10, pady=5)

                Label(add_window, text="Loan Name : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=3, column=0, padx=10, pady=5)
                Label(add_window, text=str(loan_name), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=3, column=1, padx=10, pady=5)

                Label(add_window, text="Remaining Loan Tenure : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=4, column=0, padx=10, pady=5)
                Label(add_window, text=str(remaining_tenure), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=4, column=1, padx=10, pady=5)

                Label(add_window, text="Last Pay Date : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=5, column=0, padx=10, pady=5)
                Label(add_window, text=str(last_pay_date), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=5, column=1, padx=10, pady=5)

                Label(add_window, text="EMI : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=6, column=0, padx=10, pady=5)
                Label(add_window, text=str(emi), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=6, column=1, padx=10, pady=5)
                customtkinter.CTkButton(add_window, width=150, height=30, text='Pay', font=('times new roman', 15),
                                        command=pay_amount_db).grid(row=7, columnspan=2, padx=10, pady=20)
            else:
                messagebox.showerror("Invalid", "Your account Have been cleared")
                check = askyesno("Conform", "Do you want to Restart Aplication : ")
                if (check):
                    restart_aplication()

        def view_pay_histroy1():
            view_pay_histroy(name, phone1, 2)

        def pay_complete():

            def pay_complete_amount_db(amount):
                check = askyesno("Conform", "Do you want to Pay : ")
                if (check):
                    loan_acc_number = result[0]
                    loan_name = result[1]
                    emi = result[3]
                    last_pay_date = result[4]
                    principal = result[6]
                    total_amount_paid = result[8]

                    intrest_paid = amount - principal
                    princial_paid = principal
                    principal = 0
                    remaining_tenure = 0
                    datee = last_pay_date + relativedelta(months=1)
                    remaining_amount = 0
                    total_amount_paid += amount

                    cur = con.cursor()
                    query = '''update customer set principal_amount = %s, remaining_amount = %s, 
                                    remaing_tenure_number = %s, total_amount_paid = %s, last_pay_date = %s where customer_name = %s 
                                    and customer_mobie = %s '''
                    cur.execute(query, (
                        principal, remaining_amount, remaining_tenure, total_amount_paid, datee, Username, phone))
                    con.commit()

                    date = datetime.datetime.now()

                    cur = con.cursor()
                    query = '''insert into history (phone, name, acc_number, date_payed, loan_name, emi, 
                    principal_paid, interest_paid, remaining_amount, paid_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s) '''
                    cur.execute(query,
                                (phone, Username, loan_acc_number, date, loan_name, emi, princial_paid, intrest_paid,
                                 remaining_amount, total_amount_paid))
                    con.commit()

                    messagebox.showinfo("Success", "Amount Paid Successfully")
                    userfirstpage(Username, phone)
                    add_window.destroy()
                else:
                    add_window.destroy()

            Username = name
            phone = phone1

            cur = con.cursor()
            query = '''select loan_acc_number, loan_name, remaing_tenure_number, EMI, last_pay_date, interest, 
            principal_amount, remaining_amount, total_amount_paid, pre_payment_intrest from customer where 
            customer_name = %s and customer_mobie = %s '''
            cur.execute(query, (Username, phone))
            result = cur.fetchone()
            loan_acc_number = result[0]
            loan_name = result[1]
            remaining_tenure = result[2]
            emi = result[3]
            last_pay_date = result[4]
            principal = result[6]
            remaining_amount = result[7]
            pre_pay_panalty = result[9]

            pay_amount = int(principal + int(float(principal) * float(pre_pay_panalty) * 0.01))

            if (remaining_tenure != 0):
                add_window = Toplevel()
                Label(add_window, text="Loan Account Number : ", fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=0, column=0, padx=10, pady=5)
                Label(add_window, text=str(loan_acc_number), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=0, column=1, padx=10, pady=5)

                Label(add_window, text="User Name : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=1, column=0, padx=10, pady=5)
                Label(add_window, text=str(Username), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=1, column=1, padx=10, pady=5)

                Label(add_window, text="User Mobile Number : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=2, column=0, padx=10, pady=5)
                Label(add_window, text=str(phone), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=2, column=1, padx=10, pady=5)

                Label(add_window, text="Loan Name : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=3, column=0, padx=10, pady=5)
                Label(add_window, text=str(loan_name), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=3, column=1, padx=10, pady=5)

                Label(add_window, text="Remaining Loan Tenure : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=4, column=0, padx=10, pady=5)
                Label(add_window, text=str(remaining_tenure), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=4, column=1, padx=10, pady=5)

                Label(add_window, text="Last Pay Date : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=5, column=0, padx=10, pady=5)
                Label(add_window, text=str(last_pay_date), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=5, column=1, padx=10, pady=5)

                Label(add_window, text="EMI : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=6, column=0, padx=10, pady=5)
                Label(add_window, text=str(emi), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=6, column=1, padx=10, pady=5)

                Label(add_window, text="Pre Payment Penalty Interest : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=7, column=0, padx=10, pady=5)
                Label(add_window, text=str(pre_pay_panalty), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=7, column=1, padx=10, pady=5)

                Label(add_window, text="Principle Amount : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=8, column=0, padx=10, pady=5)
                Label(add_window, text=str(principal), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=8, column=1, padx=10, pady=5)

                Label(add_window, text="Total Payable Amount : ", fg='Green',
                      font=('times new roman', 15, "bold")). \
                    grid(row=9, column=0, padx=10, pady=5)
                Label(add_window, text=str(pay_amount), fg='Green', font=('times new roman', 15, "bold")). \
                    grid(row=9, column=1, padx=10, pady=5)

                def pay_complete_amount_db1():
                    pay_complete_amount_db(pay_amount)

                customtkinter.CTkButton(add_window, width=150, height=30, text='Pay Complete',
                                        font=('times new roman', 15),
                                        command=pay_complete_amount_db1).grid(row=10, columnspan=2, padx=10, pady=20)

            else:
                messagebox.showerror("Invalid", "Your account Have been cleared")
                check = askyesno("Conform", "Do you want to Restart Aplication : ")
                if (check):
                    restart_aplication()

        customtkinter.CTkButton(frame, width=250, height=40, text='View Your Details', font=('times new roman', 15),
                                command=view_users_details1).place(x=1180, y=200)
        customtkinter.CTkButton(frame, width=250, height=40, text='View Remaining instalment details',
                                font=('times new roman', 15),
                                command=remaining_instalment_details1).place(x=1180, y=600)
        customtkinter.CTkButton(frame, width=250, height=40, text='Pay EMI', font=('times new roman', 15),
                                command=pay_amount).place(x=1180, y=300)
        customtkinter.CTkButton(frame, width=250, height=40, text='View Payed History', font=('times new roman', 15),
                                command=view_pay_histroy1).place(x=1180, y=500)
        customtkinter.CTkButton(frame, width=250, height=40, text='Pay Complete amount', font=('times new roman', 15),
                                command=pay_complete).place(x=1180, y=400)


    else:
        customtkinter.CTkButton(frame, width=100, height=40, text='Quit', font=('times new roman', 15),
                                command=exitfunc).place(x=1380, y=10)
        customtkinter.CTkButton(frame, width=100, height=40, text='Log Out', font=('times new roman', 15),
                                command=start).place(x=1380, y=70)
        Label(frame, text="Well Come " + name, fg='#58a1f0', bg='white', border=1,
              font=('times new roman', 30, 'bold')).place(x=690, y=0)
        Label(frame, text="YOU WILL GET THE TO SEE THE STATUS AFTER VERIFICATION", fg='green',
              bg='white', border=1,
              font=('times new roman', 20, 'bold')).place(x=350, y=100)


################################# Admin frame########################################################################

##################################company details###################################################################
def update_company():
    name = name_val.get()
    address = address_value.get(1.0, "end-1c")
    email = email_val.get()
    phone1 = mob1_val.get()
    phone2 = mob2_val.get()
    discription = discription_val.get(1.0, "end-1c")
    goals = goals_val.get(1.0, "end-1c")

    if (
            name != "" and address != "" and email != "" and phone1 != "" and phone2 != "" and discription != "" and goals != ""):
        if (len(phone2) == 10 and len(phone1) == 10):
            cur = con.cursor()
            query = """UPDATE company SET name = %s, address = %s, email = %s, phone1 = %s, phone2 = %s, discription = %s, goals = %s WHERE id = %s"""
            cur.execute(query, (name, address, email, phone1, phone2, discription, goals, 1))
            con.commit()
            messagebox.showinfo("Sucess", "Update sucessfull")
            admin_page()
        else:
            messagebox.showerror("Invalid", "this mobile number are invalid")
    else:
        messagebox.showerror("Invalid", "Enter all the details")


name_val = 0
address_value = 0
email_val = 0
mob1_val = 0
mob2_val = 0
discription_val = 0
goals_val = 0


def edit_comp():
    global frame
    global name_val
    global address_value
    global email_val
    global mob1_val
    global mob2_val
    global discription_val
    global goals_val
    cur = con.cursor()
    query = """select * from company WHERE id = %s"""
    cur.execute(query, (1,))
    myresult = cur.fetchone()

    frame = Frame(root, bg="white").place(x=250, y=0, width=1285, height=750)
    lab_name = Label(frame, text="Company Name", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_name.place(x=460, y=60)
    name_val = Entry(frame, width=80, fg='black', border=2, bg="white", font=('times new roman', 13))
    name_val.place(x=700, y=60)
    name_val.insert(0, myresult[1])

    lab_address = Label(frame, text="Company address", fg='black', bg='white',
                        font=('times new roman', 13, "bold"))
    lab_address.place(x=460, y=110)
    address_value = tK.Text(frame, width=80, height=3, fg='black', border=2, bg="white",
                            font=('times new roman', 13))
    address_value.place(x=700, y=110)
    address_value.insert(tK.INSERT, myresult[2])

    lab_email = Label(frame, text="Email address", fg='black', bg='white',
                      font=('times new roman', 13, "bold"))
    lab_email.place(x=460, y=190)
    email_val = Entry(frame, width=80, fg='black', border=2, bg="white", font=('times new roman', 13))
    email_val.place(x=700, y=190)
    email_val.insert(0, myresult[3])

    lab_mob1 = Label(frame, text="Mobile 1", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_mob1.place(x=460, y=240)
    mob1_val = Entry(frame, width=80, fg='black', border=2, bg="white", font=('times new roman', 13))
    mob1_val.place(x=700, y=240)
    mob1_val.insert(0, myresult[4])

    lab_mob2 = Label(frame, text="Mobile 2", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_mob2.place(x=460, y=290)
    mob2_val = Entry(frame, width=80, fg='black', border=2, bg="white", font=('times new roman', 13))
    mob2_val.place(x=700, y=290)
    mob2_val.insert(0, myresult[5])

    lab_discription = Label(frame, text="Company Description", fg='black', bg='white',
                            font=('times new roman', 13, "bold"))
    lab_discription.place(x=460, y=340)
    discription_val = tK.Text(frame, width=80, height=7, fg='black', border=2, bg="white",
                              font=('times new roman', 13))
    discription_val.place(x=700, y=340)
    discription_val.insert(tK.INSERT, myresult[6])

    lab_goals = Label(frame, text="Company Goals", fg='black', bg='white',
                      font=('times new roman', 13, "bold"))
    lab_goals.place(x=460, y=540)
    goals_val = tK.Text(frame, width=80, height=6, fg='black', border=2, bg="white",
                        font=('times new roman', 13))
    goals_val.place(x=700, y=540)
    goals_val.insert(tK.INSERT, myresult[7])
    customtkinter.CTkButton(frame, width=200, height=40, text='Update', font=('times new roman', 15),
                            command=update_company).place(
        x=800, y=670)


##########################################loan Schemes########################################################################################

sc_name = 0
sc_max_amt = 0
sc_int_rate = 0
sc_int_typ = 0
sc_tenur = 0
sc_pre_pay = 0
sc_penalty = 0
sc_doc_rec = 0
loansceme = 0
add_window = 0
sc_id = 0

new_user_table = 0
active_user_table = 0


def load_sch_tb():
    global loansceme
    for item in loansceme.get_children():
        loansceme.delete(item)

    cur = con.cursor()
    query = """select * from loan"""
    cur.execute(query, )
    myresult = cur.fetchall()

    data = list(myresult)
    for i in range(len(myresult)):
        loansceme.insert("", "end",
                         values=(
                             data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6],
                             data[i][7],
                             data[i][8]))


def add_sch_db():
    global add_window
    temp1 = sc_name.get()
    temp2 = sc_max_amt.get()
    temp3 = sc_int_rate.get()
    temp4 = sc_int_typ.get()
    temp5 = sc_tenur.get()
    temp6 = sc_pre_pay.get()
    temp7 = sc_penalty.get()
    temp8 = sc_doc_rec.get()

    check = True
    try:
        temp2 = int(temp2)
        temp3 = float(round(float(temp3), 2))
        temp6 = float(round(float(temp6), 2))
        temp7 = float(round(float(temp7), 2))
    except:
        messagebox.showerror("Invalid", "Check the Correctness with number and word types")
        check = False

    if (check):
        if (
                temp1 != "" and temp2 != "" and temp3 != "" and temp4 != "" and temp5 != "" and temp6 != "" and temp7 != "" and temp8 != ""):
            cur = con.cursor()
            query = """INSERT INTO loan (name, maxamount, intrat, inttype, loanten, prepaypen, penint, recdoc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(query, (temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8))
            con.commit()
            messagebox.showinfo("Success", "Loan Scheme added successful")
            add_window.destroy()
            loandetails()
            load_sch_tb()

        else:
            messagebox.showerror("Invalid", "All the Details must be Filled")
            loandetails()


def add_schemes():
    global sc_name
    global sc_max_amt
    global sc_int_rate
    global sc_int_typ
    global sc_tenur
    global sc_pre_pay
    global sc_penalty
    global sc_doc_rec
    global add_window
    add_window = Toplevel()
    Label(add_window, text="Name", font=('times new roman', 15, "bold")).grid(row=0, column=0, padx=10,
                                                                              pady=5)
    sc_name = Entry(add_window, width=50, fg='black', border=0, bg="white",
                    font=('times new roman', 15))
    sc_name.grid(row=0, column=1, padx=10, pady=5)
    print(sc_name.get())
    Label(add_window, text="Max Amount", font=('times new roman', 15, "bold")).grid(row=1, column=0, padx=10,
                                                                                    pady=10)
    sc_max_amt = Entry(add_window, width=50, fg='black', border=0, bg="white",
                       font=('times new roman', 15))
    sc_max_amt.grid(row=1, column=1, padx=10, pady=5)
    Label(add_window, text="Interest rate", font=('times new roman', 15, "bold")).grid(row=2, column=0,
                                                                                       padx=10,
                                                                                       pady=5)
    sc_int_rate = Entry(add_window, width=50, fg='black', border=0, bg="white",
                        font=('times new roman', 15))
    sc_int_rate.grid(row=2, column=1, padx=0, pady=5)
    Label(add_window, text="Interest type", font=('times new roman', 15, "bold")).grid(row=3, column=0,
                                                                                       padx=10,
                                                                                       pady=5)
    sc_int_typ = Entry(add_window, width=50, fg='black', border=0, bg="white",
                       font=('times new roman', 15))
    sc_int_typ.grid(row=3, column=1, padx=10, pady=5)
    Label(add_window, text="Loan Tenure", font=('times new roman', 15, "bold")).grid(row=4, column=0, padx=10,
                                                                                     pady=5)
    sc_tenur = Entry(add_window, width=50, fg='black', border=0, bg="white",
                     font=('times new roman', 15))
    sc_tenur.grid(row=4, column=1, padx=10, pady=5)
    Label(add_window, text="Pre-payment Penalty rate", font=('times new roman', 15, "bold")).grid(row=5,
                                                                                                  column=0,
                                                                                                  padx=10,
                                                                                                  pady=5)
    sc_pre_pay = Entry(add_window, width=50, fg='black', border=0, bg="white",
                       font=('times new roman', 15))
    sc_pre_pay.grid(row=5, column=1, padx=10, pady=5)
    Label(add_window, text="Penalty interest rate", font=('times new roman', 15, "bold")).grid(row=6, column=0,
                                                                                               padx=10,
                                                                                               pady=5)
    sc_penalty = Entry(add_window, width=50, fg='black', border=0, bg="white",
                       font=('times new roman', 15))
    sc_penalty.grid(row=6, column=1, padx=10, pady=5)
    Label(add_window, text="Required Documents", font=('times new roman', 15, "bold")).grid(row=7, column=0,
                                                                                            padx=10,
                                                                                            pady=5)
    sc_doc_rec = Entry(add_window, width=50, fg='black', border=0, bg="white",
                       font=('times new roman', 15))
    sc_doc_rec.grid(row=7, column=1, padx=10, pady=5)

    customtkinter.CTkButton(add_window, width=50, height=40, text='Add Scheme',
                            command=add_sch_db).grid(row=8, columnspan=2, pady=10)
    add_window.grab_set()


def update_sch_db():
    global add_window
    temp0 = sc_id.get()
    temp1 = sc_name.get()
    temp2 = sc_max_amt.get()
    temp3 = sc_int_rate.get()
    temp4 = sc_int_typ.get()
    temp5 = sc_tenur.get()
    temp6 = sc_pre_pay.get()
    temp7 = sc_penalty.get()
    temp8 = sc_doc_rec.get()

    check = True
    try:
        temp0 = int(temp0)
        temp2 = int(temp2)
        temp3 = float(round(float(temp3), 2))
        temp6 = float(round(float(temp6), 2))
        temp7 = float(round(float(temp7), 2))

    except:
        messagebox.showerror("Invalid", "Check the Correctness Weather It is Numerical or string")
        check = False

    if (check):
        if (
                temp1 != "" and temp2 != "" and temp0 != "" and temp3 != "" and temp4 != "" and temp5 != "" and temp6 !=
                "" and temp7 != "" and temp8 != ""):
            cur = con.cursor()
            query = """select * from loan WHERE id = %s"""
            cur.execute(query, (temp0,))
            myresult = cur.fetchone()
            if (myresult != None):
                cur = con.cursor()
                query = """UPDATE loan set name = %s, maxamount = %s, intrat = %s, inttype = %s, 
                loanten = %s, prepaypen = %s, penint = %s, recdoc = %s WHERE id = %s"""
                cur.execute(query, (temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp0))
                con.commit()
                messagebox.showinfo("Success", "Loan Scheme Updated successful")
                add_window.destroy()
                loandetails()
                load_sch_tb()
            else:
                messagebox.showerror("Invalid", "ID not found ")


        else:
            messagebox.showerror("Invalid", "All the Details must be Filled")
            loandetails()


def upd_schemes():
    global sc_id
    global sc_name
    global sc_max_amt
    global sc_int_rate
    global sc_int_typ
    global sc_tenur
    global sc_pre_pay
    global sc_penalty
    global sc_doc_rec
    global add_window
    global loansceme
    check = 0
    try:
        selected = loansceme.selection()[0]
        check = 1
    except:
        messagebox.showerror("Invalid", "Select the required Row")

    if check:
        add_window = Toplevel()
        Label(add_window, text="ID", font=('times new roman', 15, "bold")).grid(row=0, column=0, padx=10,
                                                                                pady=5)
        sc_id = Entry(add_window, width=50, fg='black', border=0, bg="white",
                      font=('times new roman', 15))
        sc_id.grid(row=0, column=1, padx=10, pady=5)
        sc_id.insert(0, loansceme.item(selected)['values'][0])

        Label(add_window, text="Name", font=('times new roman', 15, "bold")).grid(row=1, column=0, padx=10,
                                                                                  pady=5)
        sc_name = Entry(add_window, width=50, fg='black', border=0, bg="white",
                        font=('times new roman', 15))
        sc_name.grid(row=1, column=1, padx=10, pady=5)
        sc_name.insert(0, loansceme.item(selected)['values'][1])
        Label(add_window, text="Max Amount", font=('times new roman', 15, "bold")).grid(row=2, column=0, padx=10,
                                                                                        pady=5)
        sc_max_amt = Entry(add_window, width=50, fg='black', border=0, bg="white",
                           font=('times new roman', 15))
        sc_max_amt.grid(row=2, column=1, padx=10, pady=5)
        sc_max_amt.insert(0, loansceme.item(selected)['values'][2])
        Label(add_window, text="Interest rate", font=('times new roman', 15, "bold")).grid(row=3, column=0,
                                                                                           padx=10,
                                                                                           pady=5)
        sc_int_rate = Entry(add_window, width=50, fg='black', border=0, bg="white",
                            font=('times new roman', 15))
        sc_int_rate.grid(row=3, column=1, padx=10, pady=5)
        sc_int_rate.insert(0, loansceme.item(selected)['values'][3])
        Label(add_window, text="Interest type", font=('times new roman', 15, "bold")).grid(row=4, column=0,
                                                                                           padx=10,
                                                                                           pady=5)
        sc_int_typ = Entry(add_window, width=50, fg='black', border=0, bg="white",
                           font=('times new roman', 15))
        sc_int_typ.grid(row=4, column=1, padx=10, pady=5)
        sc_int_typ.insert(0, loansceme.item(selected)['values'][4])
        Label(add_window, text="Loan Tenure", font=('times new roman', 15, "bold")).grid(row=5, column=0, padx=10,
                                                                                         pady=5)
        sc_tenur = Entry(add_window, width=50, fg='black', border=0, bg="white",
                         font=('times new roman', 15))
        sc_tenur.grid(row=5, column=1, padx=10, pady=5)
        sc_tenur.insert(0, loansceme.item(selected)['values'][5])
        Label(add_window, text="Pre-payment Penalty rate", font=('times new roman', 15, "bold")).grid(row=6,
                                                                                                      column=0,
                                                                                                      padx=10,
                                                                                                      pady=5)
        sc_pre_pay = Entry(add_window, width=50, fg='black', border=0, bg="white",
                           font=('times new roman', 15))
        sc_pre_pay.grid(row=6, column=1, padx=10, pady=5)
        sc_pre_pay.insert(0, loansceme.item(selected)['values'][6])
        Label(add_window, text="Panalty interest rate", font=('times new roman', 15, "bold")).grid(row=7, column=0,
                                                                                                   padx=10,
                                                                                                   pady=5)
        sc_penalty = Entry(add_window, width=50, fg='black', border=0, bg="white",
                           font=('times new roman', 15))
        sc_penalty.grid(row=7, column=1, padx=10, pady=5)
        sc_penalty.insert(0, loansceme.item(selected)['values'][7])
        Label(add_window, text="Required Documents", font=('times new roman', 15, "bold")).grid(row=8, column=0,
                                                                                                padx=10,
                                                                                                pady=5)
        sc_doc_rec = Entry(add_window, width=50, fg='black', border=0, bg="white",
                           font=('times new roman', 15))
        sc_doc_rec.grid(row=8, column=1, padx=10, pady=5)
        sc_doc_rec.insert(0, loansceme.item(selected)['values'][8])
        customtkinter.CTkButton(add_window, width=100, height=40, text='Update Scheme', font=('times new roman', 15),
                                command=update_sch_db).grid(row=9, columnspan=2, pady=10)
        add_window.grab_set()


def delete_sch_db(id):
    cur = con.cursor()
    query = """select * from loan WHERE id = %s"""
    cur.execute(query, (id,))
    myresult = cur.fetchone()
    if (myresult != None):
        cur = con.cursor()
        query = """delete from loan WHERE id = %s"""
        cur.execute(query, (id,))
        con.commit()
        messagebox.showinfo("Success", "Loan Scheme Deleted successful")
        add_window.destroy()
        loandetails()
        load_sch_tb()
    else:
        messagebox.showerror("Invalid", "ID not found ")


def del_schemes():
    global sc_id
    global add_window
    check = 0
    try:
        selected = loansceme.selection()[0]
        check = 1
    except:
        messagebox.showerror("Invalid", "Select the required Row")

    if check:
        id = loansceme.item(selected)['values'][0]
        check = askyesno("Conform", "Do you want to delete ID : " + str(id))
        if (check):
            delete_sch_db(id)


def loandetails():
    global frame, frame1

    global loansceme
    frame = Frame(root, bg="white").place(x=250, y=0, width=1285, height=750)

    loansceme = ttk.Treeview(frame, selectmode='browse')

    customtkinter.CTkButton(frame, width=100, height=40, text='Add New Schemes',
                            command=add_schemes).place(x=550, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text='Update Schemes', command=upd_schemes).place(x=850, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text='Delete Schemes', command=del_schemes).place(x=1150,
                                                                                                           y=710)

    loansceme["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8")
    loansceme['show'] = 'headings'
    loansceme.column("0", width=10, anchor=CENTER)
    loansceme.column("1", width=100, anchor=CENTER)
    loansceme.column("2", width=50, anchor=CENTER)
    loansceme.column("3", width=50, anchor=CENTER)
    loansceme.column("4", width=50, anchor=CENTER)
    loansceme.column("5", width=100, anchor=CENTER)
    loansceme.column("6", width=100, anchor=CENTER)
    loansceme.column("7", width=70, anchor=CENTER)
    loansceme.column("8", width=200, anchor=CENTER)
    scrollbarX = ttk.Scrollbar(frame,
                               orient="horizontal",
                               command=loansceme.xview)
    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=loansceme.yview)
    loansceme.place(x=300, y=20, height=640, width=1170)
    scrollbarY.place(x=288, y=20, height=640)
    scrollbarX.place(x=288, y=660, width=1170)
    loansceme.configure(xscrollcommand=scrollbarX.set)
    loansceme.configure(yscrollcommand=scrollbarY.set)

    loansceme.heading("0", text="ID")
    loansceme.heading("1", text="Name")
    loansceme.heading("2", text="Max amount")
    loansceme.heading("3", text="Interest rate")
    loansceme.heading("4", text="Interest type")
    loansceme.heading("5", text="Loan Tenure(Months)")
    loansceme.heading("6", text="Pre-payment Penalty rate")
    loansceme.heading("7", text="Penalty interest Rate")
    loansceme.heading("8", text="Required Documents")

    load_sch_tb()


######################################################### NEW USERS #################################################################

def view_new_user_table():
    global new_user_table
    for item in new_user_table.get_children():
        new_user_table.delete(item)

    cur = con.cursor()
    query = """select username, userphone1, useremail, adharnumber, pannumber, loanscheme, amountrec, tenure, 
    submitdate from users Where NOT userphone2 = 'NULL' and NOT status = 'YES' order by submitdate"""
    cur.execute(query, )
    myresult = cur.fetchall()

    data = list(myresult)
    for i in range(len(myresult)):
        new_user_table.insert("", "end",
                              values=(
                                  data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6],
                                  data[i][7], data[i][8]))


def view_new_users_complete(table, id):
    new_user_table1 = table
    check = 0
    try:
        selected = new_user_table1.selection()[0]
        check = 1
    except:
        messagebox.showerror("Invalid", "Select the required Row")

    if check:
        phone = new_user_table1.item(selected)['values'][1]
        username = new_user_table1.item(selected)['values'][0]
        cur = con.cursor()
        query = '''select * from users where userphone1 = %s and username = %s'''
        cur.execute(query, (phone, username))
        myresult = cur.fetchone()

        def view_adarfile():
            view_image(convertbtof(myresult[12]))

        def view_panfile():
            view_image(convertbtof(myresult[11]))

        def view_passbookfile():
            view_image(convertbtof(myresult[21]))

        def view_doc1file():
            if convertbtof(myresult[22]) != -1:
                view_image(convertbtof(myresult[22]))

        def view_doc2file():
            if convertbtof(myresult[23]) != -1:
                view_image(convertbtof(myresult[23]))

        def view_doc3file():
            if convertbtof(myresult[24]) != -1:
                view_image(convertbtof(myresult[24]))

        def view_doc4file():
            if convertbtof(myresult[25]) != -1:
                view_image(convertbtof(myresult[25]))

        def view_user_photofile():
            view_image(convertbtof(myresult[10]))

        def go_back_to_new_userpage():
            admin_page()
            view_new_users()

        def go_back_to_active_userpage():
            admin_page()
            view_active_users()

        frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)
        Label(frame, text='Complete Details of User ' + myresult[1], fg='Green', bg='white', border=1,
              font=('times new roman', 20, 'bold')).place(x=550, y=20)
        if (id == 1):
            customtkinter.CTkButton(frame, width=120, height=40, text='Back', font=('times new roman', 15),
                                    command=go_back_to_new_userpage).place(x=1385, y=10)
        else:
            customtkinter.CTkButton(frame, width=120, height=40, text='Back', font=('times new roman', 15),
                                    command=go_back_to_active_userpage).place(x=1385, y=10)

        Label(frame, text='Father Name : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=100)
        Label(frame, text=myresult[14], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=100)

        Label(frame, text='Mother Name : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=150)
        Label(frame, text=myresult[15], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=150)

        Label(frame, text='Father Phone : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=200)
        Label(frame, text=myresult[6], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=200)

        Label(frame, text='Mother Phone : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=250)
        Label(frame, text=myresult[16], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=250)

        Label(frame, text='Aadhar Number : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=300)
        Label(frame, text=myresult[8], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=300)

        Label(frame, text='Aadhar Photo: ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=350)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_adarfile).place(x=350, y=350)

        Label(frame, text='PAN Number : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=400)
        Label(frame, text=myresult[9], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=400)

        Label(frame, text='PAN Photo: ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=450)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_panfile).place(x=350, y=450)

        Label(frame, text='Family Income(in Numbers): ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=500)
        Label(frame, text=str(myresult[17]), fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=500)

        Label(frame, text='Email : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=550)
        Label(frame, text=myresult[7], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=350, y=550)

        Label(frame, text='Permanent Address : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=600)
        perm_address = Message(frame, text=myresult[4], width=500, fg='Green', bg='white',
                               font=('times new roman', 13))
        perm_address.place(x=350, y=600)

        Label(frame, text='User Photo : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=100, y=700)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_user_photofile).place(x=350, y=700)

        Label(frame, text='Office Address : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=100)
        office_address = Message(frame, text=myresult[5], width=500, fg='Green', bg='white',
                                 font=('times new roman', 13))
        office_address.place(x=1050, y=100)

        Label(frame, text='Pincode : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=200)
        Label(frame, text=str(myresult[18]), fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=1050, y=200)

        Label(frame, text='Amount Required : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=250)
        Label(frame, text=str(myresult[26]), fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=1050, y=250)

        Label(frame, text='No of Years : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=300)
        Label(frame, text=str(myresult[27]), fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=1050, y=300)

        Label(frame, text='Bank Account number : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=350)
        Label(frame, text=myresult[19], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=1050, y=350)

        Label(frame, text='Bank IFSC code : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=400)
        Label(frame, text=myresult[20], fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=1050, y=400)

        Label(frame, text='Bank Passbook : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=450)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_passbookfile).place(x=1050, y=450)

        Label(frame, text='Remaining Documents : (Optional)', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=500)

        Label(frame, text='Documents 1 : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=550)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_doc1file).place(x=1050, y=550)

        Label(frame, text='Documents 2 : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=600)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_doc2file).place(x=1050, y=600)

        Label(frame, text='Documents 3 : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=650)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_doc3file).place(x=1050, y=650)

        Label(frame, text='Documents 4 : ', fg='Green', bg='white', border=1,
              font=('times new roman', 15, 'bold')).place(x=800, y=700)
        customtkinter.CTkButton(frame, width=100, height=30, text='View', font=('times new roman', 15),
                                command=view_doc4file).place(x=1050, y=700)


def reject_new_user():
    def reject_new_user_db():
        check = askyesno("Conform", "Do you want to Reject : ")
        if (check):

            remarks = remark.get(1.0, "end-1c")
            if (remarks != ""):
                phone = new_user_table.item(selected)['values'][1]
                username = new_user_table.item(selected)['values'][0]
                cur = con.cursor()
                query = '''update users set  userphone2 = %s, remark = %s, status = %s where userphone1 = %s and username = %s'''
                cur.execute(query, ("NULL", remarks, "NO", phone, username))
                con.commit()
                messagebox.showinfo("Success", "Rejected Successfully")
                view_new_user_table()
                add_window.destroy()
            else:
                messagebox.showerror("Invalid", "Please enter the Remark")

    global new_user_table
    check = 0
    try:
        selected = new_user_table.selection()[0]
        check = 1
    except:
        messagebox.showerror("Invalid", "Select the required Row")

    if check:
        add_window = Toplevel()
        customtkinter.CTkButton(add_window, width=100, height=30, text='Reject', font=('times new roman', 15),
                                command=reject_new_user_db).grid(row=3, padx=10, pady=10)
        Label(add_window, text="Please Provide the Remark", fg="blue", bg="white",
              font=('times new roman', 20, "bold")).grid(row=0,
                                                         padx=10,
                                                         pady=10)
        remark = tK.Text(add_window, width=80, height=5, fg='black', border=2, bg="white",
                         font=('times new roman', 13))
        remark.grid(row=1, padx=10, pady=20)


def accept_new_user():
    global new_user_table

    check = 0
    try:
        selected = new_user_table.selection()[0]
        check = 1
    except:
        messagebox.showerror("Invalid", "Select the required Row")

    if check:
        add_window = Toplevel()

        Username = new_user_table.item(selected)['values'][0]
        phone = new_user_table.item(selected)['values'][1]
        loan_name = new_user_table.item(selected)['values'][5]
        amount_rec = new_user_table.item(selected)['values'][6]
        tenur = new_user_table.item(selected)['values'][7]
        date = datetime.date.today()

        cur = con.cursor()
        query = '''select * from loan where name = %s'''
        cur.execute(query, (loan_name,))
        result = cur.fetchone()
        intrest = result[3]
        intrest_type = result[4]
        pre_pay_panalty = result[6]
        late_pay_intrest = result[7]

        ######### calculations
        tenur_in_months = int(tenur) * 12
        r_of_int = intrest / 12 / 100
        emi = amount_rec * r_of_int * (
                (pow((1 + r_of_int), tenur_in_months)) / ((pow((1 + r_of_int), tenur_in_months)) - 1))
        emi = int(emi)
        total_amount = emi * tenur_in_months

        Label(add_window, text="Loan Name", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=0, column=0, padx=10, pady=5)
        Label(add_window, text=str(loan_name), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=0, column=1, padx=10, pady=5)

        Label(add_window, text="User Name", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=1, column=0, padx=10, pady=5)
        Label(add_window, text=str(Username), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=1, column=1, padx=10, pady=5)

        Label(add_window, text="User Phone", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=2, column=0, padx=10, pady=5)
        Label(add_window, text=str(phone), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=2, column=1, padx=10, pady=5)

        Label(add_window, text="Principle amount", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=3, column=0, padx=10, pady=5)
        Label(add_window, text=str(amount_rec), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=3, column=1, padx=10, pady=5)

        Label(add_window, text="Total Amount", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=4, column=0, padx=10, pady=5)
        Label(add_window, text=str(total_amount), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=4, column=1, padx=10, pady=5)

        Label(add_window, text="Loan Tenure in Months", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=5, column=0, padx=10, pady=5)
        Label(add_window, text=str(tenur_in_months), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=5, column=1, padx=10, pady=5)

        Label(add_window, text="Loan Tenure in Years", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=6, column=0, padx=10, pady=5)
        Label(add_window, text=str(tenur), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=6, column=1, padx=10, pady=5)

        Label(add_window, text="Monthly EMI", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=7, column=0, padx=10, pady=5)
        Label(add_window, text=str(emi), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=7, column=1, padx=10, pady=5)

        Label(add_window, text="Interest per Year", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=8, column=0, padx=10, pady=5)
        Label(add_window, text=str(intrest), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=8, column=1, padx=10, pady=5)

        Label(add_window, text="Interest Type", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=9, column=0, padx=10, pady=5)
        Label(add_window, text=str(intrest_type), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=9, column=1, padx=10, pady=5)

        Label(add_window, text="Pre payment interest", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=10, column=0, padx=10, pady=5)
        Label(add_window, text=str(pre_pay_panalty), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=10, column=1, padx=10, pady=5)

        Label(add_window, text="Late Payment Interest", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=11, column=0, padx=10, pady=5)
        Label(add_window, text=str(late_pay_intrest), fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=11, column=1, padx=10, pady=5)

        Label(add_window, text="Tenure Start Date", fg='Green', font=('times new roman', 15, "bold")). \
            grid(row=12, column=0, padx=10, pady=5)
        start_date = Entry(add_window, fg='Green', bg='white', font=('times new roman', 15, "bold"))
        start_date.grid(row=12, column=1, padx=10, pady=5)
        start_date.insert(0, date)

        def accept_new_user_db():
            check = 0
            try:
                date = datetime.datetime.strptime(start_date.get(), "%Y-%m-%d")
                loan_end_date = pd.to_datetime(date) + pd.DateOffset(years=tenur)
                loan_end_date = str(loan_end_date)
                check = 1
            except:
                check = 0
                messagebox.showerror("Invalid", "enter proper Date")
            check2 = askyesno("Conform", "Do you want to Accept : ")
            if check and check2:
                tenur_in_months1 = tenur_in_months
                total_amount1 = total_amount

                cur = con.cursor()
                query = """INSERT INTO customer (customer_name, customer_mobie, loan_name, principal_amount, 
                total_amount, remaining_amount, loan_ten_year, loan_ten_month, remaing_tenure_number, EMI, interest_type, interest, 
                pre_payment_intrest, late_payment_intrest, loan_start_date, loan_end_date, last_pay_date, sanctioned_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                cur.execute(query, (Username, phone, loan_name, int(amount_rec), total_amount, total_amount, int(tenur),
                                    int(tenur_in_months),
                                    tenur_in_months1, int(emi), intrest_type, intrest, pre_pay_panalty,
                                    late_pay_intrest, date, loan_end_date, date, int(amount_rec)))
                con.commit()

                cur = con.cursor()
                query = '''update users set status = %s where userphone1 = %s and username = %s'''
                cur.execute(query, ("YES", phone, Username))
                con.commit()
                messagebox.showinfo("Success", "User Accepted")
                view_new_user_table()
                add_window.destroy()

        customtkinter.CTkButton(add_window, width=100, height=30, text='Accept', font=('times new roman', 15),
                                command=accept_new_user_db).grid(row=14, columnspan=2, padx=10, pady=10)


def view_new_users():
    def view_new_users_complete1():
        view_new_users_complete(new_user_table, 1)

    global frame, new_user_table
    frame = Frame(root, bg="white").place(x=250, y=0, width=1285, height=750)

    new_user_table = ttk.Treeview(frame, selectmode='browse')

    customtkinter.CTkButton(frame, width=100, height=40, text='View Complete Details',
                            command=view_new_users_complete1).place(x=550, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text=' Approve ', command=accept_new_user).place(x=850, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text=' Reject ', command=reject_new_user).place(x=1150,
                                                                                                         y=710)

    new_user_table["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8")
    new_user_table['show'] = 'headings'
    new_user_table.column("0", width=50, anchor=CENTER)
    new_user_table.column("1", width=100, anchor=CENTER)
    new_user_table.column("2", width=120, anchor=CENTER)
    new_user_table.column("3", width=120, anchor=CENTER)
    new_user_table.column("4", width=100, anchor=CENTER)
    new_user_table.column("5", width=100, anchor=CENTER)
    new_user_table.column("6", width=100, anchor=CENTER)
    new_user_table.column("7", width=70, anchor=CENTER)
    new_user_table.column("8", width=200, anchor=CENTER)
    scrollbarX = ttk.Scrollbar(frame,
                               orient="horizontal",
                               command=new_user_table.xview)
    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=new_user_table.yview)
    new_user_table.place(x=300, y=20, height=640, width=1170)
    scrollbarY.place(x=288, y=20, height=640)
    scrollbarX.place(x=288, y=660, width=1170)
    new_user_table.configure(xscrollcommand=scrollbarX.set)
    new_user_table.configure(yscrollcommand=scrollbarY.set)

    new_user_table.heading("0", text="User Name")
    new_user_table.heading("1", text="Phone Number")
    new_user_table.heading("2", text="Email")
    new_user_table.heading("3", text="Aadhar Number")
    new_user_table.heading("4", text="PAN Number")
    new_user_table.heading("5", text="Loan Scheme")
    new_user_table.heading("6", text="Amount required")
    new_user_table.heading("7", text="Tenure in Years")
    new_user_table.heading("8", text="Submission date")
    view_new_user_table()


###################################################### Active user #####################################################
def view_active_user_table():
    global active_user_table
    for item in active_user_table.get_children():
        active_user_table.delete(item)

    cur = con.cursor()
    query = """select * from customer where not loan_name = 'NULL'"""
    cur.execute(query, )
    myresult = cur.fetchall()

    data = list(myresult)
    for i in range(len(myresult)):
        active_user_table.insert("", "end",
                                 values=(
                                     data[i][1], data[i][2], data[i][0], data[i][3], data[i][4], data[i][5], data[i][6],
                                     data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], data[i][12],
                                     data[i][13], data[i][14], data[i][15], data[i][16], data[i][17], data[i][19],
                                     data[i][18]))


def view_active_users():
    global frame, active_user_table

    def view_new_users_complete1():
        view_new_users_complete(active_user_table, 2)

    def view_remaining_instalment_details():
        check = 0
        try:
            selected = active_user_table.selection()[0]
            check = 1
        except:
            messagebox.showerror("Invalid", "Select the required Row")

        if check:
            phone = active_user_table.item(selected)['values'][1]
            username = active_user_table.item(selected)['values'][0]
            remaining_instalment_details(username, phone, 1)

    def view_payment_history1():
        check = 0
        try:
            selected = active_user_table.selection()[0]
            check = 1
        except:
            messagebox.showerror("Invalid", "Select the required Row")

        if check:
            phone = active_user_table.item(selected)['values'][1]
            username = active_user_table.item(selected)['values'][0]
            view_pay_histroy(username, phone, 1)

    frame = Frame(root, bg="white").place(x=250, y=0, width=1285, height=750)

    active_user_table = ttk.Treeview(frame, selectmode='browse')

    customtkinter.CTkButton(frame, width=100, height=40, text='View Complete Information',
                            command=view_new_users_complete1).place(x=550, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text='View Payment History',
                            command=view_payment_history1).place(x=850, y=710)
    customtkinter.CTkButton(frame, width=100, height=40, text='View remaining Instalment details',
                            command=view_remaining_instalment_details).place(x=1050, y=710)

    active_user_table["columns"] = (
        "0", "1", "17", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "18", "19")
    active_user_table['show'] = 'headings'
    active_user_table.column("0", width=100, anchor=CENTER)
    active_user_table.column("1", width=100, anchor=CENTER)
    active_user_table.column("17", width=100, anchor=CENTER)
    active_user_table.column("2", width=120, anchor=CENTER)
    active_user_table.column("3", width=120, anchor=CENTER)
    active_user_table.column("4", width=100, anchor=CENTER)
    active_user_table.column("5", width=120, anchor=CENTER)
    active_user_table.column("6", width=150, anchor=CENTER)
    active_user_table.column("7", width=150, anchor=CENTER)
    active_user_table.column("8", width=100, anchor=CENTER)
    active_user_table.column("9", width=100, anchor=CENTER)
    active_user_table.column("10", width=100, anchor=CENTER)
    active_user_table.column("11", width=100, anchor=CENTER)
    active_user_table.column("12", width=70, anchor=CENTER)
    active_user_table.column("13", width=150, anchor=CENTER)
    active_user_table.column("14", width=100, anchor=CENTER)
    active_user_table.column("15", width=100, anchor=CENTER)
    active_user_table.column("16", width=200, anchor=CENTER)
    active_user_table.column("18", width=200, anchor=CENTER)
    active_user_table.column("19", width=200, anchor=CENTER)

    scrollbarX = ttk.Scrollbar(frame,
                               orient="horizontal",
                               command=active_user_table.xview)
    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=active_user_table.yview)
    active_user_table.place(x=300, y=20, height=640, width=1170)
    scrollbarY.place(x=288, y=20, height=640)
    scrollbarX.place(x=288, y=660, width=1170)
    active_user_table.configure(xscrollcommand=scrollbarX.set)
    active_user_table.configure(yscrollcommand=scrollbarY.set)

    active_user_table.heading("0", text="User Name")
    active_user_table.heading("1", text="Phone Number")
    active_user_table.heading("17", text="Loan Account Id")
    active_user_table.heading("2", text="Loan Name")
    active_user_table.heading("3", text="Principle amount")
    active_user_table.heading("4", text="Total amount")
    active_user_table.heading("5", text="Remaining amount")
    active_user_table.heading("6", text="Loan tenure in Years")
    active_user_table.heading("7", text="Loan tenure in Months")
    active_user_table.heading("8", text="Remaining tenure")
    active_user_table.heading("9", text="EMI")
    active_user_table.heading("10", text="Interest Type")
    active_user_table.heading("11", text="Interest")
    active_user_table.heading("12", text="Pre Payment Interest")
    active_user_table.heading("13", text="Late payment Interest")
    active_user_table.heading("14", text="Loan Start Date")
    active_user_table.heading("15", text="Loan End Date")
    active_user_table.heading("16", text="Total Amount Paid")
    active_user_table.heading("18", text="Total Sanctioned amount")
    active_user_table.heading("19", text="Last Payment date")
    view_active_user_table()


def view_history():
    global frame

    def pay_histry_table_load():
        cur = con.cursor()
        query = '''select * from history order by date_payed desc'''
        cur.execute(query, )
        result = cur.fetchall()
        result1 = list(result)

        for i in range(len(result)):
            remaining_instalment_table.insert("", "end",
                                              values=(
                                                  result1[i][3], result1[i][4], result1[i][5], result1[i][6],
                                                  result1[i][7], result1[i][8],
                                                  result1[i][9], result1[i][10]))

    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    Label(frame, text="HISTORY OF ALL THE USERS SORTED BASED ON DATE", fg='Green', bg='white',
          font=('times new roman', 20, "bold")). \
        place(x=400, y=10)

    def go_back_to_admin():
        admin_page()
        view_active_users()

    remaining_instalment_table = ttk.Treeview(frame, selectmode='browse')

    customtkinter.CTkButton(frame, width=100, height=40, text=' Back ', command=go_back_to_admin).place(x=1385, y=10)

    remaining_instalment_table["columns"] = ("0", "1", "2", "3", "4", "5", "6", "7")
    remaining_instalment_table['show'] = 'headings'
    remaining_instalment_table.column("0", width=120, anchor=CENTER)
    remaining_instalment_table.column("1", width=100, anchor=CENTER)
    remaining_instalment_table.column("2", width=120, anchor=CENTER)
    remaining_instalment_table.column("3", width=70, anchor=CENTER)
    remaining_instalment_table.column("4", width=100, anchor=CENTER)
    remaining_instalment_table.column("5", width=100, anchor=CENTER)
    remaining_instalment_table.column("6", width=100, anchor=CENTER)
    remaining_instalment_table.column("7", width=100, anchor=CENTER)

    scrollbarY = ttk.Scrollbar(frame,
                               orient="vertical",
                               command=remaining_instalment_table.yview)
    remaining_instalment_table.place(x=150, y=100, height=640, width=1170)
    scrollbarY.place(x=136, y=100, height=640)
    remaining_instalment_table.configure(yscrollcommand=scrollbarY.set)

    remaining_instalment_table.heading("0", text="Loan Account Number")
    remaining_instalment_table.heading("1", text="Date Payed")
    remaining_instalment_table.heading("2", text="Loan Name")
    remaining_instalment_table.heading("3", text="EMI")
    remaining_instalment_table.heading("4", text="Principal Paid")
    remaining_instalment_table.heading("5", text="Interest Paid")
    remaining_instalment_table.heading("6", text="Remaining Amount")
    remaining_instalment_table.heading("7", text="Total Amount Paid")

    for item in remaining_instalment_table.get_children():
        remaining_instalment_table.delete(item)
    pay_histry_table_load()


#########################################################################################################################
def admin_page():
    global frame, frame1

    cur = con.cursor()
    query = """select * from company WHERE id = %s"""
    cur.execute(query, (1,))
    myresult = cur.fetchone()

    root.title("Admin Page")
    frame = Frame(root, bg="white").place(x=250, y=0, width=1285, height=750)
    frame1 = Frame(root, width=250, height=740, bg="white").place(x=0, y=0)

    customtkinter.CTkButton(frame1, width=150, height=40, text='About Company', font=('times new roman', 15),
                            command=admin_page).place(x=100, y=50)
    customtkinter.CTkButton(frame1, width=150, height=40, text='   loan Schemes ', font=('times new roman', 15),
                            command=loandetails).place(x=100, y=100)
    customtkinter.CTkButton(frame1, width=150, height=40, text='    New Users   ', font=('times new roman', 15),
                            command=view_new_users).place(x=100, y=150)
    customtkinter.CTkButton(frame1, width=150, height=40, text=' Active Users   ', font=('times new roman', 15),
                            command=view_active_users).place(x=100, y=200)
    customtkinter.CTkButton(frame1, width=150, height=40, text=' Payment History   ', font=('times new roman', 15),
                            command=view_history).place(x=100, y=250)

    customtkinter.CTkButton(frame1, width=150, height=40, text='        Quit        ', font=('times new roman', 15),
                            command=exitfunc).place(x=100, y=650)
    customtkinter.CTkButton(frame1, width=150, height=40, text='      Log Out     ', font=('times new roman', 15),
                            command=start).place(x=100, y=600)

    customtkinter.CTkButton(frame, width=150, height=40, text='    Edit Details   ', font=('times new roman', 15),
                            command=edit_comp).place(x=1300, y=50)

    lab_name = Label(frame, text="Company Name", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_name.place(x=460, y=60)
    name_val = Label(frame, text=myresult[1], fg='black', bg='white',
                     font=('times new roman', 13))
    name_val.place(x=700, y=60)

    lab_address = Label(frame, text="Company address", fg='black', bg='white',
                        font=('times new roman', 13, "bold"))
    lab_address.place(x=460, y=110)
    address_value = Message(frame, width=500, text=myresult[2], fg='black', bg='white',
                            font=('times new roman', 13))
    address_value.place(x=700, y=110)

    lab_email = Label(frame, text="Email address", fg='black', bg='white',
                      font=('times new roman', 13, "bold"))
    lab_email.place(x=460, y=190)
    email_val = Label(frame, text=myresult[3], fg='black', bg='white',
                      font=('times new roman', 13))
    email_val.place(x=700, y=190)

    lab_mob1 = Label(frame, text="Mobile 1", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_mob1.place(x=460, y=240)
    mob1_val = Label(frame, text=myresult[4], fg='black', bg='white',
                     font=('times new roman', 13))
    mob1_val.place(x=700, y=240)

    lab_mob2 = Label(frame, text="Mobile 2", fg='black', bg='white',
                     font=('times new roman', 13, "bold"))
    lab_mob2.place(x=460, y=290)
    mob2_val = Label(frame, text=myresult[5], fg='black', bg='white',
                     font=('times new roman', 13))
    mob2_val.place(x=700, y=290)

    lab_discription = Label(frame, text="Company Description", fg='black', bg='white',
                            font=('times new roman', 13, "bold"))
    lab_discription.place(x=460, y=340)
    discription_val = Message(frame, text=myresult[6], width=500, fg='black', bg='white',
                              font=('times new roman', 13))
    discription_val.place(x=700, y=340)

    lab_goals = Label(frame, text="Company Goals", fg='black', bg='white',
                      font=('times new roman', 13, "bold"))
    lab_goals.place(x=460, y=540)
    goals_val = Message(frame, text=myresult[7], width=500, fg='black', bg='white',
                        font=('times new roman', 13))
    goals_val.place(x=700, y=540)


################################# register frame
reg_fullname = 0
reg_mobile1 = 0
reg_password = 0
reg_rePassword = 0



def register():
    def registerdb():
        mob1 = reg_mobile1.get()
        fname = reg_fullname.get()
        paswd = reg_password.get()
        paswd1 = reg_repassword.get()

        if (mob1 != "" and paswd != "" and paswd1 != "" and fname != ""):
            if (paswd == paswd1):
                cur = con.cursor()
                query = """select * from users WHERE userphone1 = %s"""
                cur.execute(query, (mob1,))
                myresult = cur.fetchone()
                if (myresult == None):
                    if (len(mob1) == 10 and len(paswd) >= 6):
                        cur = con.cursor()
                        query = """INSERT INTO users (username, userphone1, password, status, userphone2) VALUES (%s, %s, %s, %s, %s)"""
                        cur.execute(query, (fname, mob1, paswd, "NULL", "NULL"))
                        con.commit()
                        messagebox.showinfo("Sucess", "you registeration sucessfull")
                        start()
                    else:
                        messagebox.showerror("Invalid",
                                             "mobile number is not valid // the password is too short,give more than 6 chaacters")
                else:
                    messagebox.showerror("Invalid", "this mobile number already registered")
            else:
                messagebox.showerror("Invalid", "passwords are not equal")
        else:
            messagebox.showerror("Invalid", "Enter all the details")

    global frame
    global reg_fullname
    global reg_mobile1
    global reg_password
    global reg_repassword
    global img1
    root.title("Register")
    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    img1 = PhotoImage(file='registerimage.png')
    Label(frame, image=img1, bg='white').place(x=100, y=150)
    heading = Label(frame, text='Register', fg='#58a1f0', bg='white', border=1,
                    font=('times new roman', 30, 'bold')).place(x=950, y=100)

    label1 = Label(frame, text="Full Name", fg='black', bg='white',
                   font=('times new roman', 11))
    label1.place(x=800, y=200)
    reg_fullname = Entry(frame, width=30, fg='black', border=0, bg="white", font=('times new roman', 11))
    reg_fullname.place(x=1000, y=200)
    Frame(frame, width=240, height=2, bg='black').place(x=1000, y=230)

    label2 = Label(frame, text="Mobile Number", fg='black', bg='white',
                   font=('times new roman', 11))
    label2.place(x=800, y=280)
    reg_mobile1 = Entry(frame, width=30, fg='black', border=0, bg="white", font=('times new roman', 11))
    reg_mobile1.place(x=1000, y=280)
    Frame(frame, width=240, height=2, bg='black').place(x=1000, y=310)

    label3 = Label(frame, text="Password", fg='black', bg='white',
                   font=('times new roman', 11))
    label3.place(x=800, y=360)
    reg_password = Entry(frame, width=30, show="*", fg='black', border=0, bg="white",
                         font=('times new roman', 11))
    reg_password.place(x=1000, y=360)
    Frame(frame, width=240, height=2, bg='black').place(x=1000, y=390)

    label4 = Label(frame, text="Re-enter password", fg='black', bg='white',
                   font=('times new roman', 11))
    label4.place(x=800, y=440)
    reg_repassword = Entry(frame, show="*", width=30, fg='black', border=0, bg="white",
                           font=('times new roman', 11))
    reg_repassword.place(x=1000, y=440)
    Frame(frame, width=240, height=2, bg='black').place(x=1000, y=470)

    customtkinter.CTkButton(frame, width=300, text=' Register ', cursor='hand2', height=30,
                            font=('times new roman', 15), command=registerdb).place(
        x=875, y=550)
    customtkinter.CTkButton(frame, width=30, text=' Back ', cursor='hand2', height=30,
                            font=('times new roman', 15), command=start).place(x=1395, y=10)


########################################loginframe
loginphone1 = 0
loginpassword = 0


def on_enterpho(e):
    loginphone1.delete(0, 'end')


def on_leavepho(e):
    name = loginphone1.get()
    if name == '':
        loginphone1.insert(0, 'Phone Number')


def on_enterpass(e):
    loginpassword.delete(0, 'end')


def on_leavepass(e):
    name = loginpassword.get()
    if name == '':
        loginpassword.insert(0, 'Password')


def exitfunc():
    exit()


def start():
    global frame
    global loginphone1
    global loginpassword
    global img1
    frame = Frame(root, width=1535, height=780, bg="white").place(x=0, y=0)

    heading = Label(frame, text='Sign in', fg='#58a1f0', bg='white', border=1,
                    font=('times new roman', 30, 'bold')).place(x=800, y=200)

    img1 = PhotoImage(file='loginimage.png')
    Label(frame, image=img1, bg='white').place(x=100, y=150)

    loginphone1 = Entry(frame, width=30, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 13))
    loginphone1.place(x=720, y=300)
    loginphone1.insert(0, 'Phone Number')
    loginphone1.bind('<FocusIn>', on_enterpho)
    loginphone1.bind('<FocusOut>', on_leavepho)
    Frame(frame, width=320, height=2, bg='black').place(x=720, y=330)

    loginpassword = Entry(frame, show="*", width=30, fg='black', border=0, bg="white",
                          font=('times new roman', 13))
    loginpassword.place(x=720, y=380)
    loginpassword.insert(0, 'Password')
    loginpassword.bind('<FocusIn>', on_enterpass)
    loginpassword.bind('<FocusOut>', on_leavepass)
    Frame(frame, width=320, height=2, bg='black').place(x=720, y=410)

    customtkinter.CTkButton(frame, width=320, height=30, text='Sign in', font=('times new roman', 15),
                            command=sigin).place(x=720,
                                                 y=460)

    Label(frame, text="Don't have an account?", fg='black', bg='white',
          font=('times new roman', 13)).place(x=720, y=540)
    customtkinter.CTkButton(frame, width=30, text=' Sign up ', cursor='hand2', height=30,
                            font=('times new roman', 15), command=register).place(x=950, y=540)
    # command = lambda: register
    customtkinter.CTkButton(frame, width=100, height=30, text='Quit', command=exitfunc,
                            font=('times new roman', 15)).place(x=1395, y=10)


penalty_checker()
start()
root.mainloop()
