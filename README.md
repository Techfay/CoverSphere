#########################################################

"CoverSphere - All in One Insurance Management System"

Coversphere is a powerful, full-stack web application designed to **digitally transform the end-to-end lifecycle of insurance operations** — from policy onboarding to claims approval — under one seamless platform.

Built with **Django**, **SQLite**, and **Python**, Coversphere is a scalable and secure solution for both **insurance providers** and **policyholders**, delivering intuitive access to policy management, claims processing, premium calculations, and real-time administrative control.

---

## Why Coversphere?

Insurance firms juggle multiple workflows — user onboarding, policy customization, claims handling — often spread across disconnected systems. **Coversphere unifies these processes into one dashboard**, reducing overhead, increasing transparency, and delivering a better user experience.

CoverSphere is designed with a role-based architecture, ensuring every stakeholder — be it a policyholder, agent, or admin — gets a tailored experience. The platform offers three distinct yet interconnected interfaces:

1. (Customer) User Interface (Policyholders)
Empowers end-users to:

🔐 Register and log into a secure portal

- Browse available insurance plans with category filters

- Purchase or subscribe to policies

- Use premium calculators to make informed decisions.

- File claims and track their progress

- View policy status (active, expired, pending) in real-time

2. Agent Dashboard
Optimized for insurance agents and advisors, enabling them to:

- View and manage assigned policies.

- Edit or remove plans (based on permissions)

= Monitor performance metrics:

** Total policies sold

** Total clients managed

** Claims processed

** Commission earned

- Update personal details and set active/inactive status.

- Access a clear, responsive table of all policies with actions for each.

This dashboard simplifies day-to-day operations for agents, helping them stay efficient and aligned with their goals.

3. Admin Interface (Internal Staff)

A powerful interface for platform management:

- Create, edit, or remove insurance policies.

- Manage user and agent access levels

- Approve or reject claims based on criteria

- Analyze trends, monitor system activity, and export reports

- Full control over operational aspects of the system

---

## Key Modules & Features

### (Customer) User Side (Policyholder Portal)

- **Register/Login** to a secure portal
- Browse and **purchase insurance policies**
- **Calculate premiums** dynamically
- **Submit claims** and track status
- Dashboard view of user policies and activity

### Agent Side (Sales & Policy Operations)

- **Login to agent dashboard
- **View and manage assigned policies
- **Edit/Delete policy details
- **Track performance: policies sold, claims processed, clients managed, and commissions earned
- **Update profile information and work status
- **Clean tabular layout for efficient navigation and policy actions

### Admin Side (Back Office)

- **Login to the admin dashboard**
- Manage all users and roles
- **Create/update/delete policies**
- View and **approve/reject claims**
- See aggregated data and quick stats (claims, users, etc.)

### 🔢 Premium Calculator

- Smart form-based input (age, plan, coverage)
- Instant premium estimates
- Can be extended to use custom logic or ML models

---

## Tech Stack

| Layer         | Tech Stack       |
|---------------|------------------|
| Backend       | Django (Python)  |
| Database      | SQLite           |
| Frontend      | HTML, CSS, Bootstrap |
| Auth          | Django's built-in auth |
| Dev Environment | VS Code / Cloud9     |

---

## Installation & Setup (Best Practices)

Step.1  Clone the Repository.

git clone https://github.com/Techfay/CoverSphere
cd CoverSphere

Step.2 Create a virtual Environment.

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Step.3 Install the required packages.

pip install -r requirements.txt

Step.4 Apply Migrations.

python manage.py makemigrations
python manage.py migrate

Step.6 Create superuser (Admin Login) ---Optional

python manage.py createsuperuser

Step.7  Run the development server.

python manage.py runserver

---

## License

This project is licensed under the [MIT License](LICENSE).

© 2025 Shivangi Pandey

## Author
Shivangi Pandey

