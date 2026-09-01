# HeartWise ❤️

### Personalized Heart-Healthy Food Recommendation and Meal Planning System

**HeartWise** is a web-based health and nutrition application designed to help users make better food choices through personalized food recommendations, nutritional information, daily meal plans, and healthy recipes.

The system allows users to create an account, manage their profile, explore heart-friendly foods, search and filter food items, view detailed nutritional information, receive personalized recommendations, and access meal plans and recipes.

---

## 📌 Project Description

Choosing healthy food can be difficult when nutritional information and suitable meal options are spread across different sources.

HeartWise provides a centralized platform that combines:

* 👤 User registration and login
* 📝 User profile management
* 🥗 Healthy food exploration
* 🔎 Food search and category filtering
* 📊 Nutritional information
* ❤️ Personalized food recommendations
* 🍽️ Daily meal planning
* 📖 Recipe details
* 📱 Responsive web design

The goal of the project is to make healthy food discovery and meal planning simple, organized, and personalized.

---

## ✨ Features

### 🔐 User Authentication

* User registration
* User login
* Login error handling
* Session-based user access
* Logout functionality

### 👤 User Profile

Users can create and update their profile information.

Profile information is used to provide more relevant food recommendations.

### 🏠 Dashboard

The personalized dashboard provides an overview of the user's HeartWise experience, including:

* Profile status
* Recommended foods
* Food categories
* Nutritional information
* Meal plan information
* HeartWise journey information

### 🥗 HeartWise Foods

Users can browse available food items through a clean card-based interface.

Each food card can display:

* Food name
* Food category
* Dietary tag
* Nutritional information
* HeartWise recommendation
* Food details

### 🔎 Search and Filtering

Users can:

* Search for food items
* Filter foods by category
* Clear search and filter selections

This makes it easier to find relevant foods.

### ❤️ Personalized Recommendations

HeartWise uses information from the user's profile to provide personalized food recommendations.

### 🍎 Food Details

Users can open individual food items to view detailed information, including:

* Food category
* Dietary information
* Nutritional values
* HeartWise recommendation
* Related recipe information

### 🍽️ Daily Meal Plan

The application provides personalized meal suggestions organized by meal type.

Meal information can include:

* Meal type
* Recipe name
* Description
* Ingredients
* Nutritional information
* Recipe link

### 📖 Recipe Details

Users can view detailed recipe information, including:

* Recipe name
* Description
* Ingredients
* Preparation instructions
* Recipe metadata
* HeartWise health tips

### 📱 Responsive Design

The interface is designed to work across:

* Desktop
* Laptop
* Tablet
* Mobile devices

Responsive layouts are implemented using CSS media queries.

---

## 🛠️ Technologies Used

### Frontend

* **HTML5** – Used to structure the web pages.
* **CSS3** – Used for styling, layouts, cards, forms, buttons, navigation, and responsive design.
* **JavaScript** – Used for client-side interactions and dynamic functionality where required.

### Backend

* **Python** – Used as the primary backend programming language.
* **Flask** – Used as the web framework for handling routes, requests, sessions, application logic, and communication between the frontend and database.

### Database

* **MySQL** – Used as the relational database for storing users, profiles, food information, and recipes.

### Design

* **Responsive Web Design**
* **CSS Media Queries**

---

## 🗄️ Database

The project uses a MySQL database named:

```text
heartwise_db
```

The database contains four main tables:

| Table           | Description                                                                                |
| --------------- | ------------------------------------------------------------------------------------------ |
| `users`         | Stores user account and authentication information.                                        |
| `user_profiles` | Stores user profile and dietary information used for personalization.                      |
| `foods`         | Stores food items, categories, dietary information, and nutritional details.               |
| `recipes`       | Stores recipe information, ingredients, preparation details, and related meal information. |

### Database Structure

```text
heartwise_db
│
├── users
├── user_profiles
├── foods
└── recipes
```

---

## 🏗️ System Architecture

HeartWise follows a basic three-layer web application structure:

```text
┌─────────────────────────────┐
│         Frontend            │
│     HTML + CSS + JavaScript │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Backend            │
│       Python + Flask        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Database           │
│           MySQL             │
│       heartwise_db          │
└─────────────────────────────┘
```

The Flask backend handles application requests and communicates with the MySQL database to retrieve and store application data.

---

## 📂 Project Structure

The exact file and folder structure may vary depending on the final project setup.

A typical Flask project structure is:

```text
HeartWise/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── foods.html
│   ├── food_details.html
│   ├── meal_plan.html
│   └── recipe_details.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── [JavaScript files]
│
├── database/
│   └── heartwise_db.sql
│
└── README.md
```

