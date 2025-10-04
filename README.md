This project, **CompanyOS**, is a responsive Company Management System built as a single-page application (SPA) using **HTML, CSS, and JavaScript**, featuring a dark-themed, modern design and an advanced admin panel for user and company management.

Here is the `README.md` for the provided `index.html` file.

```markdown
# CompanyOS - The Ultimate Company Management System

**CompanyOS** is a modern, responsive single-page application (SPA) designed for efficient company management. It features a sleek, dark-themed user interface, an engaging landing page with dynamic effects, a smooth, interactive authentication modal, and a comprehensive, role-based admin panel.

## Features

### 💻 Frontend & Design
* **Modern, Dark Theme:** A visually appealing interface using a dark color palette (`--bg-dark: #25252b`) with a vibrant primary accent color (`--primary-color: #e46033`).
* **Fully Responsive:** Optimized layout for all screen sizes, from mobile devices to desktop computers.
* **Smooth Animations:** Utilizes **Animate On Scroll (AOS)** for engaging content transitions and custom CSS animations for navigation and UI elements.
* **Dynamic Background:** Features a subtle, floating particle effect on the home section for a futuristic look.
* **Custom Modals:** Unique, curved-shape animated modals for the Login/Register flow.

---

### 🚀 Landing Page Highlights
* **Home Section:** Eye-catching hero section with a transparent, gradient-filled title ("Welcome to CompanyOS").
* **About Section:** Grid-based layout showcasing key features with hover effects:
    * **Easy Onboarding**
    * **Team Management**
    * **Role-Based Access** (Admin, Manager, Employee)
    * **Manager Hierarchy**
    * **Multi-Currency** (USD, EUR, GBP, INR, JPY, AUD, CAD)
    * **Real-Time Dashboard**
* **Contact Form:** Simple form with floating labels and a modern dark aesthetic.

---

### 🔒 Authentication & Management (Simulated with JS)
The application includes front-end logic (JavaScript functions like `handleLogin`, `handleRegister`, `loadUsersData`) to simulate interaction with a backend API (e.g., `/api/login/`, `/api/register/`, `/api/users/`).

* **Login / Register Modal:** A dynamic, two-sided modal that transitions between sign-in and sign-up forms.
* **User Roles:** Implements Admin, Manager, and Employee roles for access control.
* **Initial Setup:** Registration simulates the creation of the first company and an Admin user.

---

### 📊 Admin Panel (for Admin Role)
A dedicated, fully-featured management interface accessible upon successful login as an 'admin'.

* **Dashboard:** Displays key metrics like **Total Employees**, **Total Managers**, and **Total Users**.
* **Employee Management:**
    * View, Add, Edit, and Delete employee records.
    * Assign a **Manager** to an employee using a dropdown.
* **Manager Management:**
    * View managers and their respective **Team Size** (simulated).
    * View, Add, Edit, and Delete manager records.
* **Company Settings:** Allows the admin to update the **Company Name**, **Currency**, **Address**, and **Phone**.
* **Responsive Sidebar:** A collapsible sidebar for navigation that adapts for mobile viewing with a toggle button.

## 🛠️ Technologies Used

* **HTML5**
* **CSS3** (Custom Styles & Variables)
* **JavaScript** (ES6+)
* **AOS Library:** (Animate On Scroll) for scroll animations.

## 📝 Setup and Usage

This project is a client-side SPA and can be run directly in any web browser.

1.  **Clone the repository or save the `index.html` file.**
2.  **Open `index.html`** in your web browser.

**Note:** Since this is a front-end only implementation, the `handleLogin`, `handleRegister`, and admin panel functions currently simulate API calls and manage application state within the browser's memory (`appState` object). A real-world application would require a backend (like Django, Node.js, or similar) to persist data and handle authentication securely.
```
