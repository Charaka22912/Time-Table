# Time Table Management System
A web-based Time Table Management System built using the Django framework. This system is designed for managing lecture schedules, monitoring lecturer workloads, and applying for leave, with features to ensure smooth and efficient academic management.

## Features

- **Dynamic Time Table Management**:
  - Add and edit schedules with conflict resolution.
  - Color-coded schedule tiles for different years.
  - Interactive calendar view for better visualization.

- **Lecturer Workload Monitoring**:
  - Displays the total lecture hours for each lecturer.
  - Highlights lecturers exceeding the workload limit of 20 hours.

- **Leave Application System**:
  - Allows lecturers to apply for leave.
  - Displays available lecturers for replacement based on day and time slot.

- **User Management**:
  - Admin login for managing schedules and users.
  - user registration via the application.
  - User authentication with a limit on login attempts for security.
   
## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap
- **Version Control**: Git, GitHub

   ## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/time-table-management-system.git
   
2.Create a virtual environment and activate it:
 ```bash
 python -m venv venv
 source venv/bin/activate  # For Linux/Mac
 venv\Scripts\activate
 ````

3.Install dependencies:
 ```bash
 pip install django
 ```

4.Apply migrations:
 ```bash
 py manage.py makemigrations
 py manage.py migrate
 ```
5.Run the development server:
 ```bash
 py manage.py runserver
 ```
## Admin Features
Manage schedules and monitor lecturer workloads via the admin panel.
Register and manage lecturers, halls, and subjects.
Apply for leave and view available lecturers for replacement.
Monitor personal workloads.


## Screenshots

![image](https://github.com/user-attachments/assets/abc1f6ec-437b-4a2c-95e0-92bb4769f3ba)
![image](https://github.com/user-attachments/assets/a555501e-ef6e-446c-b6df-823b4d45ad8e)
![image](https://github.com/user-attachments/assets/2be7633b-e335-4ee9-a19f-9945e59053fb)
![image](https://github.com/user-attachments/assets/34f7a4d1-fbd6-48c4-9c6b-760e00aeba3d)
![image](https://github.com/user-attachments/assets/03746f21-01d8-4df3-a3d6-da36aca6d557)
![image](https://github.com/user-attachments/assets/456da987-2358-43a1-bfc9-b27f4268dee8)




