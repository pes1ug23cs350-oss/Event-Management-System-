import mysql.connector

# ----------------- Database Connection -----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Your_db_password",
        database="event_management"
    )

# ----------------- User Login -----------------
def login_user(email, password_hash):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE email=%s AND password=%s", (email, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user

# ----------------- Events -----------------
def get_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, event_name, event_date FROM Events")
    rows = cursor.fetchall()
    conn.close()
    return rows

def register_for_event(user_id, event_id, ticket_type):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('register_user_for_event', (user_id, event_id, ticket_type))
        conn.commit()
        return True, "Registered successfully!"
    except mysql.connector.Error as err:
        return False, f"Registration failed: {err}"
    finally:
        conn.close()

# ----------------- Payments -----------------
def make_payment(user_id, registration_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Payments (registration_id, amount, payment_date, payment_method, status)
            VALUES (%s, %s, NOW(), 'upi', 'completed')
        """, (registration_id, amount))
        conn.commit()
        return True, "Payment successful!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

# ----------------- Feedback -----------------
def give_feedback(user_id, event_id, rating, comments):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Feedback (user_id, event_id, rating, comments, feedback_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, event_id, rating, comments))
        conn.commit()
        return True, "Feedback submitted!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def get_tickets_for_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ticket_type, price FROM Tickets WHERE event_id=%s AND quantity_available>0", (event_id,))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def get_user_registrations(user_id):
    """Get all registrations for a user (for My Registrations view)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.registration_id, e.event_name, t.ticket_type, t.ticket_id, r.status
        FROM Registrations r
        JOIN Events e ON r.event_id = e.event_id
        JOIN Tickets t ON r.ticket_id = t.ticket_id
        WHERE r.user_id = %s
    """, (user_id,))
    regs = cursor.fetchall()
    conn.close()
    return regs

def get_unpaid_registrations(user_id):
    """Get only unpaid registrations for payment screen"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.registration_id, e.event_name, t.ticket_type, t.ticket_id, r.status
        FROM Registrations r
        JOIN Events e ON r.event_id = e.event_id
        JOIN Tickets t ON r.ticket_id = t.ticket_id
        WHERE r.user_id = %s AND r.status IN ('registered', 'pending')
    """, (user_id,))
    regs = cursor.fetchall()
    conn.close()
    return regs

def get_ticket_price(ticket_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM Tickets WHERE ticket_id=%s", (ticket_id,))
    price = cursor.fetchone()[0]
    conn.close()
    return price

def update_registration_status(registration_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Registrations SET status=%s WHERE registration_id=%s", (status, registration_id))
    conn.commit()
    conn.close()

def delete_registration(registration_id, user_id):
    """Delete a registration (only if status is 'registered')"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if registration belongs to user and is in 'registered' status
        cursor.execute("""
            SELECT status FROM Registrations 
            WHERE registration_id=%s AND user_id=%s
        """, (registration_id, user_id))
        result = cursor.fetchone()
        
        if not result:
            return False, "Registration not found or doesn't belong to you"
        
        if result[0] != 'registered':
            return False, "Cannot delete registration - payment already made or status changed"
        
        # Delete the registration
        cursor.execute("DELETE FROM Registrations WHERE registration_id=%s", (registration_id,))
        conn.commit()
        return True, "Registration deleted successfully"
    except mysql.connector.Error as err:
        return False, f"Error deleting registration: {err}"
    finally:
        cursor.close()
        conn.close()

def update_registration_ticket(registration_id, user_id, new_ticket_id):
    """Update ticket type for a registration (only if status is 'registered')"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if registration belongs to user and is in 'registered' status
        cursor.execute("""
            SELECT r.status, r.event_id, t.ticket_type 
            FROM Registrations r
            JOIN Tickets t ON r.ticket_id = t.ticket_id
            WHERE r.registration_id=%s AND r.user_id=%s
        """, (registration_id, user_id))
        result = cursor.fetchone()
        
        if not result:
            return False, "Registration not found or doesn't belong to you"
        
        if result[0] != 'registered':
            return False, "Cannot modify ticket - payment already made or status changed"
        
        # Verify new ticket belongs to same event and is available
        cursor.execute("""
            SELECT ticket_type, quantity_available 
            FROM Tickets 
            WHERE ticket_id=%s AND event_id=%s
        """, (new_ticket_id, result[1]))
        ticket_info = cursor.fetchone()
        
        if not ticket_info:
            return False, "Invalid ticket or ticket doesn't belong to this event"
        
        if ticket_info[1] <= 0:
            return False, f"Ticket type '{ticket_info[0]}' is sold out"
        
        # Update the registration
        cursor.execute("""
            UPDATE Registrations 
            SET ticket_id=%s 
            WHERE registration_id=%s
        """, (new_ticket_id, registration_id))
        conn.commit()
        return True, f"Ticket updated to '{ticket_info[0]}' successfully"
    except mysql.connector.Error as err:
        return False, f"Error updating ticket: {err}"
    finally:
        cursor.close()
        conn.close()

def update_feedback(user_id, event_id, rating, comments):
    """Update existing feedback for an event"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if feedback exists
        cursor.execute("""
            SELECT feedback_id FROM Feedback 
            WHERE user_id=%s AND event_id=%s
        """, (user_id, event_id))
        
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False, "No existing feedback found for this event"
        
        # Update feedback
        cursor.execute("""
            UPDATE Feedback 
            SET rating=%s, comments=%s, feedback_date=NOW()
            WHERE user_id=%s AND event_id=%s
        """, (rating, comments, user_id, event_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Feedback updated successfully"
    except mysql.connector.Error as err:
        cursor.close()
        conn.close()
        return False, f"Error updating feedback: {err}"

def delete_feedback(user_id, event_id):
    """Delete feedback for an event"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if feedback exists
        cursor.execute("""
            SELECT feedback_id FROM Feedback 
            WHERE user_id=%s AND event_id=%s
        """, (user_id, event_id))
        
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False, "No feedback found for this event"
        
        # Delete feedback
        cursor.execute("""
            DELETE FROM Feedback 
            WHERE user_id=%s AND event_id=%s
        """, (user_id, event_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Feedback deleted successfully"
    except mysql.connector.Error as err:
        cursor.close()
        conn.close()
        return False, f"Error deleting feedback: {err}"
    finally:
        cursor.close()
        conn.close()

def get_user_feedback(user_id, event_id):
    """Get existing feedback for an event"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rating, comments FROM Feedback 
        WHERE user_id=%s AND event_id=%s
    """, (user_id, event_id))
    result = cursor.fetchone()
    conn.close()
    return result  # Returns (rating, comments) or None



def make_payment(user_id, registration_id, amount, payment_method):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Insert payment record
        cursor.execute("""
            INSERT INTO Payments (registration_id, amount, payment_date, payment_method, status)
            VALUES (%s, %s, NOW(), %s, 'completed')
        """, (registration_id, amount, payment_method))
        conn.commit()
        return True, "Payment successful"
    except mysql.connector.Error as err:
        return False, f"Payment failed: {err}"
    finally:
        conn.close()


def get_attended_events(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.event_id, e.event_name
        FROM Registrations r
        JOIN Events e ON r.event_id = e.event_id
        WHERE r.user_id = %s AND r.status = 'attended'
    """, (user_id,))
    events = cursor.fetchall()
    conn.close()
    return events

def register_user(fname,lname, email, password_hash, phone, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Users (first_name,last_name, email, password, phone_no, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fname,lname, email, password_hash, phone, role))
        conn.commit()
        return True, "User registered successfully!"
    except mysql.connector.Error as err:
        return False, f"Registration failed: {err}"
    finally:
        conn.close()

def get_location_id(location_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT location_id FROM Locations WHERE location_name=%s", (location_name,))
    row = cursor.fetchone()

    if row:  # location already exists
        conn.close()
        return row[0]

    # Location doesn’t exist → ask for full details
    from tkinter import simpledialog
    address = simpledialog.askstring("Location", "Enter Address:")
    city = simpledialog.askstring("Location", "Enter City:")
    state = simpledialog.askstring("Location", "Enter State:")
    zip_code = simpledialog.askstring("Location", "Enter Zip Code:")

    cursor.execute(
        "INSERT INTO Locations (location_name, address, city, state, zip_code) VALUES (%s,%s,%s,%s,%s)",
        (location_name, address, city, state, zip_code)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


# ----------------- EVENT HELPERS -----------------
def create_event(organizer_id, name, description, date, location_id):
    """
    Insert a new event into Events table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Events (event_name, description, event_date, organizer_id, location_id) VALUES (%s, %s, %s, %s, %s)",
            (name, description, date, organizer_id, location_id)
        )
        conn.commit()
        event_id = cursor.lastrowid
        # CORRECTION: Return success status, a message, and the event_id
        return True, "Event created successfully!", event_id
    except mysql.connector.Error as err:
        # Return False on error with the error message
        return False, str(err), None
    finally:
        cursor.close()
        conn.close()

# In func.py, add these functions:

def get_organizer_events(organizer_id):
    """Retrieves all events owned by the specified organizer."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT event_id, event_name, event_date, description, location_id
        FROM Events 
        WHERE organizer_id = %s
    """, (organizer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# In func.py, add this new helper function:

def add_ticket_type(event_id, ticket_type, price, quantity):
    """Inserts a new ticket type for an event."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if ticket type already exists for this event
        cursor.execute(
            "SELECT 1 FROM Tickets WHERE event_id=%s AND ticket_type=%s",
            (event_id, ticket_type)
        )
        if cursor.fetchone():
            return False, f"Ticket type '{ticket_type}' already exists for this event."

        cursor.execute(
            """INSERT INTO Tickets (event_id, ticket_type, price, quantity_available) 
               VALUES (%s, %s, %s, %s)""",
            (event_id, ticket_type, price, quantity)
        )
        conn.commit()
        return True, f"Ticket type '{ticket_type}' added successfully!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def get_event_details(event_id):
    """Retrieves single event details for modification."""
    conn = get_connection()
    # Use dictionary=True for easier access by name in main.py
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT event_name, description, event_date 
        FROM Events 
        WHERE event_id = %s
    """, (event_id,))
    details = cursor.fetchone()
    conn.close()
    return details

def update_event(event_id, name, description, date):
    """Updates the core details of an event."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Events
            SET event_name = %s, description = %s, event_date = %s
            WHERE event_id = %s
        """, (name, description, date, event_id))
        conn.commit()
        return True, "Event updated successfully!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def add_event_schedule(event_id, start_time, end_time, activity_name, description):
    """
    Insert schedule entry for an event.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Event_Schedule (event_id, start_time, end_time, activity_name, description) VALUES (%s, %s, %s, %s, %s)",
        (event_id, start_time, end_time, activity_name, description)
    )
    conn.commit()
    cursor.close()
    conn.close()

def view_feedback(event_id, organizer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            U.user_id,                                    -- Attendee's ID
            CONCAT(U.first_name, ' ', U.last_name) AS user_full_name, -- FIXED: Concatenate first and last name
            F.event_id,                                   -- Event ID
            E.event_name,                                 -- Event Name
            F.rating,                                     -- Rating
            F.comments,                                   -- Comments
            F.feedback_date                               -- Date of Feedback
        FROM Feedback F
        JOIN Users U ON F.user_id = U.user_id
        JOIN Events E ON F.event_id = E.event_id
        WHERE E.organizer_id = %s
          AND (F.event_id = %s OR %s IS NULL)
        ORDER BY F.feedback_date DESC
    """, (organizer_id, event_id, event_id))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ----------------- Event Schedule -----------------
def manage_schedule(event_id, activity_time, activity_name, description=""): # Added description
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Added 'description' to the INSERT statement and values tuple
        cursor.execute("""
            INSERT INTO Event_Schedule (event_id, start_time, end_time, activity_name, description)
            VALUES (%s, %s, DATE_ADD(%s, INTERVAL 1 HOUR), %s, %s)
        """, (event_id, activity_time, activity_time, activity_name, description))
        conn.commit()
        return True, "Schedule updated!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

# Add a helper function to create a new sponsor
def create_new_sponsor(name, contact, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO Sponsors (sponsor_name, contact_person, email, phone_no) 
               VALUES (%s, %s, %s, %s)""",
            (name, contact, email, phone)
        )
        conn.commit()
        return True, cursor.lastrowid
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def get_all_sponsors():
    """Get all available sponsors from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sponsor_id, sponsor_name, contact_person, email FROM Sponsors ORDER BY sponsor_name")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ----------------- Sponsors -----------------
def view_organizer_sponsors(organizer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            E.event_id,
            E.event_name,
            S.sponsor_id,
            S.sponsor_name,
            S.contact_person,
            S.email,
            S.phone_no,
            ES.amount_contributed 
        FROM Events E
        JOIN Event_Sponsors ES ON E.event_id = ES.event_id
        JOIN Sponsors S ON ES.sponsor_id = S.sponsor_id
        WHERE E.organizer_id = %s
        ORDER BY E.event_id
    """, (organizer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# In func.py, add these functions:

def update_event_sponsor_amount(event_id, sponsor_id, organizer_id, new_amount):
    """
    Updates the contribution amount in Event_Sponsors, after verifying event ownership.
    This focuses ONLY on modifying amount_contributed.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check ownership (Essential security check)
        cursor.execute("SELECT 1 FROM Events WHERE event_id=%s AND organizer_id=%s", (event_id, organizer_id))
        if not cursor.fetchone():
            return False, "Error: You can only modify sponsors for events you organize."

        # Update the contribution amount
        cursor.execute("""
            UPDATE Event_Sponsors
            SET amount_contributed = %s
            WHERE event_id = %s AND sponsor_id = %s
        """, (new_amount, event_id, sponsor_id))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Sponsor not found for this event."

        return True, "Sponsor contribution amount updated successfully!"

    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def delete_event_sponsor(event_id, sponsor_id, organizer_id):
    """
    Deletes a sponsor from an event (deletes from Event_Sponsors), after verifying ownership.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check ownership (Essential security check)
        cursor.execute("SELECT 1 FROM Events WHERE event_id=%s AND organizer_id=%s", (event_id, organizer_id))
        if not cursor.fetchone():
            return False, "Error: You can only remove sponsors from events you organize."

        # Delete the entry from the junction table
        cursor.execute("""
            DELETE FROM Event_Sponsors
            WHERE event_id = %s AND sponsor_id = %s
        """, (event_id, sponsor_id))
        conn.commit()

        if cursor.rowcount == 0:
            return False, "Sponsor was not assigned to this event."

        return True, "Sponsor successfully removed from event."

    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

# In func.py, add these functions:

# In func.py, replace get_event_average_rating with this new comprehensive function:

def get_organizer_analytics(organizer_id):
    """Retrieves name, ID, Average Rating, and Total Revenue for all organized events."""
    conn = get_connection()
    # Use dictionary cursor for clear column access in Python
    cursor = conn.cursor(dictionary=True)

    # CRITICAL: Use the Stored Function and AVG() within the SELECT list
    cursor.execute("""
        SELECT
            E.event_id,
            E.event_name,
            -- Aggregate: Calculate Average Rating for each event
            IFNULL(AVG(F.rating), 0) AS avg_rating,
            -- Call Stored Function: Calculate Total Revenue for each event
            CalculateEventRevenue(E.event_id) AS total_revenue
        FROM Events E
        LEFT JOIN Feedback F ON E.event_id = F.event_id
        WHERE E.organizer_id = %s
        GROUP BY E.event_id, E.event_name
        ORDER BY E.event_id
    """, (organizer_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_events_with_no_sponsors(organizer_id):
    """Nested Query: Finds events organized by the user that have no sponsors."""
    conn = get_connection()
    cursor = conn.cursor()
    # Uses a NOT IN clause with a subquery to find event_ids that are not in Event_Sponsors
    cursor.execute("""
        SELECT event_id, event_name, event_date
        FROM Events
        WHERE organizer_id = %s
          AND event_id NOT IN (
            SELECT DISTINCT event_id
            FROM Event_Sponsors
          )
    """, (organizer_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# In func.py, add this function, perhaps near your create_event function:

def delete_event_cascading(event_id):
    """
    Deletes an event and all associated records (schedules, registrations, tickets, payments, sponsors).
    This function wraps all deletions in a single transaction.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Delete dependent records (Schedules, Sponsors, Tickets, Registrations)

        # Delete Event Schedules
        cursor.execute("DELETE FROM Event_Schedule WHERE event_id = %s", (event_id,))

        # Delete Event Sponsors mapping
        cursor.execute("DELETE FROM Event_Sponsors WHERE event_id = %s", (event_id,))

        # Delete Payments (Requires finding registrations first, but let's assume direct deletion or cascade is set up)
        # If your database has CASCADE DELETE set up on FKs: Registrations, Tickets, and Payments linked to them will cascade.
        # ASSUMPTION: Payments are linked to Registrations. We delete Registrations and Tickets.

        # Get registration IDs to delete associated payments if CASCADE is not set on payments
        cursor.execute("SELECT registration_id FROM Registrations WHERE event_id = %s", (event_id,))
        registration_ids = [row[0] for row in cursor.fetchall()]
        if registration_ids:
            # Delete Payments for these registrations
            cursor.execute(f"DELETE FROM Payments WHERE registration_id IN ({','.join(['%s']*len(registration_ids))})", tuple(registration_ids))

        # Delete Registrations
        cursor.execute("DELETE FROM Registrations WHERE event_id = %s", (event_id,))

        # Delete Tickets
        cursor.execute("DELETE FROM Tickets WHERE event_id = %s", (event_id,))

        # Delete Feedback
        cursor.execute("DELETE FROM Feedback WHERE event_id = %s", (event_id,))

        # 2. Delete the Event itself (must be last)
        cursor.execute("DELETE FROM Events WHERE event_id = %s", (event_id,))

        conn.commit()
        return True, f"Event ID {event_id} and all related data deleted successfully."

    except mysql.connector.Error as err:
        conn.rollback() # CRITICAL: Roll back all changes if any step fails
        return False, f"Database error during cascade delete: {str(err)}"

    finally:
        cursor.close()
        conn.close()

# Modified to accept amount_contributed
# In func.py

# In func.py, add this function, perhaps under the 'Events' section

def check_event_ownership(event_id, organizer_id):
    """Checks if the given organizer_id owns the event_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM Events WHERE event_id=%s AND organizer_id=%s",
        (event_id, organizer_id)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0 # Returns True if owned, False otherwise

# In func.py, add these functions, perhaps under the 'Event Schedule' section:

# In func.py, modify the function signature and add the check:

# In func.py, the function must look like this:

def get_event_revenue(event_id, organizer_id):  # CRITICAL: Accepts organizer_id
    """
    Calls the MySQL stored function to calculate total revenue,
    after verifying the organizer owns the event.
    """
    # 0. CRITICAL: Check event ownership locally before connecting
    if not check_event_ownership(event_id, organizer_id):
        return False, "Permission Denied: You can only calculate revenue for events you organize."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Calls the MySQL Stored Function
        cursor.execute(f"SELECT CalculateEventRevenue(%s)", (event_id,))
        revenue = cursor.fetchone()[0]
        return True, float(revenue)
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def get_event_schedules(event_id, organizer_id):
    """Retrieves all schedules for an event, but only if the organizer owns the event."""
    conn = get_connection()
    # Use dictionary cursor to easily get schedule_id and other details
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            ES.schedule_id, 
            ES.start_time, 
            ES.end_time, 
            ES.activity_name, 
            ES.description
        FROM Event_Schedule ES
        JOIN Events E ON ES.event_id = E.event_id
        WHERE ES.event_id = %s AND E.organizer_id = %s
        ORDER BY ES.start_time
    """, (event_id, organizer_id))
    schedules = cursor.fetchall()
    conn.close()
    return schedules

def update_schedule(schedule_id, start_time, activity_name, description):
    """Updates an existing schedule entry."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Note: We reuse the logic from manage_schedule to calculate end_time (+1 Hour)
        cursor.execute("""
            UPDATE Event_Schedule
            SET start_time = %s, 
                end_time = DATE_ADD(%s, INTERVAL 1 HOUR), 
                activity_name = %s, 
                description = %s
            WHERE schedule_id = %s
        """, (start_time, start_time, activity_name, description, schedule_id))
        conn.commit()
        return True, "Schedule updated successfully!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def delete_schedule(schedule_id):
    """Deletes an existing schedule entry."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Event_Schedule WHERE schedule_id = %s", (schedule_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False, "Schedule ID not found."
        return True, "Schedule deleted successfully!"
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()

def assign_sponsor(organizer_id, event_id, sponsor_id, amount_contributed):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Step 1: Check if the organizer OWNS the event (RELIABLE CHECK)
        cursor.execute(
            "SELECT COUNT(*) FROM Events WHERE event_id=%s AND organizer_id=%s",
            (event_id, organizer_id)
        )
        # Fetch the count (it will be a single integer)
        event_count = cursor.fetchone()[0]

        if event_count == 0:
            return False, "Error: You can only assign sponsors to events you organize."

        # Step 2: Check if sponsor is already assigned to THIS event
        cursor.execute("SELECT 1 FROM Event_Sponsors WHERE event_id=%s AND sponsor_id=%s", (event_id, sponsor_id))
        if cursor.fetchone():
            return False, "Sponsor is already assigned to this event."

        # Step 3: Insert event_sponsor mapping with contribution amount
        cursor.execute(
            """INSERT INTO Event_Sponsors (event_id, sponsor_id, amount_contributed)
               VALUES (%s, %s, %s)""",
            (event_id, sponsor_id, amount_contributed)
        )
        conn.commit()
        return True, "Sponsor assigned successfully!"

    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()