> The structure above is a general representation. Keep the actual filenames and folders from your project if they differ.

---

## ⚙️ Installation and Setup

### 1. Install Python

Make sure Python is installed on your computer.

Check the installation using:

```bash
python --version
```

---

### 2. Install MySQL

Install and configure MySQL Server.

Make sure the MySQL server is running before starting the application.

---

### 3. Create the Database

Open MySQL and create the database:

```sql
CREATE DATABASE heartwise_db;
```

---

### 4. Create the Required Tables

Import the SQL database file if it is included with the project:

```text
heartwise_db.sql
```

The database should contain:

```text
users
user_profiles
foods
recipes
```

---

### 5. Configure the Database Connection

Update the database configuration in the Flask application according to your local MySQL setup.

Typical configuration values are:

```text
Host: localhost
Database: heartwise_db
Username: root
Password: [YOUR MYSQL PASSWORD]
```

Use the MySQL username and password configured on your system.

---

### 6. Install Python Dependencies

If the project contains a `requirements.txt` file, install the required packages using:

```bash
pip install -r requirements.txt
```

If a requirements file is not included, install the packages required by the project manually according to the imports used in the Flask application.

---

### 7. Run the Flask Application

Start the Flask application using the project's configured entry point.

For example:

```bash
python app.py
```

The Flask development server will provide a local address, commonly:

```text
http://127.0.0.1:5000/
```

Open the address in a web browser to use HeartWise.

---

## 🔄 Application Workflow

The basic user workflow is:

```text
Register
   ↓
Login
   ↓
Complete Profile
   ↓
Dashboard
   ↓
Personalized Recommendations
   ↓
Explore Foods
   ↓
Search / Filter Foods
   ↓
View Food Details
   ↓
View Meal Plan
   ↓
View Recipe Details
```

---

## 🧩 Main Modules

### 1. User Authentication Module

Handles:

* Registration
* Login
* Logout
* Authentication
* Session management
* Login error handling

### 2. User Profile Module

Allows users to:

* Enter profile information
* Update profile information
* Maintain dietary preferences
* Provide information used for personalization

### 3. Food Recommendation Module

Uses available user profile information and food data to display relevant food recommendations.

### 4. Food Management Module

Provides:

* Food listing
* Food search
* Category filtering
* Food details
* Nutritional information

### 5. Meal Planning Module

Provides personalized meal suggestions organized by meal type.

### 6. Recipe Module

Provides detailed recipe information, including ingredients, preparation details, metadata, and HeartWise tips.

### 7. Dashboard Module

Provides a centralized view of the user's recommendations, food information, profile status, and meal planning features.

---

## 🧪 Testing

The major functionalities of the application were tested, including:

* User registration
* User login
* Invalid login handling
* Profile creation
* Profile updating
* Food listing
* Food search
* Category filtering
* Food details
* Personalized recommendations
* Meal plan display
* Recipe details
* Responsive layout
* Logout functionality

The major features were verified to function as intended.

---

## 🎯 Project Objectives

The main objectives of HeartWise are:

1. To develop a personalized healthy food recommendation system.
2. To provide nutritional information in an organized manner.
3. To simplify food discovery through search and filtering.
4. To provide personalized meal suggestions.
5. To provide detailed recipe information.
6. To maintain user profile information.
7. To develop a simple and responsive web interface.

---

## 🚀 Future Enhancements

Possible future improvements include:

* AI/ML-based food recommendations
* Calorie tracking
* Weekly and monthly meal planning
* Personalized nutrition goals
* Progress tracking
* Automatic shopping lists
* Meal reminders and notifications
* Larger food and recipe database
* Multilingual support
* Dedicated Android/iOS application

---

## ⚠️ Disclaimer

HeartWise is an academic mini-project developed for educational purposes.

The food recommendations and nutritional information provided by the application should not be considered a substitute for professional medical, dietary, or nutritional advice.

Users with specific medical or dietary requirements should consult a qualified healthcare or nutrition professional.

---

## 👨‍💻 Project Information

**Project Name:** HeartWise

**Project Type:** Mini Project

**Domain:** Health & Nutrition / Web Application

**Frontend:** HTML5, CSS3, JavaScript

**Backend:** Python, Flask

**Database:** MySQL

**Database Name:** `heartwise_db`

**Database Tables:**

```text
users
user_profiles
foods
recipes
```

---

## 📄 License

This project was developed as an academic mini-project for educational purposes.

© [2026] [Ancy Infant Jemi C]. All rights reserved.
