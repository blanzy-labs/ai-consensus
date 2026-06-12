# Mythadis Consensus Engine: Quick Troubleshooting Guide

This guide covers common issues people may run into when installing or running Mythadis Consensus Engine locally.

## 1. Docker is not installed

**Problem:**
`docker: command not found` or Docker commands are not recognized.

**Quick fix:**
Install Docker Desktop or Docker Engine for your operating system.

**Check:**

```bash
docker --version
docker compose version
```

Both commands should return version information.

---

## 2. Docker Desktop or Docker service is not running

**Problem:**
You see an error such as:

```text
failed to connect to the docker API
Cannot connect to the Docker daemon
docker.sock: no such file or directory
```

**Quick fix:**
Start Docker Desktop on Mac/Windows, or start the Docker service on Linux.

**Mac/Windows:**
Open Docker Desktop and wait until it says Docker is running.

**Linux:**

```bash
sudo systemctl start docker
sudo systemctl status docker
```

Then retry:

```bash
docker compose up --build
```

---

## 3. Docker context or socket is wrong

**Problem:**
Docker is installed and running, but the terminal still points to the wrong Docker socket or context.

**Quick fix:**
Check your Docker context:

```bash
docker context ls
```

On Docker Desktop, try:

```bash
docker context use desktop-linux
```

Also check whether `DOCKER_HOST` is set:

```bash
echo $DOCKER_HOST
```

If it points to an old or missing socket, clear it:

```bash
unset DOCKER_HOST
```

Then test:

```bash
docker info
```

---

## 4. `.env` file is missing

**Problem:**
The backend starts, but the app reports missing API keys.

**Quick fix:**
Create your local `.env` file from the example:

```bash
cp .env.example .env
```

Then edit `.env` and add your provider keys:

```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

Do not commit `.env` to GitHub.

---

## 5. Docker Compose is loading `.env.example` instead of `.env`

**Problem:**
You added real keys to `.env`, but the backend still says:

```text
OpenAI API key is not configured.
```

**Quick fix:**
Check `docker-compose.yml`. The backend service should load `.env`, not `.env.example`.

Correct:

```yaml
services:
  backend:
    env_file:
      - .env
```

Incorrect:

```yaml
services:
  backend:
    env_file:
      - .env.example
```

After fixing it:

```bash
docker compose down
docker compose up --build
```

---

## 6. API key is wrong, expired, or from the wrong provider account

**Problem:**
The app starts, but OpenAI or Gemini calls fail.

**Quick fix:**
Confirm the keys are valid and copied correctly into `.env`.

Check that the backend container can see the key without printing the key itself:

```bash
docker compose exec backend printenv OPENAI_API_KEY | wc -c
docker compose exec backend printenv GEMINI_API_KEY | wc -c
```

Each count should be greater than `1`.

Do not paste your real API keys into GitHub issues, chat, screenshots, or logs.

---

## 7. Gemini model name is outdated

**Problem:**
Gemini returns a model error, model-not-found error, or unsupported model error.

**Quick fix:**
Check the `GEMINI_MODEL` value in `.env`.

Recommended default:

```env
GEMINI_MODEL=gemini-2.5-flash
```

If Google changes model availability, update the model name in `.env` to a currently supported Gemini API model.

Then restart:

```bash
docker compose down
docker compose up --build
```

---

## 8. Port 8000 or 5173 is already in use

**Problem:**
Docker fails because a port is already allocated or the browser cannot reach the app.

Default ports:

```text
Backend:  http://localhost:8000
Frontend: http://localhost:5173
```

**Quick fix:**
Find what is using the port.

**Mac/Linux:**

```bash
lsof -i :8000
lsof -i :5173
```

Stop the conflicting process, or change the port mapping in `docker-compose.yml`.

Then restart:

```bash
docker compose down
docker compose up --build
```

---

## 9. Browser cache or old frontend state

**Problem:**
The frontend loads, but behaves strangely after recent changes.

**Quick fix:**
Try a hard refresh.

**Chrome/Edge/Firefox:**

```text
Ctrl + Shift + R
```

**Mac:**

```text
Cmd + Shift + R
```

You can also try an incognito/private window.

If running Docker, rebuild the frontend:

```bash
docker compose down
docker compose up --build
```

---

## 10. Local Python setup issues

**Problem:**
Running backend tests locally fails with missing packages such as:

```text
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'pydantic_settings'
```

**Quick fix:**
Run backend tests from the backend virtual environment.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

If you are on Windows:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

Docker users do not need to run Python locally unless they are developing the backend.

---

# Quick Health Check

After starting the app, verify the backend:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "mythadis-consensus-engine-backend"
}
```

Then open the frontend:

```text
http://localhost:5173
```

# Security Reminder

Never share or commit your `.env` file. Your OpenAI and Gemini API keys should remain local to your machine.

