🚀 Pileus Backend

Pileus Backend is a production-ready backend built with FastAPI, designed with scalability, async database access, authentication helpers, and a clean modular architecture.
It is ready for both local development and deployment.

✨ Features

⚡ FastAPI with async support

🗄️ Async SQLAlchemy database access

🔐 Authentication & security helpers

🧱 Modular, scalable project structure

🧪 Unit & integration testing setup


📁 Project Structure
my_fastapi_app/
├── app/
│   ├── main.py             # FastAPI app instance
│   ├── config.py           # Environment configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic models
│   ├── crud/               # Database operations
│   ├── api/                # Routers / endpoints
│   ├── core/               # Security & authentication helpers
│   ├── db/                 # Database connection & session
│   └── utils/              # Helper utilities
├── tests/                  # Unit & integration tests
├── requirements.txt        # Python dependencies
├── Dockerfile              # Optional Docker setup
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone <your-repo-url>
cd my_fastapi_app

2️⃣ Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows

3️⃣ Install dependencies
pip install "fastapi<1.0" uvicorn sqlalchemy aiosqlite \
"passlib[bcrypt]" httpx pytest "pydantic<2.0" \
greenlet "pydantic[email]"

📦 Key packages explained
Package	Purpose
fastapi<1.0	Stable FastAPI version
pydantic<2.0	Ensures Pydantic v1 compatibility
passlib[bcrypt]	Secure password hashing
pydantic[email]	EmailStr validation
greenlet	Required for async SQLAlchemy
httpx	Async API testing
4️⃣ Run the backend
uvicorn app.main:app --reload


✅ App runs at:
👉 http://127.0.0.1:8000

📘 Swagger UI:
👉 http://127.0.0.1:8000/docs

🧪 Testing

Run all tests with:

pytest


Uses httpx for async API testing

Tests are located in the tests/ directory

🔐 Environment Variables

Create a .env file (optional) to override defaults from config.py:

DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

🛣️ Future Improvements

🔄 Switch to PostgreSQL for production

🔑 Full JWT authentication

📧 Email verification & password reset

📊 Logging & monitoring
