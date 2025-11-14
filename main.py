import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from tkinter import font as tkfont
import hashlib
import func as db

# ==================== THEME CONFIGURATION ====================
class DarkTheme:
    BG_PRIMARY = "#0a0e27"
    BG_SECONDARY = "#16213e"
    BG_TERTIARY = "#1a2332"
    BG_CARD = "#1e2d3d"
    ACCENT = "#00d4aa"
    ACCENT_HOVER = "#00ffcc"
    ACCENT_DIM = "#008866"
    TEXT_PRIMARY = "#e8e8e8"
    TEXT_SECONDARY = "#9ca3af"
    TEXT_DIM = "#6b7280"
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"
    BORDER = "#2d3748"
    SIDEBAR = "#0f1419"

VALID_TICKET_TYPES = ['regular', 'vip', 'student']

# ==================== CUSTOM WIDGETS ====================
class HoverButton(tk.Button):
    def __init__(self, parent, **kwargs):
        self.default_bg = kwargs.pop('bg', DarkTheme.ACCENT)
        self.hover_bg = kwargs.pop('hover_bg', DarkTheme.ACCENT_HOVER)

        super().__init__(
            parent,
            bg=self.default_bg,
            fg=DarkTheme.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=12,
            cursor="hand2",
            activebackground=self.hover_bg,
            activeforeground=DarkTheme.TEXT_PRIMARY,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_bg

    def on_leave(self, e):
        self['bg'] = self.default_bg

class SidebarButton(tk.Button):
    def __init__(self, parent, **kwargs):
        self.is_active = False
        super().__init__(
            parent,
            bg=DarkTheme.SIDEBAR,
            fg=DarkTheme.TEXT_SECONDARY,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=15,
            cursor="hand2",
            anchor="w",
            activebackground=DarkTheme.BG_TERTIARY,
            activeforeground=DarkTheme.TEXT_PRIMARY,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if not self.is_active:
            self['bg'] = DarkTheme.BG_TERTIARY
            self['fg'] = DarkTheme.TEXT_PRIMARY

    def on_leave(self, e):
        if not self.is_active:
            self['bg'] = DarkTheme.SIDEBAR
            self['fg'] = DarkTheme.TEXT_SECONDARY

    def set_active(self):
        self.is_active = True
        self['bg'] = DarkTheme.ACCENT_DIM
        self['fg'] = DarkTheme.TEXT_PRIMARY

    def set_inactive(self):
        self.is_active = False
        self['bg'] = DarkTheme.SIDEBAR
        self['fg'] = DarkTheme.TEXT_SECONDARY

class ModernEntry(tk.Entry):
    def __init__(self, parent, placeholder="", **kwargs):
        defaults = {
            'bg': DarkTheme.BG_TERTIARY,
            'fg': DarkTheme.TEXT_PRIMARY,
            'font': ("Segoe UI", 10),
            'relief': tk.FLAT,
            'bd': 0,
            'insertbackground': DarkTheme.TEXT_PRIMARY
        }
        defaults.update(kwargs)

        self.placeholder = placeholder
        self.placeholder_color = DarkTheme.TEXT_DIM
        self.default_fg = defaults['fg']

        super().__init__(parent, **defaults)

        if placeholder:
            self.insert(0, placeholder)
            self['fg'] = self.placeholder_color
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg

    def on_focus_out(self, e):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, bg=kwargs.get('bg', DarkTheme.BG_PRIMARY),
                               highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview,
                                bg=DarkTheme.BG_TERTIARY, troughcolor=DarkTheme.BG_PRIMARY,
                                activebackground=DarkTheme.ACCENT)
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get('bg', DarkTheme.BG_PRIMARY))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def style_treeview():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Treeview",
                    background=DarkTheme.BG_CARD,
                    foreground=DarkTheme.TEXT_PRIMARY,
                    fieldbackground=DarkTheme.BG_CARD,
                    borderwidth=0,
                    font=("Segoe UI", 9))

    style.map('Treeview',
              background=[('selected', DarkTheme.ACCENT_DIM)],
              foreground=[('selected', DarkTheme.TEXT_PRIMARY)])

    style.configure("Treeview.Heading",
                    background=DarkTheme.BG_SECONDARY,
                    foreground=DarkTheme.TEXT_PRIMARY,
                    relief=tk.FLAT,
                    font=("Segoe UI", 10, "bold"))

    style.map("Treeview.Heading",
              background=[('active', DarkTheme.BORDER)])

    style.configure("TCombobox",
                    fieldbackground=DarkTheme.BG_TERTIARY,
                    background=DarkTheme.BG_TERTIARY,
                    foreground=DarkTheme.TEXT_PRIMARY,
                    arrowcolor=DarkTheme.TEXT_PRIMARY,
                    borderwidth=0)

