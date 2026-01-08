# Event Scheduler Application

## 📌 Project Description

The **Event Scheduler** is a Flask-based web application designed to manage events, resources, and their allocations efficiently. It allows users to create events, manage resources, allocate resources to events, and generate reports. The application uses **Flask**, **SQLite**, **SQLAlchemy**, and **Jinja2 templates** to provide a clean and user-friendly interface.

This project is suitable for learning and demonstrating CRUD operations, relational database design, and basic web application architecture using Python.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS (Jinja2 templates)
* **Database:** SQLite
* **ORM:** SQLAlchemy

---

## ⚙️ Installation Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd event_scheduler
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not available:

```bash
pip install flask flask-sqlalchemy
```

### 4️⃣ Database Setup

The application uses **SQLite**.

* Database file is located at:

```
event_scheduler/instance/events.db
```

* To initialize a fresh database, delete `events.db` and run the application once.

---

## ▶️ How to Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000/
```

---

## ✨ Features Implemented

* Create, view, and manage events
* Add and manage resources
* Allocate resources to events
* View allocations
* Generate event allocation reports
* Clean and responsive UI using templates

---

## 🗄️ Database Schema Diagram

```
+------------------+        +------------------+
|      Event       |        |     Resource     |
+------------------+        +------------------+
| id (PK)          |        | id (PK)          |
| name             |        | name             |
| date             |        | type             |
| location         |        | availability     |
+------------------+        +------------------+
        |                             |
        |                             |
        +-----------+   +-------------+
                    |   |
             +------------------------------+
             | EventResourceAllocation       |
             +------------------------------+
             | id (PK)                       |
             | event_id (FK)                 |
             | resource_id (FK)              |
             | quantity                      |
             +------------------------------+
```

---

## 🖼️ Screenshots

> Add screenshots of all major screens below.

* Home Page
* Events Page
* Add Event Page
* Resources Page
* Add Resource Page
* Resource Allocation Page
* Reports Page

```
/screenshots/home.png
/screenshots/events.png
/screenshots/resources.png
/screenshots/allocate.png
/screenshots/report.png
```

---

## 🎥 Demo Video (Mandatory)

Please provide a screen-recorded demo video showcasing:

* Application setup
* Adding events and resources
* Resource allocation
* Report generation

🔗 **Demo Video Link:**

```
[https://<your-video-link>](https://drive.google.com/file/d/1zcZHlbApYHhxiAYk4D-v0bu6QcM51c6Y/view?usp=sharing)
```

---

## 📄 License

This project is for educational purposes.

---

## 👤 Author

**Justin Cruz**

---
