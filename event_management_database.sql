create database event_management;
use event_management;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_no VARCHAR(20),
    role ENUM('attendee', 'organizer') NOT NULL
);
CREATE TABLE Locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20)
);
CREATE TABLE Events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    location_id INT NOT NULL,
    organizer_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (organizer_id) REFERENCES Users(user_id)
);
CREATE TABLE Tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    ticket_type ENUM('regular','vip','student') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity_available INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);
CREATE TABLE Registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    ticket_id INT NOT NULL,
    registration_date DATE NOT NULL,
    status ENUM('registered','cancelled','attended') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id)
);
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    registration_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('credit_card','debit_card','paypal','upi') NOT NULL,
    status ENUM('pending','completed','failed') NOT NULL,
    FOREIGN KEY (registration_id) REFERENCES Registrations(registration_id)
);
CREATE TABLE Sponsors (
    sponsor_id INT AUTO_INCREMENT PRIMARY KEY,
    sponsor_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone_no VARCHAR(20),
    amount_contributed DECIMAL(15,2)
);
CREATE TABLE Event_Sponsors (
    event_id INT NOT NULL,
    sponsor_id INT NOT NULL,
    PRIMARY KEY (event_id, sponsor_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (sponsor_id) REFERENCES Sponsors(sponsor_id)
);
CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    rating INT NOT NULL,
    comments TEXT,
    feedback_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);
CREATE TABLE Event_Schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    description TEXT,
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);
INSERT INTO Users (first_name, last_name, email, phone_no, role) VALUES
('Rahul','Sharma','rahul.sharma@example.com','9876543210','attendee'),
('Priya','Mehta','priya.mehta@example.com','9123456780','organizer'),
('Amit','Verma','amit.verma@example.com','9988776655','attendee'),
('Sneha','Patil','sneha.patil@example.com','9090909090','attendee'),
('Vikram','Kapoor','vikram.kapoor@example.com','9123987654','organizer'),
('Ananya','Reddy','ananya.reddy@example.com','9876012345','attendee'),
('Rohit','Gupta','rohit.gupta@example.com','9812345678','attendee'),
('Kavya','Iyer','kavya.iyer@example.com','9900112233','organizer'),
('Suresh','Nair','suresh.nair@example.com','9877654321','attendee'),
('Meera','Joshi','meera.joshi@example.com','9012345678','organizer');

INSERT INTO Locations (location_name, address, city, state, zip_code) VALUES
('Grand Convention Center','123 MG Road','Bengaluru','Karnataka','560001'),
('Lotus Banquet Hall','45 Marine Drive','Mumbai','Maharashtra','400020'),
('Heritage Palace Grounds','Near Palace Road','Bengaluru','Karnataka','560052'),
('Sunset Gardens','22 Palm Beach Road','Navi Mumbai','Maharashtra','400706'),
('Royal Orchid Hotel','9 Residency Road','Bengaluru','Karnataka','560025'),
('Green Valley Resort','NH-7, Shamshabad','Hyderabad','Telangana','500108'),
('City Expo Center','120 Nehru Place','New Delhi','Delhi','110019'),
('Silver Leaf Auditorium','88 Park Street','Kolkata','West Bengal','700016'),
('Ocean View Hall','5 Beach Road','Chennai','Tamil Nadu','600004'),
('Amber Convention Hall','77 SG Highway','Ahmedabad','Gujarat','380015');


INSERT INTO Events (event_name, description, event_date, location_id, organizer_id) VALUES
('Tech Innovation Summit',
 'A conference showcasing the latest in technology and innovation.',
 '2025-10-15', 1, 2),

('Wedding Expo 2025',
 'An exhibition featuring wedding planners, designers, and vendors.',
 '2025-11-10', 2, 5),

('Food Carnival',
 'A celebration of street food and gourmet cuisines with live music.',
 '2025-12-01', 4, 8),

('Startup Pitch Fest',
 'Entrepreneurs pitch their ideas to investors and industry leaders.',
 '2025-10-25', 3, 2),

('Music Fiesta',
 'A grand concert featuring top Indian and international artists.',
 '2025-11-20', 5, 5),

('Literature & Arts Fest',
 'Talks, book readings, and art exhibitions by renowned personalities.',
 '2025-12-15', 7, 10),

('Comedy Night Live',
 'Stand-up comedy performances by popular comedians.',
 '2025-10-30', 9, 8),

