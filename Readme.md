# 💰 **Finance Flow**

A comprehensive **desktop application** for managing **loan applications, processing, and tracking**, built with **Python and MySQL**.

---

## 🚀 **Features**

### 🔐 **User Management**
- ✅ Secure **login and registration** system
- 🏢 **Role-based access** (Admin/User)
- 📂 **Profile management** with **document uploads**

### 💳 **Loan Processing**
- 🏦 **Multiple loan schemes** management
- 📑 **Document verification** system
- 🧮 **Automated EMI calculations**
- ⚠️ **Penalty management**
- 📊 **Payment tracking**

### 📜 **Document Management**
- 🖼️ Support for multiple **document types** (.jpg, .png)
- 🔒 **Secure document storage**
- 👀 **Document preview** functionality
- 🔄 **Binary data conversion** for efficient storage

### 📈 **Financial Management**
- 🏦 **EMI calculation and tracking**
- 📜 **Payment history**
- ⚠️ **Penalty calculations**
- 💲 **Interest management**
- 💰 **Outstanding balance tracking**

---

## 🛠️ **Technical Stack**

- **Frontend**: Python **Tkinter, CustomTkinter**
- **Backend**: Python **3.x**
- **Database**: MySQL
- **Image Processing**: PIL (Python Imaging Library)
- **Date Processing**: Pandas, DateUtil

---

## 📌 **Prerequisites**

1. **Python 3.x**
2. **MySQL Server**
3. **Required Python packages:**
   ```bash
   pip install mysql-connector-python customtkinter pillow pandas python-dateutil
   ```

---

## ⚙️ **Installation**

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`

3. **Install required packages**:
   ```bash
   pip install mysql-connector-python customtkinter pillow pandas python-dateutil
   ```

4. **Configure database connection in `Main.py`**:
   ```python
   host='localhost'
   user='your_username'
   password='your_password'
   port='3306'
   database='finance_for_need'
   ```

5. **Run the application**:
   ```bash
   python Main.py
   ```

---

## 🎯 **Usage**

### 🔹 **Admin Features**
1. **Company Management**
   - 🏢 Edit company details
   - 📊 Manage loan schemes
   - 📜 View transaction history

2. **User Management**
   - 👥 View new applications
   - ✅ Process loan applications
   - 📌 Track active loans

3. **Loan Scheme Management**
   - ✍️ Create new loan schemes
   - 🛠️ Modify existing schemes
   - 💲 Set interest rates and terms

### 🔸 **User Features**
1. **Loan Application**
   - 📝 Apply for loans
   - 📑 Upload required documents
   - 🔄 Track application status

2. **Loan Management**
   - 🏦 View loan details
   - 💵 Track EMI payments
   - 📜 Access payment history
   - 🏁 View remaining installments

---

## 🔐 **Security Features**

- 🔑 **Password-protected access**
- 🔒 **Secure document storage**
- 👤 **Role-based authorization**
- ⏳ **Session management**

---

## 🗂️ **Database Schema**

See **`DatabaseStructure.txt`** for complete database setup commands.

### **Key Tables**
- `users` (**User management and authentication**)
- `customer` (**Loan customer information**)
- `loan` (**Loan scheme details**)
- `history` (**Payment transaction history**)
- `company` (**Company configuration**)

---

## 🚀 **Real-World Problem Solved**

🔹 **Manual loan processing** is time-consuming and prone to errors. **Finance Flow** automates loan applications, EMI calculations, and document verification.  
🔹 **Tracking financial transactions** can be difficult. This system provides a **detailed transaction history, penalty tracking, and EMI reminders**.  
🔹 **Security risks** with financial documents. The system ensures **secure storage and role-based access** to sensitive data.  

---


## 📜 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

You can connect with me through the following platforms:

- **GitHub**: [Bharath S J](https://github.com/Bharath-S-J)  
  Explore my repositories and projects.

- **LinkedIn**: [Bharath S J](https://www.linkedin.com/in/bharathsj
- )  
  Let's connect and discuss potential opportunities.

- **Portfolio**: [Portfolio Website](https://bharathsjweb.vercel.app/)  
  Check out my work and projects.

