# Aritra's Writing Editor

A professional, AI-powered writing companion designed to polish your drafts into a clear, engaging, and refined signature style.

## 🚀 Features

- **AI Polishing**: High-quality text refinement using state-of-the-art LLMs.
- **Modern UI**: A sleek, premium interface with a focus on readability and focus.
- **Draft History**: Manage and browse your past refinements with ease.
- **Permanent Storage**: Securely save your raw and polished drafts in a MySQL database.
- **Full Control**: Delete unwanted drafts and start fresh anytime.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- MySQL Server

### 2. Database Configuration
Run the following SQL commands to set up your database environment:

```sql
CREATE DATABASE IF NOT EXISTS ai_tools;

USE ai_tools;

CREATE TABLE IF NOT EXISTS drafts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    raw_text TEXT NOT NULL,
    polished_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Environment Setup
1. Clone the repository and navigate to the project root.
2. Initialize and activate your virtual environment.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create an `.env` file in the `editor_project/` directory with your MySQL credentials:
   ```env
   DB_NAME=ai_tools
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

### 4. AI Model Setup
To use the local high-performance model, download the Falcon weights using the Hugging Face CLI:

```bash
huggingface-cli download tiiuae/falcon-7b-instruct --local-dir ./models/falcon-7b
```

### 5. Running the Application
Start the Django development server:

```bash
cd editor_project
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000`.

## 🧠 AI Configuration
Currently, the editor uses **DistilGPT-2** for efficient local processing, but it is configured to support **Falcon-7B** for even higher quality refinements.

---
&copy; 2026 Aritra's Personal Writing Editor.