('Business Leadership Forum',
 'Corporate leaders sharing strategies on business growth.',
 '2025-11-05', 6, 5),

('Cultural Extravaganza',
 'Dance, drama, and cultural programs showcasing traditions.',
 '2025-12-22', 8, 10),

('New Year Gala 2026',
 'A grand celebration to welcome the new year with music and dance.',
 '2025-12-31', 10, 2);
 
 INSERT INTO Tickets (event_id, ticket_type, price, quantity_available) VALUES
-- Event 1: Tech Innovation Summit
(1, 'regular', 500.00, 200),
(1, 'vip', 1500.00, 50),
(1, 'student', 300.00, 100),

-- Event 2: Wedding Expo 2025
(2, 'regular', 400.00, 300),
(2, 'vip', 1200.00, 80),
(2, 'student', 200.00, 150),

-- Event 3: Food Carnival
(3, 'regular', 200.00, 500),
(3, 'vip', 800.00, 100),
(3, 'student', 100.00, 250),

-- Event 4: Startup Pitch Fest
(4, 'regular', 600.00, 150),
(4, 'vip', 2000.00, 40),
(4, 'student', 250.00, 80),

-- Event 5: Music Fiesta
(5, 'regular', 1000.00, 400),
(5, 'vip', 3000.00, 100),
(5, 'student', 600.00, 200),

-- Event 6: Literature & Arts Fest
(6, 'regular', 300.00, 250),
(6, 'vip', 1000.00, 70),
(6, 'student', 150.00, 120),

-- Event 7: Comedy Night Live
(7, 'regular', 400.00, 200),
(7, 'vip', 1200.00, 60),
(7, 'student', 250.00, 90),

-- Event 8: Business Leadership Forum
(8, 'regular', 800.00, 180),
(8, 'vip', 2500.00, 50),
(8, 'student', 400.00, 70),

-- Event 9: Cultural Extravaganza
(9, 'regular', 350.00, 300),
(9, 'vip', 1200.00, 80),
(9, 'student', 180.00, 150),

-- Event 10: New Year Gala 2026
(10, 'regular', 1500.00, 500),
(10, 'vip', 5000.00, 150),
(10, 'student', 800.00, 200);

INSERT INTO Registrations (user_id, event_id, ticket_id, registration_date, status) VALUES
-- Rahul Sharma (attendee) registering for Tech Innovation Summit
(1, 1, 1, '2025-09-20', 'registered'),

-- Amit Verma (attendee) registering VIP ticket for Wedding Expo
(3, 2, 5, '2025-09-22', 'registered'),

-- Sneha Patil (attendee) student ticket for Food Carnival
(4, 3, 9, '2025-09-25', 'attended'),

-- Ananya Reddy (attendee) regular ticket for Startup Pitch Fest
(6, 4, 10, '2025-09-28', 'registered'),

-- Rohit Gupta (attendee) VIP ticket for Music Fiesta
(7, 5, 14, '2025-10-01', 'cancelled'),

-- Suresh Nair (attendee) student ticket for Literature & Arts Fest
(9, 6, 18, '2025-10-05', 'registered'),

-- Rahul Sharma (attendee) another event: Comedy Night Live
(1, 7, 19, '2025-10-08', 'registered'),

-- Amit Verma (attendee) Business Leadership Forum
(3, 8, 22, '2025-10-10', 'registered'),

-- Sneha Patil (attendee) Cultural Extravaganza
(4, 9, 25, '2025-10-12', 'attended'),

-- Ananya Reddy (attendee) New Year Gala 2026
(6, 10, 28, '2025-10-15', 'registered');


INSERT INTO Payments (registration_id, amount, payment_date, payment_method, status) VALUES
-- Rahul Sharma - Tech Innovation Summit
(1, 500.00, '2025-09-21', 'upi', 'completed'),

-- Amit Verma - Wedding Expo (VIP)
(2, 1200.00, '2025-09-23', 'credit_card', 'completed'),

-- Sneha Patil - Food Carnival (student)
(3, 100.00, '2025-09-25', 'debit_card', 'completed'),

-- Ananya Reddy - Startup Pitch Fest (regular)
(4, 600.00, '2025-09-29', 'paypal', 'pending'),

-- Rohit Gupta - Music Fiesta (VIP) – cancelled, but payment failed
(5, 3000.00, '2025-10-02', 'credit_card', 'failed'),

