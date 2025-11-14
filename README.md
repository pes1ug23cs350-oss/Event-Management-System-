## 🚀 Features

### 🔐 User Authentication
- Login via email + password  
- Passwords stored using **SHA-256 hashing**  
- Role-based access:
  - **Organizer** – manage events and tickets  
  - **Customer** – view events and book tickets  

---

### 📅 Event Management
Admins/Managers can:
- Create new events  
- Update event details  
- Delete events  
- View all events  
- Manage event date, venue, cost, ticket types, and available seats  

---

### 🎫 Ticket Booking System
Customers can:
- Browse available events  
- Choose ticket types (Regular / VIP / Student)  
- Book tickets  
- View booking confirmation  
- Automatic seat availability updates  

---

### 🧾 Attendee Management
- Automatic attendee record creation during booking  
- Smooth database-linked workflow  
- Maintains booking history and customer-event mapping  

---

### 💾 Database Integration
Uses a well-designed **MySQL database schema** including:
- `users`
- `events`
- `tickets`
- `bookings`
- `attendees`

The database ensures:
- Normalized structure  
- No data redundancy  
- Fast relational queries  

---

## 🛠️ Tech Stack

| Component   | Technology |
|-------------|------------|
| Language    | Python 3.x |
| GUI         | Tkinter, ttk |
| Database    | MySQL |
| Security    | SHA-256 password hashing |
| Modules     | mysql-connector-python, hashlib |

---

## 📦 Project Structure
