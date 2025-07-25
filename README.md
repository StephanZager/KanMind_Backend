# KanMind Backend API

This is a backend API service for a Kanban board application, built with Python, Django, and the Django REST Framework. The API allows for the management of boards, tasks, and comments with a role-based permission system where users can share and collaborate on boards.

---

## 🔧 Features

-   **User Authentication:** Registration and token-based login.
-   **Board Management:** Create, read, update, and delete (CRUD) operations for boards.
-   **Collaboration:** Users can invite other registered users to their boards as members.
-   **Task Management:** Full management of tasks within boards.
-   **Comment System:** Add and delete comments on tasks.
-   **Permission System:** Clear, role-based rules (Owner, Board Member, Task Creator).

---

## 🚀 Tech Stack

-   **Python 3.13.1**
-   **Django 5.2**
-   **Django REST Framework (DRF)**
-   **SQLite** (for development)
-   **CORS Support** (via `django-cors-headers`)

---

## 📁 Project Structure

```
KanMind_Backend/
├── user_auth_app/    # Manages registration, login, etc.
├── kanban_app/       # Core logic for boards, tasks, comments
├── core/             # Main settings and URL routing
├── manage.py
└── db.sqlite3
```

---

## 📦 Installation

Follow these steps to set up and run the project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/StephanZager/KanMind_Backend.git](https://github.com/StephanZager/KanMind_Backend.git)
    cd KanMind_Backend
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv env
    ```

3.  **Activate the virtual environment**
    -   On **macOS / Linux**:
        ```bash
        source venv/bin/activate
        ```
    -   On **Windows**:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```
    The API is now available at `http://127.0.0.1:8000/`.

---

## 🔑 API Endpoints

#### Authentication
-   `POST /api/registration/` – Register a new user.
-   `POST /api/login/` – Log in a user and receive a token.
-   `GET /api/email-check/` – Check if an email is already registered.

#### Boards
-   `GET /api/boards/` – Lists all boards where the user is either the owner or a member.
-   `POST /api/boards/` – Create a new board. The creator is automatically set as the owner.
-   `GET /api/boards/{board_id}/` – Retrieve details of a specific board (members/owner only).
-   `PATCH /api/boards/{board_id}/` – Update a board's title and members.
-   `DELETE /api/boards/{board_id}/` – Delete a board (owner only).

#### Tasks
-   `POST /api/tasks/` – Create a new task in a board (board members/owner only).
-   `GET /api/tasks/assigned-to-me/` – List tasks assigned to the user.
-   `GET /api/tasks/reviewing/` – List tasks the user is set to review.
-   `PATCH /api/tasks/{task_id}/` – Update a task (board members only).
-   `DELETE /api/tasks/{task_id}/` – Delete a task (board owner or task creator only).

#### Comments
-   `GET /api/tasks/{task_id}/comments/` – List comments on a task (board members only).
-   `POST /api/tasks/{task_id}/comments/` – Add a comment to a task (board members only).
-   `DELETE /api/tasks/{task_id}/comments/{comment_id}/` – Delete a comment (comment author only).

---

## ⚙️ Requirements

The exact versions of the dependencies are specified in `requirements.txt`:
```
asgiref==3.8.1
Django==5.2
django-cors-headers==4.7.0
djangorestframework==3.16.0
drf-nested-routers==0.94.2
sqlparse==0.5.3
tzdata==2025.2
```

---

## 📌 Notes

-   Users can access boards they own or have been added to as a member. This allows for collaboration.
-   CORS is configured to allow frontend applications to communicate with the backend.
-   For a production environment, the SQLite database should be replaced with a more robust solution like PostgreSQL.