-- Suresh Nair - Literature & Arts Fest (student)
(6, 150.00, '2025-10-05', 'upi', 'completed'),

-- Rahul Sharma - Comedy Night Live (regular)
(7, 400.00, '2025-10-08', 'debit_card', 'completed'),

-- Amit Verma - Business Leadership Forum (regular)
(8, 800.00, '2025-10-11', 'paypal', 'completed'),

-- Sneha Patil - Cultural Extravaganza (VIP)
(9, 1200.00, '2025-10-12', 'credit_card', 'completed'),

-- Ananya Reddy - New Year Gala 2026 (student)
(10, 800.00, '2025-10-15', 'upi', 'pending');


INSERT INTO Sponsors (sponsor_name, contact_person, email, phone_no, amount_contributed) VALUES
('Infosys Ltd','Ravi Kumar','ravi.kumar@infosys.com','9876001122',500000.00),
('Tata Consultancy Services','Anjali Mehta','anjali.mehta@tcs.com','9823456710',750000.00),
('HDFC Bank','Suresh Rao','suresh.rao@hdfcbank.com','9811223344',300000.00),
('Amazon India','Priya Sharma','priya.sharma@amazon.in','9900112233',1000000.00),
('Flipkart Pvt Ltd','Amit Verma','amit.verma@flipkart.com','9123456789',600000.00),
('Coca Cola India','Sneha Nair','sneha.nair@coca-cola.com','9877665544',400000.00),
('PepsiCo India','Rahul Joshi','rahul.joshi@pepsico.com','9812334455',350000.00),
('Reliance Jio','Vikram Patel','vikram.patel@jio.com','9933445566',900000.00),
('Aditya Birla Group','Meera Iyer','meera.iyer@adityabirla.com','9898989898',450000.00),
('ICICI Bank','Kavya Reddy','kavya.reddy@icicibank.com','9776655443',550000.00);



INSERT INTO Event_Sponsors (event_id, sponsor_id) VALUES
-- Tech Innovation Summit
(1, 1), -- Infosys
(1, 2), -- TCS
(1, 4), -- Amazon

-- Wedding Expo 2025
(2, 3), -- HDFC Bank
(2, 5), -- Flipkart
(2, 6), -- Coca Cola

-- Food Carnival
(3, 6), -- Coca Cola
(3, 7), -- PepsiCo

-- Startup Pitch Fest
(4, 1), -- Infosys
(4, 8), -- Reliance Jio

-- Music Fiesta
(5, 6), -- Coca Cola
(5, 7), -- PepsiCo
(5, 9), -- Aditya Birla

-- Literature & Arts Fest
(6, 2), -- TCS
(6, 10), -- ICICI Bank

-- Comedy Night Live
(7, 7), -- PepsiCo
(7, 5), -- Flipkart

-- Business Leadership Forum
(8, 1), -- Infosys
(8, 3), -- HDFC Bank
(8, 8), -- Reliance Jio

-- Cultural Extravaganza
(9, 9), -- Aditya Birla
(9, 10), -- ICICI Bank

-- New Year Gala 2026
(10, 4), -- Amazon
(10, 8), -- Reliance Jio
(10, 6); -- Coca Cola

INSERT INTO Feedback (user_id, event_id, rating, comments, feedback_date) VALUES
-- Rahul Sharma - Tech Innovation Summit
(1, 1, 5, 'Excellent sessions, very informative!', '2025-10-16'),

-- Amit Verma - Wedding Expo
(3, 2, 4, 'Good variety of stalls, but could improve seating.', '2025-11-11'),

-- Sneha Patil - Food Carnival
(4, 3, 5, 'Amazing food options, loved the live music!', '2025-12-02'),

-- Ananya Reddy - Startup Pitch Fest
(6, 4, 4, 'Great networking opportunities, though a bit crowded.', '2025-10-26'),

-- Rohit Gupta - Music Fiesta
(7, 5, 3, 'Music was great, but sound system had issues.', '2025-11-21'),

-- Suresh Nair - Literature & Arts Fest
(9, 6, 5, 'Wonderful experience, inspiring speakers.', '2025-12-16'),

-- Rahul Sharma - Comedy Night Live
(1, 7, 4, 'Very funny performances, thoroughly enjoyed.', '2025-10-31'),

-- Amit Verma - Business Leadership Forum
(3, 8, 5, 'Well-organized, excellent keynote speakers.', '2025-11-06'),

