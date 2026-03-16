
# FastAPI Chatbox Project - Vlad-Andrei Mocan

A FastAPI-based backend application featuring authentication, database integration, and a clean modular structure. This guide walks you through cloning the project, setting up the environment, and running the server using **uv**.

---

## 1. Clone the Repository

```sh
git clone <https://github.com/Vlad-Mocan/chatbox.git>
cd fastapi
```

---

## 2. Create & Sync the Virtual Environment (using uv)

This project uses **uv** for dependency management.

Create the environment (if not already created):

```sh
uv venv
```

Install all dependencies:

```sh
uv sync
```

Activate the environment:

```sh
source .venv/bin/activate
```

---

## 3. Environment Variables

The application uses **Pydantic Settings**, so you must provide required configuration values.

Create a `.env` file in the project root:

```
SQLITE_DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

These values are required for the app to start.

---

## 4. Running the Application

### **Option A — Run Uvicorn directly (recommended)**

From the project root:

```sh
uv run uvicorn app.main:app --reload
```

### **Option B — Run the module (executes main())**

```sh
uv run -m app.main
```

---

## 5. Testing the API

Once the server is running, open:

```
http://localhost:8000/docs
```

This loads the interactive Swagger UI where you can test all endpoints.

---