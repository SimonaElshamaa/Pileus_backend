Pileus Backend

This is a Pileus backend project designed for production-ready usage, including async database access, authentication helpers, and modular structure. It is ready for development and deployment.



Project Structure
my_fastapi_app/
├── app/
│   ├── main.py             # FastAPI app instance
│   ├── config.py           # Environment configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic models
│   ├── crud/               # DB operations
│   ├── api/                # Routers/endpoints
│   ├── core/               # Security/auth helpers
│   ├── db/                 # Database connection/session
│   └── utils/              # Helper functions
├── tests/                  # Unit and integration tests
├── requirements.txt        # Python dependencies
├── Dockerfile              # Optional Docker setup
└── README.md

Setup Instructions
1. Clone the repository
git clone <your-repo-url>
cd my_fastapi_app

2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

3. Install dependencies
pip install "fastapi<1.0" uvicorn sqlalchemy aiosqlite "passlib[bcrypt]" httpx pytest "pydantic<2.0" greenlet "pydantic[email]"


Explanation of key packages:

"pydantic<2.0" → Ensures Pydantic v1 compatibility

"passlib[bcrypt]" → Password hashing

"pydantic[email]" → Required for EmailStr validation

greenlet → Required for async SQLAlchemy

fastapi<1.0 → Stable FastAPI version

4. Run the backend
uvicorn app.main:app --reload


App will run at http://127.0.0.1:8000

Swagger UI available at http://127.0.0.1:8000/docs

Testing

Run tests with:

pytest


Uses httpx for async API testing

Tests are located in the tests/ folder

Environment Variables

Create a .env file (optional) to override defaults in config.py:

DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Future Improvements

Switch to PostgreSQL for production

JWT authentication for users

Email verification / password reset

Docker and Docker Compose setup

Logging and monitoring