-- Sneha Patil - Cultural Extravaganza
(4, 9, 5, 'Loved the cultural performances, great atmosphere.', '2025-12-23'),

-- Ananya Reddy - New Year Gala 2026
(6, 10, 4, 'Fantastic event, but the entry line was too long.', '2026-01-01');

INSERT INTO Event_Schedule (event_id, start_time, end_time, activity_name, description) VALUES
-- Tech Innovation Summit
(1, '2025-10-15 10:00:00', '2025-10-15 12:00:00', 'Keynote Session', 'Opening keynote on emerging technologies.'),
(1, '2025-10-15 14:00:00', '2025-10-15 16:00:00', 'Panel Discussion', 'Experts discuss AI, IoT, and Blockchain trends.'),

-- Wedding Expo 2025
(2, '2025-11-10 11:00:00', '2025-11-10 13:00:00', 'Bridal Wear Showcase', 'Latest bridal fashion designs displayed.'),
(2, '2025-11-10 15:00:00', '2025-11-10 17:00:00', 'Wedding Planning Workshop', 'Tips for budgeting and organizing weddings.'),

-- Food Carnival
(3, '2025-12-01 12:00:00', '2025-12-01 14:00:00', 'Street Food Fiesta', 'Popular street foods from across India.'),
(3, '2025-12-01 16:00:00', '2025-12-01 18:00:00', 'Live Music Show', 'Local bands performing while guests enjoy food.'),

-- Startup Pitch Fest
(4, '2025-10-25 10:30:00', '2025-10-25 12:30:00', 'Startup Pitches', '10 startups pitch their ideas to investors.'),
(4, '2025-10-25 14:00:00', '2025-10-25 16:00:00', 'Investor Networking', 'Investors and startups connect for funding talks.'),

-- Music Fiesta
(5, '2025-11-20 18:00:00', '2025-11-20 20:00:00', 'Opening Act', 'Performance by rising local artists.'),
(5, '2025-11-20 20:30:00', '2025-11-20 23:00:00', 'Headliner Concert', 'Main performance by top international band.'),

-- Literature & Arts Fest
(6, '2025-12-15 10:00:00', '2025-12-15 12:00:00', 'Author Talk', 'Discussion with bestselling authors.'),
(6, '2025-12-15 14:00:00', '2025-12-15 16:00:00', 'Art Exhibition', 'Showcasing contemporary Indian art.'),

-- Comedy Night Live
(7, '2025-10-30 19:00:00', '2025-10-30 20:30:00', 'Stand-up Set 1', 'Performance by emerging comedians.'),
(7, '2025-10-30 21:00:00', '2025-10-30 22:30:00', 'Stand-up Set 2', 'Headliner stand-up comedy performance.'),

-- Business Leadership Forum
(8, '2025-11-05 09:30:00', '2025-11-05 11:30:00', 'Keynote Address', 'Business leaders discuss growth strategies.'),
(8, '2025-11-05 13:00:00', '2025-11-05 15:00:00', 'Panel Session', 'Discussion on digital transformation in business.'),

-- Cultural Extravaganza
(9, '2025-12-22 17:00:00', '2025-12-22 19:00:00', 'Dance Performances', 'Classical and folk dances from various states.'),
(9, '2025-12-22 19:30:00', '2025-12-22 21:00:00', 'Drama Play', 'Theatrical performance based on Indian mythology.'),

-- New Year Gala 2026
(10, '2025-12-31 20:00:00', '2025-12-31 22:00:00', 'DJ Night', 'Top DJs playing party mixes.'),
(10, '2025-12-31 22:30:00', '2026-01-01 00:30:00', 'Countdown & Fireworks', 'Welcoming the new year with fireworks and celebration.');

ALTER TABLE Users
ADD COLUMN password VARCHAR(255) NOT NULL AFTER email;
UPDATE Users
SET password = SHA2('password123', 256);

-- 1. Add the amount_contributed column to the Event_Sponsors table
ALTER TABLE Event_Sponsors
ADD COLUMN amount_contributed DECIMAL(15,2) DEFAULT 0.00;

-- 2. Remove the amount_contributed column from the Sponsors table
ALTER TABLE Sponsors
DROP COLUMN amount_contributed;

CREATE TABLE temp_event_sponsors AS 
SELECT event_id, sponsor_id FROM event_sponsors;

