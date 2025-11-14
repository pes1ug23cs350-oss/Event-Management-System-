# 🎯 Event Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

*A comprehensive event management platform for organizing and attending events*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Database](#-database-schema) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Contributing](#-contributing)

---

## 🌟 Overview

The **Event Management System** is a feature-rich desktop application built with Python and MySQL that streamlines event organization and attendance. Whether you're an event organizer managing multiple events or an attendee looking for exciting experiences, this system provides an intuitive interface for all your event management needs.

### Key Highlights

✨ **Modern Dark Theme UI** - Beautiful, eye-friendly interface with custom widgets  
🔒 **Secure Authentication** - SHA-256 encrypted passwords and role-based access  
📊 **Real-time Analytics** - Track revenue, attendance, and event performance  
💳 **Integrated Payment System** - Multiple payment methods supported  
⭐ **Feedback Management** - Collect and manage attendee reviews  
💼 **Sponsor Management** - Track and manage event sponsorships  

---

## 🚀 Features

### 👤 For Attendees

#### 🔐 **User Authentication & Registration**
- Secure login with email and password
- Easy registration with role selection (Attendee/Organizer)
- Password encryption using SHA-256 hashing
- Session management

#### 📅 **Event Browsing & Registration**
- Browse all available events with detailed information
- View event dates, descriptions, and locations
- Register for events with different ticket types:
  - 🎫 **Regular** - Standard admission
  - 👑 **VIP** - Premium experience
  - 🎓 **Student** - Discounted student tickets
- Double-click quick registration

#### 🎫 **Registration Management**
- View all your event registrations
- Check registration status (Registered/Cancelled/Attended)
- Modify ticket types for existing registrations
- Cancel registrations when needed
- Real-time ticket availability tracking

#### 💳 **Payment Processing**
- Secure payment for event registrations
- Multiple payment methods:
  - Credit Card
  - Debit Card
  - PayPal
  - UPI
- Real-time price calculation
- Payment history tracking
- Automatic status updates after payment

#### ⭐ **Feedback & Reviews**
- Submit ratings (1-5 stars) for attended events
- Write detailed comments and reviews
- Edit existing feedback
- Delete feedback
- Help organizers improve future events

---

### 🎪 For Organizers

#### 📋 **Event Management**
- **Create Events** - Add new events with complete details
- **Update Events** - Modify event information anytime
- **Delete Events** - Remove events with cascade deletion of related data
- **View All Events** - Comprehensive event listing
- Event details include:
  - Event name and description
  - Date and time
  - Location information
  - Event schedules

#### 🎫 **Ticket Management**
- Create multiple ticket types per event
- Set individual pricing for each ticket type
- Manage ticket availability and quantities
- Automatic inventory tracking
- Real-time sold-out detection

#### 🗓️ **Event Scheduling**
- Create detailed event schedules
- Add multiple activities per event
- Set start and end times for each activity
- Modify existing schedules
- Delete schedule entries
- Activity descriptions and details

#### 💼 **Sponsor Management**
- Create new sponsor profiles
- Assign sponsors to events
- Track contribution amounts per sponsor
- Update sponsor contribution amounts
- Remove sponsor assignments
- View all event sponsorships
- Contact information management

#### 💬 **Feedback Monitoring**
- View feedback from attendees
- Check event ratings
- Read attendee comments
- Analyze feedback for improvements

#### 📈 **Analytics Dashboard**
- **Total Events** - Track all your events
- **Revenue Tracking** - Monitor total earnings
- **Average Ratings** - See overall event quality scores
- **Attendance Statistics** - View participation metrics
- Per-event analytics available

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.x | Core application logic |
| **GUI Framework** | Tkinter | Desktop user interface |
| **UI Components** | ttk (Themed Tkinter) | Enhanced widgets and styling |
| **Database** | MySQL | Data persistence and management |
| **Database Connector** | mysql-connector-python | Python-MySQL integration |
| **Security** | hashlib (SHA-256) | Password encryption |
| **Date/Time** | datetime | Date and time handling |

### Custom Components

- **HoverButton** - Interactive buttons with hover effects
- **SidebarButton** - Navigation menu buttons
- **ModernEntry** - Styled input fields with placeholder support
- **ScrollableFrame** - Scrollable content containers
- **Dark Theme** - Professionally designed dark color scheme

---

## 📦 Installation

### Prerequisites

Before installation, ensure you have:

- **Python 3.x** installed ([Download Python](https://www.python.org/downloads/))
- **MySQL Server** installed and running ([Download MySQL](https://dev.mysql.com/downloads/mysql/))
- **pip** package manager (included with Python)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Event-Management-System-
```

### Step 2: Install Python Dependencies

```bash
pip install mysql-connector-python
```

### Step 3: Configure Database Connection

**Important:** Edit the `func.py` file and update the database connection details:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",           # Your MySQL host (usually 'localhost')
        user="root",                # Your MySQL username (default: 'root')
        password="Your_db_password", # ⚠️ REPLACE with your actual MySQL password
        database="event_management"
    )
```

> **⚠️ Required Configuration:**  
> You **MUST** replace `"Your_db_password"` with your actual MySQL root password.  
> Example: If your MySQL password is `MyPass123`, change the line to:  
> ```python
> password="MyPass123",
> ```

---

## 🗄️ Database Setup

### Option 1: Automated Setup (Recommended)

Run the provided SQL script to automatically create and populate the database:

```bash
mysql -u your_username -p < event_management_database.sql
```

Enter your MySQL password when prompted.

### Option 2: Manual Setup

1. **Log into MySQL**:
```bash
mysql -u your_username -p
```

2. **Copy and paste** the contents of `event_management_database.sql` into your MySQL terminal.

### Database Structure

The system creates a complete database with:

- **10 Tables** - Users, Events, Locations, Tickets, Registrations, Payments, Sponsors, Event_Sponsors, Feedback, Event_Schedule
- **Sample Data** - Pre-populated with 10 users, 10 events, 10 locations, and related data
- **Triggers** - Automated business logic for data consistency
- **Stored Procedures** - Reusable database operations
- **Functions** - Custom calculations (e.g., revenue calculation)

### 🔑 Important: Default Passwords

> **⚠️ SECURITY NOTICE**  
> When you use the provided SQL script to create the database, **all existing users will have the default password**:
> 
> **Password: `password123`**
>
> **Pre-configured Users:**
> - rahul.sharma@example.com
> - priya.mehta@example.com  
> - amit.verma@example.com
> - sneha.patil@example.com
> - vikram.kapoor@example.com
> - ananya.reddy@example.com
> - rohit.gupta@example.com
> - kavya.iyer@example.com
> - suresh.nair@example.com
> - meera.joshi@example.com
>
> **🔒 Security Recommendation:**  
> For production use, you should:
> 1. Change all default passwords immediately
> 2. Implement a password reset mechanism
> 3. Use stronger password policies
> 4. Consider using bcrypt or Argon2 instead of SHA-256 for password hashing

---

## 🚀 Usage

### Starting the Application

```bash
python main.py
```

### First-Time Login

**Using Pre-configured Accounts:**

1. Select any email from the list above (e.g., `rahul.sharma@example.com`)
2. Enter password: `password123`
3. Click "LOGIN"

**Creating a New Account:**

1. Click "Register here" on the login screen
2. Fill in your details:
   - Full Name
   - Email Address
   - Phone Number
   - Password
   - Select Role (Attendee or Organizer)
3. Click "CREATE ACCOUNT"
4. Return to login and use your credentials

### Navigation

#### Attendee Dashboard
- 🏠 **Dashboard** - View your statistics and activity overview
- 📅 **Browse Events** - Explore and register for events
- 🎫 **My Registrations** - Manage your event registrations
- 💳 **Make Payment** - Process payments for registrations
- ⭐ **Give Feedback** - Rate and review attended events

#### Organizer Dashboard
- 🏠 **Dashboard** - View analytics and performance metrics
- 📋 **My Events** - Create and manage your events
- 🗓️ **Schedules** - Set up event timelines and activities
- 💼 **Sponsors** - Manage event sponsors and contributions
- 💬 **Feedback** - View attendee feedback
- 📈 **Analytics** - Detailed event performance reports

---

## 📊 Database Schema

### Core Tables

#### Users
Stores user account information and authentication data.
```sql
- user_id (PK)
- first_name
- last_name
- email (UNIQUE)
- password (SHA-256 hashed)
- phone_no
- role (attendee/organizer)
```

#### Events
Contains all event information.
```sql
- event_id (PK)
- event_name
- description
- event_date
- location_id (FK)
- organizer_id (FK)
```

#### Tickets
Manages ticket types and availability.
```sql
- ticket_id (PK)
- event_id (FK)
- ticket_type (regular/vip/student)
- price
- quantity_available
```

#### Registrations
Tracks user event registrations.
```sql
- registration_id (PK)
- user_id (FK)
- event_id (FK)
- ticket_id (FK)
- registration_date
- status (registered/cancelled/attended)
```

#### Payments
Records payment transactions.
```sql
- payment_id (PK)
- registration_id (FK)
- amount
- payment_date
- payment_method
- status (pending/completed/failed)
```

#### Event_Schedule
Manages event timelines and activities.
```sql
- schedule_id (PK)
- event_id (FK)
- start_time
- end_time
- activity_name
- description
```

#### Sponsors & Event_Sponsors
Handles sponsor information and event assignments.

---

## 🔒 Security

### Current Implementation

✅ **Password Hashing** - SHA-256 encryption for all passwords  
✅ **SQL Injection Prevention** - Parameterized queries  
✅ **Session Management** - User authentication tracking  
✅ **Role-Based Access** - Permission-based feature access  
✅ **Input Validation** - Data type and format checking  

### Recommendations for Production

🔐 **Enhanced Password Hashing** - Migrate to bcrypt or Argon2  
🔐 **HTTPS** - Use SSL/TLS for network communications  
🔐 **Rate Limiting** - Prevent brute force attacks  
🔐 **Session Timeout** - Auto-logout after inactivity  
🔐 **Audit Logging** - Track all user actions  

---

## 🎨 UI Features

### Modern Dark Theme
- Eye-friendly dark color palette
- Professional gradient backgrounds
- Consistent spacing and alignment
- Responsive component sizing

### Interactive Elements
- Hover effects on buttons
- Active state indicators
- Smooth transitions
- Tooltip-style help text

### User Experience
- Intuitive navigation
- Clear visual hierarchy
- Contextual help messages
- Error prevention dialogs
- Success/error notifications

---

## 🐛 Troubleshooting

### Common Issues

**"Access denied for user"**
- Check MySQL username and password in `func.py`
- Ensure MySQL server is running

**"No module named 'mysql.connector'"**
```bash
pip install mysql-connector-python
```

**"Database does not exist"**
- Run the database setup script
- Check database name in `func.py`

**Application won't start**
- Verify Python 3.x is installed
- Check all dependencies are installed
- Review console for error messages

---

## 📝 License

This project is available for educational and commercial use. Please ensure compliance with all third-party library licenses.

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Enhanced security features
- Mobile responsive version
- Web-based interface
- API development
- Additional payment gateways
- Email notifications
- Calendar integration
- Export functionality (PDF/Excel)

---

## 📞 Support

For issues, questions, or suggestions:

1. Check the troubleshooting section
2. Review closed issues on GitHub
3. Open a new issue with detailed information
4. Include error messages and steps to reproduce

---

## 🙏 Acknowledgments

- Python Software Foundation for Python
- Oracle Corporation for MySQL
- The open-source community for libraries and tools

---

<div align="center">

**Made with ❤️ for Event Organizers and Attendees**

⭐ Star this repository if you find it helpful!

</div>

