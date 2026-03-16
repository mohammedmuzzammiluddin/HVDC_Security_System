## 🔗👨‍💻 Team

| Name                         | Roll Number  |
| ---------------------------- | ------------ |
| Mohammed Muzzammil Uddin     | 160922748121 |
| Syed Moosa                   | 160922748166 |
| Zuhaib Mohammed Abdul Waheed | 160922748160 |

**Project Guide:**
Mazher Uddin Associate Professor

**Co-Guide / HoD:**
Dr. Abdul Rasool Mohammed
Associate Professor & Head of Department, CSE (AIML)

**Institution:**
Lords Institute of Engineering and Technology, Hyderabad

---

# ⚡ HVDC CyberSec — Cyber-Physical Security Monitoring Platform

## 🧰 Tech Stack

* Python **3.11.9**
* Django **5.x**
* MySQL
* Bootstrap **5**
* scikit-learn *(Random Forest)*
* ReportLab *(PDF Generation)*

---

# ⚙️ Setup Instructions

## Step 1 — Open Project Folder

```
cd D:\HVDC_Security_System
```

## Step 2 — Activate Virtual Environment

```
venv\Scripts\activate
```

## Step 3 — Install Requirements

```
pip install -r requirements.txt
```

## Step 4 — Create MySQL Database

Open MySQL shell and run:

```sql
CREATE DATABASE hvdc_cybersec_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hvdc_user'@'localhost' IDENTIFIED BY 'hvdc_pass_2024';
GRANT ALL PRIVILEGES ON hvdc_cybersec_db.* TO 'hvdc_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## Step 5 — Run Migrations

```
python manage.py makemigrations accounts
python manage.py makemigrations monitoring
python manage.py makemigrations threat_detection
python manage.py makemigrations reports
python manage.py makemigrations simulation
python manage.py makemigrations alerts
python manage.py makemigrations vulnerability
python manage.py makemigrations defense
python manage.py makemigrations dashboard

python manage.py migrate
```

---

## Step 6 — Generate Dataset

```
python datasets/generate_dataset.py
```

---

## Step 7 — Train AI Model

```
python ml_models/train_model.py
```

---

## Step 8 — Load All Sample Data

Run Django shell:

```
python manage.py shell
```

Then paste the **entire dataset generation block** (the Python script you already included).

---

## Step 9 — Collect Static Files

```
python manage.py collectstatic --no-input
```

---

## Step 10 — Create Superuser (Admin)

```
python manage.py createsuperuser
```

```
Username : admin1
Email    : admin@hvdcsec.com
Password : Admin@1234
```

Set admin role:

```
python manage.py shell
```

```python
from accounts.models import CustomUser
u = CustomUser.objects.get(username='admin1')
u.role = 'admin'
u.save()
print("Admin role set:", u.is_admin())
exit()
```

---

## Step 11 — Run Development Server

```
python manage.py runserver
```

---

# 🌐 Access URLs

| Page             | URL                                      |
| ---------------- | ---------------------------------------- |
| Login            | http://127.0.0.1:8000/accounts/login/    |
| Register         | http://127.0.0.1:8000/accounts/register/ |
| Dashboard        | http://127.0.0.1:8000/home/              |
| HVDC Monitoring  | http://127.0.0.1:8000/monitoring/        |
| Threat Detection | http://127.0.0.1:8000/threat-detection/  |
| Reports          | http://127.0.0.1:8000/reports/           |
| Simulation       | http://127.0.0.1:8000/simulation/        |
| Alerts           | http://127.0.0.1:8000/alerts/            |
| Vulnerability    | http://127.0.0.1:8000/vulnerability/     |
| Defense          | http://127.0.0.1:8000/defense/           |
| Django Admin     | http://127.0.0.1:8000/admin/             |

---

# 🔑 Login Credentials

### Admin

```
Username : admin1
Password : Admin@1234
```

### Test Analyst User

```
Username : analyst1
Password : Analyst@1234
```

Register at:

```
/accounts/register/
```

Admin must set role to **analyst**.

---

### Test Viewer User

```
Username : viewer1
Password : Viewer@1234
```

Default role after registration = **viewer**

---

# 👥 User Roles

| Role    | Access                                          |
| ------- | ----------------------------------------------- |
| Admin   | Full system control, user management, AI models |
| Analyst | Monitoring, threats, reports, simulation        |
| Viewer  | Read-only dashboard and alerts                  |

---

# 📦 Project Apps

| App              | Purpose                          |
| ---------------- | -------------------------------- |
| accounts         | Authentication and roles         |
| dashboard        | Role-based dashboards            |
| monitoring       | HVDC sensor & network monitoring |
| threat_detection | AI attack detection              |
| reports          | PDF & CSV reporting              |
| simulation       | Attack scenario simulator        |
| alerts           | Real-time alerting               |
| vulnerability    | Risk & vulnerability management  |
| defense          | Security policies & mitigation   |

---

# 🤖 AI Model Details

| Property    | Value                                          |
| ----------- | ---------------------------------------------- |
| Algorithm   | Random Forest Classifier                       |
| Dataset     | 5,000 synthetic HVDC samples                   |
| Classes     | Normal, DoS, FDI, Command Manipulation, Replay |
| Features    | Electrical + Network parameters                |
| Accuracy    | ~97%                                           |
| Model Files | `ml_models/hvdc_rf_model.pkl`                  |

---

# ▶️ Every Time You Start Development

```
cd D:\HVDC_Security_System
venv\Scripts\activate
python manage.py runserver
```

Make sure **MySQL service is running**.

---

# 🛠 Troubleshooting

| Error                      | Fix                             |
| -------------------------- | ------------------------------- |
| django.db.OperationalError | Start MySQL                     |
| ModuleNotFoundError        | pip install -r requirements.txt |
| TemplateDoesNotExist       | Check templates folder          |
| No module named accounts   | Verify INSTALLED_APPS           |
| Table doesn't exist        | python manage.py migrate        |
| Model file missing         | Train AI model                  |
| Dashboard empty            | Run sample data script          |
| Reports empty              | Check reports views             |
| ImportError in admin.py    | Fix incorrect model imports     |