TRUNCATE TABLE event_sponsors;
INSERT INTO event_sponsors (event_id, sponsor_id, amount_contributed)
SELECT event_id,
       sponsor_id,
       FLOOR(RAND() * (1000000 - 50000 + 1)) + 50000 AS amount_contributed
FROM temp_event_sponsors;

DROP TABLE temp_event_sponsors;

DELIMITER //
DELIMITER //

CREATE PROCEDURE register_user_for_event(
    IN p_user_id INT,
    IN p_event_id INT,
    IN p_ticket_type VARCHAR(50)
)
BEGIN
    DECLARE v_ticket_id INT;
    DECLARE v_quantity INT;

    -- Fetch ticket details
    SELECT ticket_id, quantity_available
    INTO v_ticket_id, v_quantity
    FROM Tickets
    WHERE event_id = p_event_id AND ticket_type = p_ticket_type
    LIMIT 1;

    -- Ticket not found
    IF v_ticket_id IS NULL THEN
        SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Ticket not found';
    END IF;

    -- Ticket sold out
    IF v_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ticket sold out';
    END IF;

    -- Register the user
    INSERT INTO Registrations (user_id, event_id, ticket_id, registration_date, status)
    VALUES (p_user_id, p_event_id, v_ticket_id, NOW(), 'registered');

END //

DELIMITER ;




DELIMITER //

CREATE TRIGGER prevent_duplicate_registration
BEFORE INSERT ON Registrations
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM Registrations 
        WHERE user_id = NEW.user_id AND event_id = NEW.event_id) > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User already registered for this event';
    END IF;
END;
//

DELIMITER //

CREATE TRIGGER update_status_after_payment
AFTER INSERT ON Payments
FOR EACH ROW
BEGIN
    UPDATE Registrations
    SET status = 'attended'
    WHERE registration_id = NEW.registration_id;
END
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER CheckTicketAvailability
BEFORE INSERT ON Registrations
FOR EACH ROW
BEGIN
    DECLARE available_quantity INT;

    -- Get the current quantity available for the ticket being registered
    SELECT quantity_available INTO available_quantity
    FROM Tickets
    WHERE ticket_id = NEW.ticket_id
    FOR UPDATE;

    -- Check if quantity is zero
    IF available_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Registration failed: Ticket type is sold out.';
    ELSE
        -- Decrement the quantity for the ticket type being used
        UPDATE Tickets
        SET quantity_available = quantity_available - 1
        WHERE ticket_id = NEW.ticket_id;
    END IF;
END //

DELIMITER ;


DELIMITER //

DELIMITER //

CREATE FUNCTION CalculateEventRevenue(eventID INT)
RETURNS DECIMAL(15, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_revenue DECIMAL(15, 2);

    -- Sum all completed payments linked to the event
    SELECT SUM(P.amount) INTO total_revenue
    FROM Payments P
    JOIN Registrations R 
        ON P.registration_id = R.registration_id
    WHERE R.event_id = eventID
      AND P.status = 'completed';

    -- Return 0.00 instead of NULL
    RETURN IFNULL(total_revenue, 0.00);
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER trg_registration_delete
AFTER DELETE ON Registrations
FOR EACH ROW
BEGIN
    -- Increase quantity of the ticket that was deleted
    UPDATE Tickets
    SET quantity_available = quantity_available + 1
    WHERE ticket_id = OLD.ticket_id;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER trg_ticket_change
AFTER UPDATE ON Registrations
FOR EACH ROW
BEGIN
    -- If ticket_id is modified
    IF NEW.ticket_id <> OLD.ticket_id THEN
    
        -- Increase quantity of old ticket
        UPDATE Tickets
        SET quantity_available = quantity_available + 1
        WHERE ticket_id = OLD.ticket_id;

        -- Decrease quantity of new ticket
        UPDATE Tickets
        SET quantity_available = quantity_available - 1
        WHERE ticket_id = NEW.ticket_id;

    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER trg_registration_cancel
AFTER UPDATE ON Registrations
FOR EACH ROW
BEGIN
    -- Only if status changed to cancelled
    IF NEW.status = 'cancelled' AND OLD.status <> 'cancelled' THEN
        UPDATE Tickets
        SET quantity_available = quantity_available + 1
        WHERE ticket_id = OLD.ticket_id;
    END IF;
END //

DELIMITER ;