# ==================== MAIN APPLICATION ====================
class EventManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg=DarkTheme.BG_PRIMARY)
        self.root.resizable(False, False)

        style_treeview()

        self.current_user = None
        self.current_role = None
        self.sidebar_buttons = []

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================== LOGIN SCREEN ====================
    def show_login(self):
        self.clear_window()

        # Split screen layout
        left_frame = tk.Frame(self.root, bg=DarkTheme.SIDEBAR, width=700)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(self.root, bg=DarkTheme.BG_PRIMARY, width=700)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        # Left side - Branding
        brand_container = tk.Frame(left_frame, bg=DarkTheme.SIDEBAR)
        brand_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(brand_container, text="🎯", bg=DarkTheme.SIDEBAR,
                font=("Segoe UI", 80)).pack()

        tk.Label(brand_container, text="Event Management", bg=DarkTheme.SIDEBAR,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 28, "bold")).pack(pady=(20, 5))

        tk.Label(brand_container, text="System", bg=DarkTheme.SIDEBAR,
                fg=DarkTheme.ACCENT, font=("Segoe UI", 28, "bold")).pack()

        tk.Label(brand_container, text="Organize • Attend • Experience",
                bg=DarkTheme.SIDEBAR, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 12)).pack(pady=(30, 0))

        # Right side - Login Form
        form_container = tk.Frame(right_frame, bg=DarkTheme.BG_PRIMARY)
        form_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(form_container, text="Welcome Back!", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(pady=(0, 10))

        tk.Label(form_container, text="Please login to continue",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 11)).pack(pady=(0, 40))

        # Email
        tk.Label(form_container, text="EMAIL ADDRESS", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        email_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        email_frame.pack(fill=tk.X, pady=(0, 25))

        self.email_entry = ModernEntry(email_frame, placeholder="Enter your email")
        self.email_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Password
        tk.Label(form_container, text="PASSWORD", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        password_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        password_frame.pack(fill=tk.X, pady=(0, 35))

        self.password_entry = ModernEntry(password_frame, show="●", placeholder="Enter your password")
        self.password_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())



        # Login Button
        HoverButton(form_container, text="LOGIN", command=self.login, width=30).pack(pady=(0, 20))

        # Register Link
        register_frame = tk.Frame(form_container, bg=DarkTheme.BG_PRIMARY)
        register_frame.pack()

        tk.Label(register_frame, text="Don't have an account?",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 9)).pack(side=tk.LEFT)

        register_btn = tk.Label(register_frame, text=" Register here",
                               bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.ACCENT,
                               font=("Segoe UI", 9, "bold"), cursor="hand2")
        register_btn.pack(side=tk.LEFT)
        register_btn.bind("<Button-1>", lambda e: self.show_register())

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in ["", "Enter your email"] or password in ["", "Enter your password"]:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = db.login_user(email, password_hash)

        if user:
            self.current_user = user['user_id']
            self.current_role = user['role']
            messagebox.showinfo("Success", f"Welcome {user['role'].title()}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def show_register(self):
        self.clear_window()

        # Split screen layout
        left_frame = tk.Frame(self.root, bg=DarkTheme.SIDEBAR, width=700)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(self.root, bg=DarkTheme.BG_PRIMARY, width=700)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)

        # Left side - Branding
        brand_container = tk.Frame(left_frame, bg=DarkTheme.SIDEBAR)
        brand_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(brand_container, text="🎯", bg=DarkTheme.SIDEBAR,
                font=("Segoe UI", 80)).pack()

        tk.Label(brand_container, text="Join Us", bg=DarkTheme.SIDEBAR,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 28, "bold")).pack(pady=(20, 5))

        tk.Label(brand_container, text="Create Your Account", bg=DarkTheme.SIDEBAR,
                fg=DarkTheme.ACCENT, font=("Segoe UI", 28, "bold")).pack()

        tk.Label(brand_container, text="Start organizing or attending events today",
                bg=DarkTheme.SIDEBAR, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 12)).pack(pady=(30, 0))

        # Right side - Registration Form
        form_container = tk.Frame(right_frame, bg=DarkTheme.BG_PRIMARY)
        form_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(form_container, text="Create Account", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(pady=(0, 10))

        tk.Label(form_container, text="Fill in your details to register",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 11)).pack(pady=(0, 30))

        # Name
        tk.Label(form_container, text="FULL NAME", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        name_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        name_frame.pack(fill=tk.X, pady=(0, 20))

        name_entry = ModernEntry(name_frame, placeholder="Enter your full name")
        name_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Email
        tk.Label(form_container, text="EMAIL ADDRESS", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        email_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        email_frame.pack(fill=tk.X, pady=(0, 20))

        email_entry = ModernEntry(email_frame, placeholder="Enter your email")
        email_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Phone Number (NEW ENTRY ADDED HERE)
        tk.Label(form_container, text="PHONE NUMBER", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        phone_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        phone_frame.pack(fill=tk.X, pady=(0, 20))

        phone_entry = ModernEntry(phone_frame, placeholder="Enter your phone number")
        phone_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Password
        tk.Label(form_container, text="PASSWORD", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        password_frame = tk.Frame(form_container, bg=DarkTheme.BG_TERTIARY, bd=0)
        password_frame.pack(fill=tk.X, pady=(0, 20))

        password_entry = ModernEntry(password_frame, show="●", placeholder="Create a password")
        password_entry.pack(fill=tk.X, padx=15, pady=12, ipady=5)

        # Role Selection
        tk.Label(form_container, text="REGISTER AS", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 8))

        role_frame = tk.Frame(form_container, bg=DarkTheme.BG_PRIMARY)
        role_frame.pack(fill=tk.X, pady=(0, 25))

        role_var = tk.StringVar(value="attendee")

        attendee_rb = tk.Radiobutton(role_frame, text="🎫 Attendee (Join Events)",
                                     variable=role_var, value="attendee",
                                     bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_PRIMARY,
                                     selectcolor=DarkTheme.BG_TERTIARY, font=("Segoe UI", 10),
                                     activebackground=DarkTheme.BG_PRIMARY,
                                     activeforeground=DarkTheme.ACCENT)
        attendee_rb.pack(anchor=tk.W, pady=5)

        organizer_rb = tk.Radiobutton(role_frame, text="🎪 Organizer (Create Events)",
                                      variable=role_var, value="organizer",
                                      bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_PRIMARY,
                                      selectcolor=DarkTheme.BG_TERTIARY, font=("Segoe UI", 10),
                                      activebackground=DarkTheme.BG_PRIMARY,
                                      activeforeground=DarkTheme.ACCENT)
        organizer_rb.pack(anchor=tk.W, pady=5)

        def register_user():
            # Use nonlocal to access the entry widgets defined in the outer function (show_register)
            nonlocal name_entry, email_entry, password_entry, phone_entry, role_var

            # 1. Split the name into first and last name
            full_name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            phone = phone_entry.get()  # 2. Added phone entry
            role = role_var.get()

            # Basic input validation
            if full_name in ["", "Enter your full name"] or \
               email in ["", "Enter your email"] or \
               password in ["", "Create a password"] or \
               phone in ["", "Enter your phone number"]: # Updated validation
                messagebox.showerror("Error", "Please fill in all fields")
                return

            # Attempt to split full name. Assuming the first word is the first name and the rest is the last name.
            # You might want more robust splitting or separate input fields in a real application.
            name_parts = full_name.split(maxsplit=1)
            if len(name_parts) == 2:
                fname = name_parts[0]
                lname = name_parts[1]
            elif len(name_parts) == 1:
                fname = name_parts[0]
                lname = "" # Use an empty string for last name if only one name is entered
            else:
                messagebox.showerror("Error", "Please enter a valid full name.")
                return

            # Hash the password
            # 3. Changed variable name to 'password_hash' for clarity, though it was already correct.
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            # --- Call database function to register user ---
            try:
                # Note: You need to replace this block with a call to your backend function
                # which takes fname, lname, email, password_hash, phone, role

                # Example using the provided backend signature:
                # success, message = db.register_user(fname, lname, email, password_hash, phone, role)

                # Mock database check (since I don't have your db module)
                conn = db.get_connection()
                cursor = conn.cursor()

                # Check if email already exists
                cursor.execute("SELECT email FROM Users WHERE email=%s", (email,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Email already registered")
                    cursor.close()
                    conn.close()
                    return

                # Insert new user - UPDATED QUERY AND TUPLE
                cursor.execute(
                    "INSERT INTO Users (first_name, last_name, email, password, phone_no, role) VALUES (%s, %s, %s, %s, %s, %s)",
                    (fname, lname, email, password_hash, phone, role) # **KEY CHANGE: passing all 6 arguments**
                )
                conn.commit()
                cursor.close()
                conn.close()
                # End Mock

                messagebox.showinfo("Success", f"Account created successfully as {role.title()}!\nPlease login to continue.")
                self.show_login()

            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")

        # Bind Enter key
        password_entry.bind("<Return>", lambda e: register_user())

        # Register Button
        HoverButton(form_container, text="CREATE ACCOUNT", command=register_user, width=30).pack(pady=(0, 20))

        # Login Link
        login_frame = tk.Frame(form_container, bg=DarkTheme.BG_PRIMARY)
        login_frame.pack()

        tk.Label(login_frame, text="Already have an account?",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 9)).pack(side=tk.LEFT)

        login_btn = tk.Label(login_frame, text=" Login here",
                            bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.ACCENT,
                            font=("Segoe UI", 9, "bold"), cursor="hand2")
        login_btn.pack(side=tk.LEFT)
        login_btn.bind("<Button-1>", lambda e: self.show_login())

    # ==================== DASHBOARD ====================
    def show_dashboard(self):
        self.clear_window()

        # Sidebar
        sidebar = tk.Frame(self.root, bg=DarkTheme.SIDEBAR, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Sidebar Header
        header = tk.Frame(sidebar, bg=DarkTheme.SIDEBAR, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="🎯", bg=DarkTheme.SIDEBAR, font=("Segoe UI", 30)).pack(pady=(15, 0))
        tk.Label(header, text="EMS", bg=DarkTheme.SIDEBAR, fg=DarkTheme.ACCENT,
                font=("Segoe UI", 14, "bold")).pack()

        # User Info
        user_frame = tk.Frame(sidebar, bg=DarkTheme.BG_TERTIARY, height=80)
        user_frame.pack(fill=tk.X, pady=(0, 20))
        user_frame.pack_propagate(False)

        tk.Label(user_frame, text=f"👤 {self.current_role.title()}", bg=DarkTheme.BG_TERTIARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))
        tk.Label(user_frame, text=f"ID: {self.current_user}", bg=DarkTheme.BG_TERTIARY,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 9)).pack()

        # Menu Items
        menu_frame = tk.Frame(sidebar, bg=DarkTheme.SIDEBAR)
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Main Content Area
        self.main_content = tk.Frame(self.root, bg=DarkTheme.BG_PRIMARY)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        if self.current_role == "attendee":
            self.setup_attendee_menu(menu_frame)
        elif self.current_role == "organizer":
            self.setup_organizer_menu(menu_frame)

        # Logout at bottom
        logout_frame = tk.Frame(sidebar, bg=DarkTheme.SIDEBAR, height=80)
        logout_frame.pack(side=tk.BOTTOM, fill=tk.X)
        logout_frame.pack_propagate(False)

        logout_btn = SidebarButton(logout_frame, text="🚪  Logout", command=self.logout)
        logout_btn.pack(fill=tk.X, padx=10, pady=10)

    def setup_attendee_menu(self, menu_frame):
        menus = [
            ("🏠  Dashboard", self.show_attendee_dashboard),
            ("📅  Browse Events", self.show_browse_events),
            ("🎫  My Registrations", self.show_my_registrations),
            ("💳  Make Payment", self.show_payment_screen),
            ("⭐  Give Feedback", self.show_feedback_screen),
        ]

        for text, command in menus:
            btn = SidebarButton(menu_frame, text=text, command=command)
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.sidebar_buttons.append(btn)

        self.show_attendee_dashboard()

    def setup_organizer_menu(self, menu_frame):
        menus = [
            ("🏠  Dashboard", self.show_organizer_dashboard),
            ("📋  My Events", self.show_my_events),
            ("🗓️  Schedules", self.show_schedules),
            ("💼  Sponsors", self.show_sponsors),
            ("💬  Feedback", self.show_organizer_feedback),
            ("📈  Analytics", self.show_analytics),
        ]

        for text, command in menus:
            btn = SidebarButton(menu_frame, text=text, command=command)
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.sidebar_buttons.append(btn)

        self.show_organizer_dashboard()

    def set_active_menu(self, index):
        for i, btn in enumerate(self.sidebar_buttons):
            if i == index:
                btn.set_active()
            else:
                btn.set_inactive()

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.current_role = None
            self.sidebar_buttons = []
            self.show_login()

    # ==================== ATTENDEE SCREENS ====================
    def show_attendee_dashboard(self):
        self.set_active_menu(0)
        self.clear_content()

        # Header
        tk.Label(self.main_content, text="Dashboard", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 10))

        tk.Label(self.main_content, text="Welcome back! Here's your activity overview.",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 11)).pack(anchor=tk.W, padx=40, pady=(0, 30))

        # Stats Cards
        cards_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        cards_frame.pack(fill=tk.X, padx=40, pady=20)

        # Get stats
        regs = db.get_user_registrations(self.current_user)
        attended = db.get_attended_events(self.current_user)

        stats = [
            ("🎫", "Total Registrations", len(regs) if regs else 0, DarkTheme.ACCENT),
            ("✅", "Attended Events", len(attended) if attended else 0, DarkTheme.SUCCESS),
            ("📅", "Available Events", len(db.get_events()) if db.get_events() else 0, DarkTheme.WARNING),
        ]

        for icon, label, value, color in stats:
            card = tk.Frame(cards_frame, bg=DarkTheme.BG_CARD, bd=0, relief=tk.FLAT)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

            tk.Label(card, text=icon, bg=DarkTheme.BG_CARD, font=("Segoe UI", 36)).pack(pady=(25, 10))
            tk.Label(card, text=str(value), bg=DarkTheme.BG_CARD, fg=color,
                    font=("Segoe UI", 32, "bold")).pack()
            tk.Label(card, text=label, bg=DarkTheme.BG_CARD, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 10)).pack(pady=(5, 25))

    def show_browse_events(self):
        self.set_active_menu(1)
        self.clear_content()

        # Header
        header_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        header_frame.pack(fill=tk.X, padx=40, pady=(30, 20))

        tk.Label(header_frame, text="Browse Events", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(side=tk.LEFT)

        # Get events
        events = db.get_events()

        if not events:
            tk.Label(self.main_content, text="No events available at the moment",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        # Table frame
        table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("ID", "Name", "Date", "Actions")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        tree.heading("ID", text="Event ID")
        tree.column("ID", width=100, anchor=tk.CENTER)
        tree.heading("Name", text="Event Name")
        tree.column("Name", width=500)
        tree.heading("Date", text="Date")
        tree.column("Date", width=200, anchor=tk.CENTER)
        tree.heading("Actions", text="Actions")
        tree.column("Actions", width=200, anchor=tk.CENTER)

        for row in events:
            tree.insert("", tk.END, values=(row[0], row[1], row[2], "→ Register"))

        tree.bind("<Double-1>", lambda e: self.register_for_event_inline(tree))

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons for sponsors: Create Sponsor, Assign, Modify Amount, Remove
        action_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        action_frame.pack(pady=12)

        def create_sponsor_flow():
            dialog = tk.Toplevel(self.root)
            dialog.title("Create Sponsor")
            dialog.geometry("520x420")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text="Create New Sponsor", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=10)

            tk.Label(dialog, text="Sponsor Name", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            name_entry = ModernEntry(dialog, width=50)
            name_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Contact Person", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            contact_entry = ModernEntry(dialog, width=50)
            contact_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Email", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            email_entry = ModernEntry(dialog, width=50)
            email_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Phone", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            phone_entry = ModernEntry(dialog, width=50)
            phone_entry.pack(padx=20, ipady=6)

            def submit_new():
                name = name_entry.get()
                contact = contact_entry.get()
                email = email_entry.get()
                phone = phone_entry.get()
                if not name:
                    messagebox.showerror("Error", "Sponsor name required")
                    return
                ok, result = db.create_new_sponsor(name, contact, email, phone)
                if ok:
                    messagebox.showinfo("Success", f"Sponsor created with ID {result}")
                    dialog.destroy()
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", result)

            HoverButton(dialog, text="Create Sponsor", command=submit_new).pack(pady=14)

        def assign_sponsor_flow():
            # Get organizer's events for combobox
            my_events = db.get_organizer_events(self.current_user)
            if not my_events:
                messagebox.showerror("Error", "You don't have any events. Create an event first.")
                return
            
            # Get all available sponsors
            all_sponsors = db.get_all_sponsors()
            if not all_sponsors:
                messagebox.showerror("Error", "No sponsors available. Create a sponsor first using the 'Create Sponsor' button.")
                return
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Assign Sponsor to Event")
            dialog.geometry("550x380")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text="Assign Sponsor", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=10)

            tk.Label(dialog, text="Select Event *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            tk.Label(dialog, text="💡 Choose from your events", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 8, "italic")).pack(anchor=tk.W, padx=20)
            
            event_options = [f"{e[0]} - {e[1]}" for e in my_events]
            event_var = tk.StringVar(value=event_options[0] if event_options else "")
            event_combo = ttk.Combobox(dialog, textvariable=event_var, values=event_options,
                                      state="readonly", width=47, font=("Segoe UI", 10))
            event_combo.pack(padx=20, pady=(0, 10))

            tk.Label(dialog, text="Select Sponsor *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            tk.Label(dialog, text="💡 Choose from available sponsors", 
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_DIM, 
                    font=("Segoe UI", 8, "italic")).pack(anchor=tk.W, padx=20)
            
            sponsor_options = [f"{s[0]} - {s[1]} ({s[2]})" for s in all_sponsors]
            sponsor_var = tk.StringVar(value=sponsor_options[0] if sponsor_options else "")
            sponsor_combo = ttk.Combobox(dialog, textvariable=sponsor_var, values=sponsor_options,
                                        state="readonly", width=47, font=("Segoe UI", 10))
            sponsor_combo.pack(padx=20, pady=(0, 10))

            tk.Label(dialog, text="Contribution Amount ($) *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            amount_entry = ModernEntry(dialog, width=30)
            amount_entry.pack(padx=20, ipady=6)

            def submit_assign():
                selected_event = event_var.get()
                selected_sponsor = sponsor_var.get()
                
                if not selected_event or not selected_sponsor:
                    messagebox.showerror("Error", "Please select both event and sponsor")
                    return
                    
                try:
                    event_id_val = int(selected_event.split(" - ")[0])
                    sponsor_id_val = int(selected_sponsor.split(" - ")[0])
                    amount_val = float(amount_entry.get().strip())
                except Exception:
                    messagebox.showerror("Error", "Invalid amount - ensure it's a valid number")
                    return
                
                if amount_val < 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                    
                ok, msg = db.assign_sponsor(self.current_user, event_id_val, sponsor_id_val, amount_val)
                if ok:
                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", msg)

            HoverButton(dialog, text="Assign Sponsor", command=submit_assign).pack(pady=12)

        def modify_sponsor_amount():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a sponsor mapping to modify")
                return
            vals = tree.item(selection[0])['values']
            event_id_val = vals[0]
            sponsor_id_val = vals[2]

            new_amount = simpledialog.askstring("Modify Amount", "Enter new amount:")
            if new_amount is None:
                return
            try:
                amt = float(new_amount)
            except Exception:
                messagebox.showerror("Error", "Invalid amount")
                return
            ok, msg = db.update_event_sponsor_amount(event_id_val, sponsor_id_val, self.current_user, amt)
            if ok:
                messagebox.showinfo("Success", msg)
                self.show_sponsors()
            else:
                messagebox.showerror("Error", msg)

        def remove_sponsor_mapping():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a sponsor mapping to remove")
                return
            vals = tree.item(selection[0])['values']
            event_id_val = vals[0]
            sponsor_id_val = vals[2]
            if messagebox.askyesno("Confirm", f"Remove sponsor ID {sponsor_id_val} from event {event_id_val}?"):
                ok, msg = db.delete_event_sponsor(event_id_val, sponsor_id_val, self.current_user)
                if ok:
                    messagebox.showinfo("Success", msg)
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", msg)

        tk.Label(self.main_content, text="💡 Tip: Double-click on an event to register",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_DIM,
                font=("Segoe UI", 9, "italic")).pack(pady=(0, 20))

    def register_for_event_inline(self, tree):
        selection = tree.selection()
        if not selection:
            return

        event_id = tree.item(selection[0])['values'][0]

        # Get tickets
        tickets = db.get_tickets_for_event(event_id)
        if not tickets:
            messagebox.showerror("Error", "No tickets available for this event")
            return

        # Show ticket selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Ticket")
        dialog.geometry("400x300")
        dialog.configure(bg=DarkTheme.BG_PRIMARY)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🎫 Select Ticket Type", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 16, "bold")).pack(pady=20)

        ticket_var = tk.StringVar()
        for ticket_type, price in tickets:
            rb = tk.Radiobutton(dialog, text=f"{ticket_type.upper()} - ${price}",
                               variable=ticket_var, value=ticket_type,
                               bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_PRIMARY,
                               selectcolor=DarkTheme.BG_TERTIARY,
                               font=("Segoe UI", 11),
                               activebackground=DarkTheme.BG_PRIMARY,
                               activeforeground=DarkTheme.ACCENT)
            rb.pack(pady=8)

        if tickets:
            ticket_var.set(tickets[0][0])

        def confirm():
            ticket_type = ticket_var.get()
            success, msg = db.register_for_event(self.current_user, event_id, ticket_type)
            if success:
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                self.show_browse_events()
            else:
                messagebox.showerror("Error", msg)

        HoverButton(dialog, text="Register Now", command=confirm).pack(pady=30)

    def show_my_registrations(self):
        self.set_active_menu(2)
        self.clear_content()

        header_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        header_frame.pack(fill=tk.X, padx=40, pady=(30, 20))

        tk.Label(header_frame, text="My Registrations", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(side=tk.LEFT)

        regs = db.get_user_registrations(self.current_user)

        if not regs:
            tk.Label(self.main_content, text="You haven't registered for any events yet",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("Reg ID", "Event", "Ticket", "Price", "Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        tree.heading("Reg ID", text="Reg ID")
        tree.column("Reg ID", width=100, anchor=tk.CENTER)
        tree.heading("Event", text="Event Name")
        tree.column("Event", width=400)
        tree.heading("Ticket", text="Ticket Type")
        tree.column("Ticket", width=150, anchor=tk.CENTER)
        tree.heading("Price", text="Price")
        tree.column("Price", width=120, anchor=tk.CENTER)
        tree.heading("Status", text="Status")
        tree.column("Status", width=150, anchor=tk.CENTER)

        for reg in regs:
            price = db.get_ticket_price(reg[3])
            tree.insert("", tk.END, values=(reg[0], reg[1], reg[2].upper(), f"${price}", reg[4].upper()))

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons for registrations
        action_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        action_frame.pack(pady=20)

        def modify_ticket():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a registration to modify")
                return
            
            vals = tree.item(selection[0])['values']
            reg_id = vals[0]
            event_name = vals[1]
            current_ticket = vals[2]
            status = vals[4].lower()
            
            if status != 'registered':
                messagebox.showerror("Error", "Can only modify registrations with 'registered' status")
                return
            
            # Get event_id from registration
            from func import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT event_id FROM Registrations WHERE registration_id=%s", (reg_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not result:
                messagebox.showerror("Error", "Event not found")
                return
            
            event_id = result[0]
            
            # Create dialog for ticket selection
            dialog = tk.Toplevel(self.root)
            dialog.title("Modify Ticket Type")
            dialog.geometry("500x350")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text=f"Change Ticket for {event_name}", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=15)
            
            tk.Label(dialog, text=f"Current Ticket: {current_ticket}", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 11)).pack(pady=5)
            
            tk.Label(dialog, text="Select New Ticket Type", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=30, pady=(15, 5))
            
            # Get ticket IDs
            from func import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT ticket_id, ticket_type, price FROM Tickets WHERE event_id=%s AND quantity_available>0", (event_id,))
            tickets_with_id = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if not tickets_with_id:
                messagebox.showerror("Error", "No available tickets for this event")
                dialog.destroy()
                return
            
            ticket_var = tk.StringVar()
            ticket_frame = tk.Frame(dialog, bg=DarkTheme.BG_PRIMARY)
            ticket_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
            
            for ticket_id, ticket_type, price in tickets_with_id:
                rb = tk.Radiobutton(ticket_frame, text=f"{ticket_type} - ${price}",
                                   variable=ticket_var, value=str(ticket_id),
                                   bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_PRIMARY,
                                   selectcolor=DarkTheme.BG_TERTIARY, font=("Segoe UI", 11),
                                   activebackground=DarkTheme.BG_PRIMARY,
                                   activeforeground=DarkTheme.ACCENT)
                rb.pack(anchor=tk.W, pady=8)
            
            if tickets_with_id:
                ticket_var.set(str(tickets_with_id[0][0]))
            
            def confirm_change():
                new_ticket_id = int(ticket_var.get())
                success, msg = db.update_registration_ticket(reg_id, self.current_user, new_ticket_id)
                if success:
                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                    self.show_my_registrations()
                else:
                    messagebox.showerror("Error", msg)
            
            HoverButton(dialog, text="✓ Update Ticket", command=confirm_change).pack(pady=20)

        def delete_registration():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a registration to delete")
                return
            
            vals = tree.item(selection[0])['values']
            reg_id = vals[0]
            event_name = vals[1]
            status = vals[4].lower()
            
            if status != 'registered':
                messagebox.showerror("Error", "Can only delete registrations with 'registered' status")
                return
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete registration for '{event_name}'?\n\nThis action cannot be undone."):
                success, msg = db.delete_registration(reg_id, self.current_user)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.show_my_registrations()
                else:
                    messagebox.showerror("Error", msg)

        HoverButton(action_frame, text="✏️ Modify Ticket Type", command=modify_ticket,
                   bg=DarkTheme.BG_TERTIARY, hover_bg=DarkTheme.BORDER).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="🗑️ Delete Registration", command=delete_registration,
                   bg=DarkTheme.DANGER, hover_bg="#c0392b").pack(side=tk.LEFT, padx=8)


    def show_payment_screen(self):
        self.set_active_menu(3)
        self.clear_content()

        tk.Label(self.main_content, text="Make Payment", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 10))

        regs = db.get_unpaid_registrations(self.current_user)

        if not regs:
            tk.Label(self.main_content, text="No unpaid registrations found. All payments are up to date! ✓",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        # Payment form in center
        form_container = tk.Frame(self.main_content, bg=DarkTheme.BG_CARD, bd=0)
        form_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=600)

        tk.Label(form_container, text="💳 Payment Details", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(pady=20)

        # Registration Selection
        tk.Label(form_container, text="Select Registration", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        reg_options = [f"RegID {r[0]} - {r[1]} ({r[2]}) - {r[4]}" for r in regs]
        reg_var = tk.StringVar(value=reg_options[0])

        reg_combo = ttk.Combobox(form_container, textvariable=reg_var, values=reg_options,
                                state="readonly", width=50, font=("Segoe UI", 10))
        reg_combo.pack(padx=40, pady=(0, 15))

        # Price Display
        tk.Label(form_container, text="Amount to Pay", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        price_label = tk.Label(form_container, text="$0.00", bg=DarkTheme.BG_CARD,
                              fg=DarkTheme.ACCENT, font=("Segoe UI", 24, "bold"))
        price_label.pack(padx=40, pady=(0, 15))

        # Payment Method
        tk.Label(form_container, text="Payment Method", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        payment_var = tk.StringVar(value="credit_card")
        payment_methods = [
            ("💳 Credit Card", "credit_card"),
            ("💳 Debit Card", "debit_card"),
            ("🅿️ PayPal", "paypal"),
            ("📱 UPI", "upi")
        ]

        method_frame = tk.Frame(form_container, bg=DarkTheme.BG_CARD)
        method_frame.pack(padx=40, pady=(0, 15))

        for text, value in payment_methods:
            rb = tk.Radiobutton(method_frame, text=text, variable=payment_var, value=value,
                               bg=DarkTheme.BG_CARD, fg=DarkTheme.TEXT_PRIMARY,
                               selectcolor=DarkTheme.BG_TERTIARY, font=("Segoe UI", 10),
                               activebackground=DarkTheme.BG_CARD,
                               activeforeground=DarkTheme.ACCENT)
            rb.pack(anchor=tk.W, pady=3)

        def update_price(*args):
            selected = reg_var.get()
            # Extract reg_id from the string (e.g., "RegID 123 - Event Name...")
            try:
                reg_id = int(selected.split()[1])
                # Find the corresponding ticket_id (index 3) from the regs list
                ticket_id = next(r[3] for r in regs if r[0] == reg_id)
                price = db.get_ticket_price(ticket_id)
                price_label.config(text=f"${price}")
            except (IndexError, ValueError, StopIteration):
                 price_label.config(text="$0.00")


        reg_combo.bind("<<ComboboxSelected>>", update_price)
        update_price()

        def process_payment():
            selected = reg_var.get()
            reg_id = int(selected.split()[1])
            amount_text = price_label.cget("text")
            if amount_text.strip() == "$0.00":
                messagebox.showerror("Error", "Please select a valid registration with a price.")
                return

            try:
                amount = float(amount_text.replace('$',''))
            except ValueError:
                messagebox.showerror("Error", "Invalid amount detected.")
                return

            method = payment_var.get()

            success, msg = db.make_payment(self.current_user, reg_id, amount, method)
            if success:
                # Update status to 'attended' after successful payment
                db.update_registration_status(reg_id, "attended")
                messagebox.showinfo("Success", msg)
                self.show_payment_screen()
            else:
                messagebox.showerror("Error", msg)

        # Payment Button - Ensure it's visible!
        HoverButton(form_container, text="💰 Process Payment", command=process_payment).pack(pady=15)

    def show_feedback_screen(self):
        self.set_active_menu(4)
        self.clear_content()

        tk.Label(self.main_content, text="Give Feedback", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 10))

        attended_events = db.get_attended_events(self.current_user)

        if not attended_events:
            tk.Label(self.main_content, text="You haven't attended any events yet",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        # Feedback form
        form_container = tk.Frame(self.main_content, bg=DarkTheme.BG_CARD, bd=0)
        form_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=700, height=550)

        tk.Label(form_container, text="⭐ Share Your Experience", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(pady=30)

        # Event Selection
        tk.Label(form_container, text="Select Event", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        event_options = [f"{e[0]} - {e[1]}" for e in attended_events]
        event_var = tk.StringVar(value=event_options[0])

        event_combo = ttk.Combobox(form_container, textvariable=event_var, values=event_options,
                                   state="readonly", width=60, font=("Segoe UI", 10))
        event_combo.pack(padx=40, pady=(0, 20))

        # Rating
        tk.Label(form_container, text="Rating (1-5 stars)", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        rating_frame = tk.Frame(form_container, bg=DarkTheme.BG_CARD)
        rating_frame.pack(padx=40, pady=(0, 20))

        rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            rb = tk.Radiobutton(rating_frame, text=f"{'⭐' * i}", variable=rating_var, value=i,
                               bg=DarkTheme.BG_CARD, fg=DarkTheme.TEXT_PRIMARY,
                               selectcolor=DarkTheme.BG_TERTIARY, font=("Segoe UI", 12),
                               activebackground=DarkTheme.BG_CARD,
                               activeforeground=DarkTheme.ACCENT)
            rb.pack(side=tk.LEFT, padx=10)

        # Comments
        tk.Label(form_container, text="Comments", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))

        comments_text = tk.Text(form_container, height=8, width=60, bg=DarkTheme.BG_TERTIARY,
                               fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 10),
                               relief=tk.FLAT, insertbackground=DarkTheme.TEXT_PRIMARY,
                               wrap=tk.WORD)
        comments_text.pack(padx=40, pady=(0, 20))

        # Load existing feedback if available
        def load_existing_feedback(*args):
            selected = event_var.get()
            event_id = int(selected.split(" - ")[0])
            existing = db.get_user_feedback(self.current_user, event_id)
            
            if existing:
                rating_var.set(existing[0])
                comments_text.delete("1.0", tk.END)
                comments_text.insert("1.0", existing[1])
                submit_btn.config(text="📝 Update Feedback")
                delete_btn.pack(side=tk.LEFT, padx=10)
            else:
                rating_var.set(5)
                comments_text.delete("1.0", tk.END)
                submit_btn.config(text="Submit Feedback")
                delete_btn.pack_forget()
        
        event_combo.bind("<<ComboboxSelected>>", load_existing_feedback)

        def submit_feedback():
            selected = event_var.get()
            event_id = int(selected.split(" - ")[0])
            rating = rating_var.get()
            comments = comments_text.get("1.0", tk.END).strip()

            if not comments:
                messagebox.showerror("Error", "Please enter your comments")
                return

            # Check if updating or creating new
            existing = db.get_user_feedback(self.current_user, event_id)
            
            if existing:
                success, msg = db.update_feedback(self.current_user, event_id, rating, comments)
            else:
                success, msg = db.give_feedback(self.current_user, event_id, rating, comments)
            
            if success:
                messagebox.showinfo("Success", msg)
                self.show_feedback_screen()
            else:
                messagebox.showerror("Error", msg)

        def delete_feedback():
            selected = event_var.get()
            event_id = int(selected.split(" - ")[0])
            event_name = selected.split(" - ")[1]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete your feedback for '{event_name}'?"):
                success, msg = db.delete_feedback(self.current_user, event_id)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.show_feedback_screen()
                else:
                    messagebox.showerror("Error", msg)

        button_frame = tk.Frame(form_container, bg=DarkTheme.BG_CARD)
        button_frame.pack(pady=10)

        submit_btn = HoverButton(button_frame, text="Submit Feedback", command=submit_feedback)
        submit_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = HoverButton(button_frame, text="🗑️ Delete Feedback", command=delete_feedback,
                                 bg=DarkTheme.DANGER, hover_bg="#c0392b")
        # delete_btn will be packed conditionally by load_existing_feedback
        
        # Load feedback for first event
        load_existing_feedback()

    # ==================== ORGANIZER SCREENS ====================
    def show_organizer_dashboard(self):
        self.set_active_menu(0)
        self.clear_content()

        tk.Label(self.main_content, text="Organizer Dashboard", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 10))

        tk.Label(self.main_content, text="Manage your events and track performance.",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 11)).pack(anchor=tk.W, padx=40, pady=(0, 30))

        # Stats Cards
        cards_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        cards_frame.pack(fill=tk.X, padx=40, pady=20)

        events = db.get_organizer_events(self.current_user)
        analytics = db.get_organizer_analytics(self.current_user)

        total_revenue = sum(a['total_revenue'] for a in analytics) if analytics else 0
        avg_rating = sum(a['avg_rating'] for a in analytics) / len(analytics) if analytics else 0

        stats = [
            ("🎪", "Total Events", len(events) if events else 0, DarkTheme.ACCENT),
            ("💰", "Total Revenue", f"${total_revenue:.2f}", DarkTheme.SUCCESS),
            ("⭐", "Avg Rating", f"{avg_rating:.1f}/5.0", DarkTheme.WARNING),
        ]

        for icon, label, value, color in stats:
            card = tk.Frame(cards_frame, bg=DarkTheme.BG_CARD, bd=0, relief=tk.FLAT)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

            tk.Label(card, text=icon, bg=DarkTheme.BG_CARD, font=("Segoe UI", 36)).pack(pady=(25, 10))
            tk.Label(card, text=str(value), bg=DarkTheme.BG_CARD, fg=color,
                    font=("Segoe UI", 28, "bold")).pack()
            tk.Label(card, text=label, bg=DarkTheme.BG_CARD, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 10)).pack(pady=(5, 25))

    def show_my_events(self):
        self.set_active_menu(1)
        self.clear_content()

        header_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        header_frame.pack(fill=tk.X, padx=40, pady=(30, 20))

        tk.Label(header_frame, text="My Events", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(side=tk.LEFT)

        HoverButton(header_frame, text="➕ Create New Event",
                   command=self.create_event_flow).pack(side=tk.RIGHT)

        events = db.get_organizer_events(self.current_user)

        if not events:
            tk.Label(self.main_content, text="You haven't created any events yet",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("ID", "Name", "Date", "Description", "Location")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        tree.heading("ID", text="ID")
        tree.column("ID", width=70, anchor=tk.CENTER)
        tree.heading("Name", text="Event Name")
        tree.column("Name", width=250)
        tree.heading("Date", text="Date")
        tree.column("Date", width=150, anchor=tk.CENTER)
        tree.heading("Description", text="Description")
        tree.column("Description", width=400)
        tree.heading("Location", text="Loc ID")
        tree.column("Location", width=80, anchor=tk.CENTER)

        for row in events:
            tree.insert("", tk.END, values=row)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons
        action_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        action_frame.pack(pady=20)

        def modify_event():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select an event to modify")
                return
            event_id = tree.item(selection[0])['values'][0]
            self.modify_event_flow(event_id)

        def delete_event():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select an event to delete")
                return
            event_id = tree.item(selection[0])['values'][0]

            if not db.check_event_ownership(event_id, self.current_user):
                messagebox.showerror("Permission Denied", "You can only delete events you organize.")
                return

            if messagebox.askyesno("Confirm Delete",
                                  f"Delete Event ID {event_id} and ALL related data?"):
                success, msg = db.delete_event_cascading(event_id)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.show_my_events()
                else:
                    messagebox.showerror("Error", msg)

        HoverButton(action_frame, text="✏️ Modify", command=modify_event,
                   bg=DarkTheme.BG_TERTIARY, hover_bg=DarkTheme.BORDER).pack(side=tk.LEFT, padx=10)
        HoverButton(action_frame, text="🗑️ Delete", command=delete_event,
                   bg=DarkTheme.DANGER, hover_bg="#c0392b").pack(side=tk.LEFT, padx=10)

    def create_event_flow(self):
        # Simple dialog for event creation
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Event")
        dialog.geometry("500x600")
        dialog.configure(bg=DarkTheme.BG_PRIMARY)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🎪 Create New Event", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(pady=20)

        # Form fields
        fields = [
            ("Event Name:", "name"),
            ("Description:", "desc"),
            ("Date (YYYY-MM-DD):", "date"),
            ("Location Name:", "location")
        ]

        entries = {}
        for label, key in fields:
            tk.Label(dialog, text=label, bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))
            entry = ModernEntry(dialog, width=50)
            entry.pack(padx=40, pady=(0, 10), ipady=8)
            entries[key] = entry

        def submit():
            name = entries['name'].get()
            desc = entries['desc'].get()
            date = entries['date'].get()
            location = entries['location'].get()

            if not all([name, desc, date, location]):
                messagebox.showerror("Error", "Please fill all fields")
                return

            loc_id = db.get_location_id(location)
            success, msg, event_id = db.create_event(self.current_user, name, desc, date, loc_id)

            if success:
                messagebox.showinfo("Success", f"Event created! Now add tickets.")
                dialog.destroy()
                self.add_tickets_flow(event_id)
            else:
                messagebox.showerror("Error", msg)

        HoverButton(dialog, text="Create Event", command=submit).pack(pady=30)

    def add_tickets_flow(self, event_id):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Tickets")
        dialog.geometry("450x400")
        dialog.configure(bg=DarkTheme.BG_PRIMARY)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="🎫 Add Ticket Types", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(pady=20)

        tk.Label(dialog, text=f"Event ID: {event_id}", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack()

        ticket_added = [False]

        def add_ticket():
            ticket_type = type_var.get()
            try:
                price = float(price_entry.get())
                quantity = int(qty_entry.get())
            except:
                messagebox.showerror("Error", "Invalid price or quantity")
                return

            if ticket_type.lower() not in VALID_TICKET_TYPES:
                messagebox.showerror("Error", f"Invalid ticket type. Choose from: {', '.join(VALID_TICKET_TYPES)}")
                return

            ok, msg = db.add_ticket_type(event_id, ticket_type.lower(), price, quantity)
            if ok:
                messagebox.showinfo("Success", msg)
                ticket_added[0] = True
                price_entry.delete(0, tk.END)
                qty_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", msg)

        def finish():
            if not ticket_added[0]:
                messagebox.showerror("Error", "Add at least 1 ticket type")
                return
            dialog.destroy()
            self.show_my_events()

        form_frame = tk.Frame(dialog, bg=DarkTheme.BG_CARD)
        form_frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Ticket Type", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(pady=(15, 5))

        type_var = tk.StringVar(value="regular")
        ttk.Combobox(form_frame, textvariable=type_var, values=VALID_TICKET_TYPES,
                    state="readonly", width=25).pack(pady=(0, 15))

        tk.Label(form_frame, text="Price ($)", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(pady=(5, 5))
        price_entry = ModernEntry(form_frame, width=25)
        price_entry.pack(pady=(0, 15), ipady=5)

        tk.Label(form_frame, text="Quantity", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(pady=(5, 5))
        qty_entry = ModernEntry(form_frame, width=25)
        qty_entry.pack(pady=(0, 20), ipady=5)

        HoverButton(form_frame, text="➕ Add Ticket", command=add_ticket).pack(pady=5)
        HoverButton(dialog, text="✅ Finish", command=finish,
                   bg=DarkTheme.SUCCESS, hover_bg="#0d9668").pack(pady=20)

    def modify_event_flow(self, event_id):
        if not db.check_event_ownership(event_id, self.current_user):
            messagebox.showerror("Permission Denied", "You can only modify your own events")
            return

        current = db.get_event_details(event_id)
        if not current:
            messagebox.showerror("Error", "Event not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Modify Event")
        dialog.geometry("500x500")
        dialog.configure(bg=DarkTheme.BG_PRIMARY)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="✏️ Modify Event", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 18, "bold")).pack(pady=20)

        fields = [
            ("Event Name:", "event_name", current['event_name']),
            ("Description:", "description", current['description']),
            ("Date (YYYY-MM-DD):", "event_date", current['event_date'])
        ]

        entries = {}
        for label, key, default in fields:
            tk.Label(dialog, text=label, bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=40, pady=(10, 5))
            entry = ModernEntry(dialog, width=50)
            entry.insert(0, str(default))
            entry.pack(padx=40, pady=(0, 10), ipady=8)
            entries[key] = entry

        def submit():
            name = entries['event_name'].get()
            desc = entries['description'].get()
            date = entries['event_date'].get()

            success, msg = db.update_event(event_id, name, desc, date)
            if success:
                messagebox.showinfo("Success", msg)
                dialog.destroy()
                self.show_my_events()
            else:
                messagebox.showerror("Error", msg)

        HoverButton(dialog, text="Update Event", command=submit).pack(pady=30)

    def show_schedules(self):
        self.set_active_menu(2)
        self.clear_content()

        tk.Label(self.main_content, text="Event Schedules", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 20))

        tk.Label(self.main_content, text="💡 Select an event to view and manage its schedules",
                bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                font=("Segoe UI", 11)).pack(anchor=tk.W, padx=40, pady=(0, 20))

        # Get organizer's events for combobox
        my_events = db.get_organizer_events(self.current_user)
        
        if not my_events:
            tk.Label(self.main_content, text="You don't have any events yet. Create an event first.",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        # Input form
        input_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_CARD)
        input_frame.pack(padx=40, pady=20, fill=tk.X)

        tk.Label(input_frame, text="Select Event:", bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=20, pady=15)

        event_options = [f"{e[0]} - {e[1]}" for e in my_events]
        event_var = tk.StringVar(value=event_options[0] if event_options else "")
        event_combo = ttk.Combobox(input_frame, textvariable=event_var, values=event_options,
                                   state="readonly", width=50, font=("Segoe UI", 10))
        event_combo.pack(side=tk.LEFT, padx=10, ipady=5)

        def load_schedules():
            selected = event_var.get()
            if not selected:
                messagebox.showerror("Error", "Please select an event")
                return
            
            try:
                event_id = int(selected.split(" - ")[0])
            except:
                messagebox.showerror("Error", "Invalid Event selection")
                return

            schedules = db.get_event_schedules(event_id, self.current_user)
            self.display_schedules(event_id, schedules)

        HoverButton(input_frame, text="Load Schedules", command=load_schedules).pack(side=tk.LEFT, padx=10)

    def display_schedules(self, event_id, schedules):
        # Clear previous results
        for widget in self.main_content.winfo_children()[3:]:
            widget.destroy()

        # Show table only if schedules exist
        if schedules:
            table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

            columns = ("ID", "Start", "End", "Activity", "Description")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

            tree.heading("ID", text="Sch ID")
            tree.column("ID", width=80, anchor=tk.CENTER)
            tree.heading("Start", text="Start Time")
            tree.column("Start", width=180)
            tree.heading("End", text="End Time")
            tree.column("End", width=180)
            tree.heading("Activity", text="Activity")
            tree.column("Activity", width=200)
            tree.heading("Description", text="Description")
            tree.column("Description", width=400)

            for row in schedules:
                tree.insert("", tk.END, values=(
                    row['schedule_id'], row['start_time'], row['end_time'],
                    row['activity_name'], row['description']
                ))

            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(self.main_content, text="No schedules found for this event - Create one below!",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=30)

        # Action buttons for schedules: Create, Modify, Delete
        action_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        action_frame.pack(pady=20)

        def create_schedule():
            dialog = tk.Toplevel(self.root)
            dialog.title("Create Schedule Entry")
            dialog.geometry("550x450")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text=f"Add Schedule for Event ID {event_id}", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=15)

            tk.Label(dialog, text="Start Time (YYYY-MM-DD HH:MM:SS)", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            
            help_label = tk.Label(dialog, text="💡 Example: 2025-12-25 14:30:00", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 8, "italic"))
            help_label.pack(anchor=tk.W, padx=20, pady=(0, 5))
            
            start_entry = ModernEntry(dialog, width=40)
            start_entry.pack(padx=20, ipady=8)

            tk.Label(dialog, text="Activity Name", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            activity_entry = ModernEntry(dialog, width=40)
            activity_entry.pack(padx=20, ipady=8)

            tk.Label(dialog, text="Description (Optional)", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            desc_entry = ModernEntry(dialog, width=40)
            desc_entry.pack(padx=20, ipady=8)

            def validate_datetime(dt_string):
                import re
                from datetime import datetime
                pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
                if not re.match(pattern, dt_string):
                    return False, "Format must be YYYY-MM-DD HH:MM:SS"
                try:
                    datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
                    return True, ""
                except:
                    return False, "Invalid date/time values"

            def submit():
                start_time = start_entry.get().strip()
                activity = activity_entry.get().strip()
                desc = desc_entry.get().strip()
                
                if not start_time or not activity:
                    messagebox.showerror("Error", "Start time and activity name are required")
                    return
                
                # Validate datetime format
                valid, error_msg = validate_datetime(start_time)
                if not valid:
                    messagebox.showerror("Invalid Format", error_msg)
                    return
                
                ok, msg = db.manage_schedule(event_id, start_time, activity, desc)
                if ok:
                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                    schedules_new = db.get_event_schedules(event_id, self.current_user)
                    self.display_schedules(event_id, schedules_new)
                else:
                    messagebox.showerror("Error", msg)

            HoverButton(dialog, text="➕ Add Schedule", command=submit).pack(pady=20)

        def modify_schedule():
            if not schedules:
                messagebox.showinfo("Info", "No schedules available to modify. Create one first!")
                return
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a schedule to modify")
                return
            vals = tree.item(selection[0])['values']
            schedule_id, start_time, end_time, activity_name, description = vals

            dialog = tk.Toplevel(self.root)
            dialog.title("Modify Schedule")
            dialog.geometry("550x450")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text=f"Modify Schedule ID {schedule_id}", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=15)

            tk.Label(dialog, text="Start Time (YYYY-MM-DD HH:MM:SS)", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            
            help_label = tk.Label(dialog, text="💡 Example: 2025-12-25 14:30:00", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 8, "italic"))
            help_label.pack(anchor=tk.W, padx=20, pady=(0, 5))
            
            start_entry = ModernEntry(dialog, width=40)
            start_entry.insert(0, str(start_time))
            start_entry.pack(padx=20, ipady=8)

            tk.Label(dialog, text="Activity Name", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            activity_entry = ModernEntry(dialog, width=40)
            activity_entry.insert(0, str(activity_name))
            activity_entry.pack(padx=20, ipady=8)

            tk.Label(dialog, text="Description (Optional)", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(anchor=tk.W, padx=20, pady=(10, 5))
            desc_entry = ModernEntry(dialog, width=40)
            desc_entry.insert(0, str(description))
            desc_entry.pack(padx=20, ipady=8)

            def validate_datetime(dt_string):
                import re
                from datetime import datetime
                pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
                if not re.match(pattern, dt_string):
                    return False, "Format must be YYYY-MM-DD HH:MM:SS"
                try:
                    datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S')
                    return True, ""
                except:
                    return False, "Invalid date/time values"

            def submit_mod():
                new_start = start_entry.get().strip()
                new_activity = activity_entry.get().strip()
                new_desc = desc_entry.get().strip()
                
                if not new_start or not new_activity:
                    messagebox.showerror("Error", "Start time and activity name are required")
                    return
                
                # Validate datetime format
                valid, error_msg = validate_datetime(new_start)
                if not valid:
                    messagebox.showerror("Invalid Format", error_msg)
                    return
                
                ok, msg = db.update_schedule(schedule_id, new_start, new_activity, new_desc)
                if ok:
                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                    schedules_new = db.get_event_schedules(event_id, self.current_user)
                    self.display_schedules(event_id, schedules_new)
                else:
                    messagebox.showerror("Error", msg)

            HoverButton(dialog, text="Update Schedule", command=submit_mod).pack(pady=20)

        def delete_schedule_action():
            if not schedules:
                messagebox.showinfo("Info", "No schedules available to delete. Create one first!")
                return
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a schedule to delete")
                return
            schedule_id = tree.item(selection[0])['values'][0]
            if messagebox.askyesno("Confirm", f"Delete schedule ID {schedule_id}?"):
                ok, msg = db.delete_schedule(schedule_id)
                if ok:
                    messagebox.showinfo("Success", msg)
                    schedules_new = db.get_event_schedules(event_id, self.current_user)
                    self.display_schedules(event_id, schedules_new)
                else:
                    messagebox.showerror("Error", msg)

        HoverButton(action_frame, text="➕ Create Schedule", command=create_schedule).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="✏️ Modify Schedule", command=modify_schedule,
                   bg=DarkTheme.BG_TERTIARY, hover_bg=DarkTheme.BORDER).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="🗑️ Delete Schedule", command=delete_schedule_action,
                   bg=DarkTheme.DANGER, hover_bg="#c0392b").pack(side=tk.LEFT, padx=8)

    def show_sponsors(self):
        self.set_active_menu(3)
        self.clear_content()

        header_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        header_frame.pack(fill=tk.X, padx=40, pady=(30, 20))

        tk.Label(header_frame, text="Event Sponsors", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(side=tk.LEFT)

        sponsors = db.view_organizer_sponsors(self.current_user)

        # Create table frame and tree
        table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

        if not sponsors:
            tk.Label(table_frame, text="No sponsors assigned yet. Create a sponsor or assign one to your events.",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            tree = None
        else:
            columns = ("E.ID", "Event", "S.ID", "Sponsor", "Contact", "Email", "Phone", "Amount")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

            widths = [70, 200, 70, 150, 140, 180, 110, 120]
            for i, col in enumerate(columns):
                tree.heading(col, text=col)
                tree.column(col, width=widths[i], anchor=tk.E if col == "Amount" else tk.W)

            for row in sponsors:
                tree.insert("", tk.END, values=row)

            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons for sponsors - ALWAYS SHOW
        action_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        action_frame.pack(pady=12)

        def create_sponsor_flow():
            dialog = tk.Toplevel(self.root)
            dialog.title("Create Sponsor")
            dialog.geometry("520x420")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text="Create New Sponsor", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=10)

            tk.Label(dialog, text="Sponsor Name *", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            name_entry = ModernEntry(dialog, width=50)
            name_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Contact Person", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            contact_entry = ModernEntry(dialog, width=50)
            contact_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Email", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            email_entry = ModernEntry(dialog, width=50)
            email_entry.pack(padx=20, ipady=6)

            tk.Label(dialog, text="Phone", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(8, 0))
            phone_entry = ModernEntry(dialog, width=50)
            phone_entry.pack(padx=20, ipady=6)

            def submit_new():
                name = name_entry.get().strip()
                contact = contact_entry.get().strip()
                email = email_entry.get().strip()
                phone = phone_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Sponsor name is required")
                    return
                ok, result = db.create_new_sponsor(name, contact, email, phone)
                if ok:
                    messagebox.showinfo("Success", f"Sponsor created with ID {result}")
                    dialog.destroy()
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", result)

            HoverButton(dialog, text="Create Sponsor", command=submit_new).pack(pady=14)

        def assign_sponsor_flow():
            # Get organizer's events for combobox
            my_events = db.get_organizer_events(self.current_user)
            if not my_events:
                messagebox.showerror("Error", "You don't have any events. Create an event first.")
                return
            
            # Get all available sponsors
            all_sponsors = db.get_all_sponsors()
            if not all_sponsors:
                messagebox.showerror("Error", "No sponsors available. Create a sponsor first using the 'Create Sponsor' button.")
                return
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Assign Sponsor to Event")
            dialog.geometry("550x380")
            dialog.configure(bg=DarkTheme.BG_PRIMARY)
            dialog.transient(self.root)
            dialog.grab_set()

            tk.Label(dialog, text="Assign Sponsor", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 14, "bold")).pack(pady=10)

            tk.Label(dialog, text="Select Event *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            tk.Label(dialog, text="💡 Choose from your events", bg=DarkTheme.BG_PRIMARY,
                    fg=DarkTheme.TEXT_DIM, font=("Segoe UI", 8, "italic")).pack(anchor=tk.W, padx=20)
            
            event_options = [f"{e[0]} - {e[1]}" for e in my_events]
            event_var = tk.StringVar(value=event_options[0] if event_options else "")
            event_combo = ttk.Combobox(dialog, textvariable=event_var, values=event_options,
                                      state="readonly", width=47, font=("Segoe UI", 10))
            event_combo.pack(padx=20, pady=(0, 10))

            tk.Label(dialog, text="Select Sponsor *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            tk.Label(dialog, text="💡 Choose from available sponsors", 
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_DIM, 
                    font=("Segoe UI", 8, "italic")).pack(anchor=tk.W, padx=20)
            
            sponsor_options = [f"{s[0]} - {s[1]} ({s[2]})" for s in all_sponsors]
            sponsor_var = tk.StringVar(value=sponsor_options[0] if sponsor_options else "")
            sponsor_combo = ttk.Combobox(dialog, textvariable=sponsor_var, values=sponsor_options,
                                        state="readonly", width=47, font=("Segoe UI", 10))
            sponsor_combo.pack(padx=20, pady=(0, 10))

            tk.Label(dialog, text="Contribution Amount ($) *", bg=DarkTheme.BG_PRIMARY, 
                    fg=DarkTheme.TEXT_SECONDARY).pack(anchor=tk.W, padx=20, pady=(10, 5))
            amount_entry = ModernEntry(dialog, width=30)
            amount_entry.pack(padx=20, ipady=6)

            def submit_assign():
                selected_event = event_var.get()
                selected_sponsor = sponsor_var.get()
                
                if not selected_event or not selected_sponsor:
                    messagebox.showerror("Error", "Please select both event and sponsor")
                    return
                    
                try:
                    event_id_val = int(selected_event.split(" - ")[0])
                    sponsor_id_val = int(selected_sponsor.split(" - ")[0])
                    amount_val = float(amount_entry.get().strip())
                except Exception:
                    messagebox.showerror("Error", "Invalid amount - ensure it's a valid number")
                    return
                
                if amount_val < 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                    
                ok, msg = db.assign_sponsor(self.current_user, event_id_val, sponsor_id_val, amount_val)
                if ok:
                    messagebox.showinfo("Success", msg)
                    dialog.destroy()
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", msg)

            HoverButton(dialog, text="Assign Sponsor", command=submit_assign).pack(pady=12)

        def modify_sponsor_amount():
            if tree is None:
                messagebox.showerror("Error", "No sponsor mappings to modify")
                return
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a sponsor mapping to modify")
                return
            vals = tree.item(selection[0])['values']
            event_id_val = vals[0]
            sponsor_id_val = vals[2]
            current_amount = vals[7]

            new_amount = simpledialog.askstring("Modify Amount", 
                                               f"Current amount: ${current_amount}\nEnter new amount:")
            if new_amount is None:
                return
            try:
                amt = float(new_amount.strip())
                if amt < 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
            except Exception:
                messagebox.showerror("Error", "Invalid amount - must be a number")
                return
            ok, msg = db.update_event_sponsor_amount(event_id_val, sponsor_id_val, self.current_user, amt)
            if ok:
                messagebox.showinfo("Success", msg)
                self.show_sponsors()
            else:
                messagebox.showerror("Error", msg)

        def remove_sponsor_mapping():
            if tree is None:
                messagebox.showerror("Error", "No sponsor mappings to remove")
                return
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a sponsor mapping to remove")
                return
            vals = tree.item(selection[0])['values']
            event_id_val = vals[0]
            event_name = vals[1]
            sponsor_id_val = vals[2]
            sponsor_name = vals[3]
            
            if messagebox.askyesno("Confirm", 
                                  f"Remove sponsor '{sponsor_name}' (ID {sponsor_id_val})\nfrom event '{event_name}' (ID {event_id_val})?"):
                ok, msg = db.delete_event_sponsor(event_id_val, sponsor_id_val, self.current_user)
                if ok:
                    messagebox.showinfo("Success", msg)
                    self.show_sponsors()
                else:
                    messagebox.showerror("Error", msg)

        HoverButton(action_frame, text="➕ Create Sponsor", command=create_sponsor_flow).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="🔗 Assign Sponsor", command=assign_sponsor_flow,
                   bg=DarkTheme.BG_TERTIARY, hover_bg=DarkTheme.BORDER).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="✏️ Modify Amount", command=modify_sponsor_amount,
                   bg=DarkTheme.BG_TERTIARY, hover_bg=DarkTheme.BORDER).pack(side=tk.LEFT, padx=8)
        HoverButton(action_frame, text="🗑️ Remove Sponsor", command=remove_sponsor_mapping,
                   bg=DarkTheme.DANGER, hover_bg="#c0392b").pack(side=tk.LEFT, padx=8)

    def show_organizer_feedback(self):
        self.set_active_menu(4)
        self.clear_content()

        tk.Label(self.main_content, text="Event Feedback", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 20))

        feedback = db.view_feedback(None, self.current_user)

        if not feedback:
            tk.Label(self.main_content, text="No feedback received yet",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.TEXT_SECONDARY,
                    font=("Segoe UI", 12)).pack(pady=50)
            return

        table_frame = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("U.ID", "User", "E.ID", "Event", "Rating", "Comments", "Date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        widths = [70, 150, 70, 200, 80, 400, 120]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i], anchor=tk.CENTER if col in ["U.ID", "E.ID", "Rating"] else tk.W)

        for row in feedback:
            tree.insert("", tk.END, values=row)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_analytics(self):
        self.set_active_menu(5)
        self.clear_content()

        tk.Label(self.main_content, text="Analytics & Reports", bg=DarkTheme.BG_PRIMARY,
                fg=DarkTheme.TEXT_PRIMARY, font=("Segoe UI", 24, "bold")).pack(anchor=tk.W, padx=40, pady=(30, 20))

        # Revenue & Rating Analytics
        analytics = db.get_organizer_analytics(self.current_user)

        if analytics:
            tk.Label(self.main_content, text="📊 Financial & Rating Summary",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.ACCENT,
                    font=("Segoe UI", 16, "bold")).pack(anchor=tk.W, padx=40, pady=(20, 10))

            table_frame1 = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
            table_frame1.pack(fill=tk.X, padx=40, pady=(0, 30))

            columns1 = ("ID", "Event Name", "Avg Rating", "Total Revenue")
            tree1 = ttk.Treeview(table_frame1, columns=columns1, show="headings", height=8)

            tree1.heading("ID", text="E.ID")
            tree1.column("ID", width=80, anchor=tk.CENTER)
            tree1.heading("Event Name", text="Event Name")
            tree1.column("Event Name", width=500)
            tree1.heading("Avg Rating", text="Avg Rating")
            tree1.column("Avg Rating", width=150, anchor=tk.CENTER)
            tree1.heading("Total Revenue", text="Total Revenue")
            tree1.column("Total Revenue", width=180, anchor=tk.E)

            for row in analytics:
                tree1.insert("", tk.END, values=(
                    row['event_id'], row['event_name'],
                    f"{row['avg_rating']:.2f} ⭐", f"${row['total_revenue']:.2f}"
                ))

            scrollbar1 = ttk.Scrollbar(table_frame1, orient=tk.VERTICAL, command=tree1.yview)
            tree1.configure(yscrollcommand=scrollbar1.set)

            tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        # Events without sponsors
        no_sponsors = db.get_events_with_no_sponsors(self.current_user)

        if no_sponsors:
            tk.Label(self.main_content, text="⚠️ Events Without Sponsors",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.WARNING,
                    font=("Segoe UI", 16, "bold")).pack(anchor=tk.W, padx=40, pady=(20, 10))

            table_frame2 = tk.Frame(self.main_content, bg=DarkTheme.BG_PRIMARY)
            table_frame2.pack(fill=tk.X, padx=40, pady=(0, 30))

            columns2 = ("ID", "Event Name", "Date")
            tree2 = ttk.Treeview(table_frame2, columns=columns2, show="headings", height=6)

            tree2.heading("ID", text="Event ID")
            tree2.column("ID", width=100, anchor=tk.CENTER)
            tree2.heading("Event Name", text="Event Name")
            tree2.column("Event Name", width=600)
            tree2.heading("Date", text="Date")
            tree2.column("Date", width=200, anchor=tk.CENTER)

            for row in no_sponsors:
                tree2.insert("", tk.END, values=row)

            scrollbar2 = ttk.Scrollbar(table_frame2, orient=tk.VERTICAL, command=tree2.yview)
            tree2.configure(yscrollcommand=scrollbar2.set)

            tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(self.main_content, text="✅ All events have sponsors!",
                    bg=DarkTheme.BG_PRIMARY, fg=DarkTheme.SUCCESS,
                    font=("Segoe UI", 14)).pack(pady=30)

# ==================== MAIN ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagementApp(root)
    root.mainloop()
