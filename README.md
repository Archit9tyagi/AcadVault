# AcadVault 📚

**AcadVault** is a comprehensive academic resource sharing platform designed to help students easily upload, share, and access study materials. Built with Django and Bootstrap, it offers a user-friendly interface for managing notes across various engineering branches and years.

## 🚀 Features

-   **User Authentication**: Secure signup and login system.
-   **Note Management**:
    -   **Upload**: Users can upload PDF notes with metadata (Title, Subject, Branch, Year, Description).
    -   **Download**: Easy access to download notes.
    -   **Preview**: Instant in-browser PDF preview.
    -   **Delete**: Users can manage and delete their own uploaded notes.
-   **Search & Filter**: Find notes quickly by searching keywords or filtering by Branch and Year.
-   **Dashboard**: Personalized dashboard to track uploads, downloads, and reviews.
-   **Review System**: Rate and review notes to help others find quality content.
-   **Responsive Design**: Fully responsive UI built with Bootstrap 5.

## 🛠️ Tech Stack

-   **Backend**: Django (Python)
-   **Frontend**: HTML5, CSS3, Bootstrap 5
-   **Database**: SQLite (Default)
-   **Icons**: Bootstrap Icons

## ⚙️ Installation

Follow these steps to set up the project locally:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Archit9tyagi/AcadVault.git
    cd AcadVault
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

6.  **Access the app**
    Open your browser and go to `http://127.0.0.1:8000/`

## 📖 Usage

1.  **Sign Up/Login**: Create an account to start uploading.
2.  **Upload Notes**: Navigate to "Upload Note" and fill in the details.
3.  **Browse**: Use the "Browse Notes" section to find materials.
4.  **Dashboard**: Check your "My Uploads" section to manage your contributions.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License.
