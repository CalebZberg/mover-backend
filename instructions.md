## Prerequisites
- Python 3.10+
- `git` for cloning the repo
- `curl` or `Invoke-RestMethod` for testing

## Setup

1. **Clone the repo & install dependencies**
   ```bash
   git clone git@github.com:<your-user>/mover-backend.git
   cd mover-backend
   ```
2. **Create and activate a virtual environment**
   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows PowerShell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. **Install Python packages**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running Locally

Start the FastAPI server with auto‑reload:
```bash
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000`.
- CORS is enabled for `http://localhost:3000` to allow your React frontend to communicate.

---

## API Endpoints

1. **Health check**  
   `GET /`  
   **Response:**  
   ```json
   { "message": "API is running" }
   ```

2. **Login**  
   `POST /auth/login`  
   **Request Body:**  
   ```json
   {
     "username": "test",
     "password": "xxx"
   }
   ```  
   **Responses:**
   - **200 OK**  
     ```json
     { "success": true, "username": "test" }
     ```  
   - **401 Unauthorized**  
     ```json
     { "detail": "Invalid credentials" }
     ```

3. **Create Quote**  
   `POST /quote/`  
   **Request Body:**  
   ```json
   {
     "origin": "100 Main St",
     "destination": "200 Oak Ave",
     "date": "2025-04-20",
     "inventory": "10 boxes, sofa"
   }
   ```  
   **Response:**  
   ```json
   {
     "distance": "n/a",
     "estimate": 75.0
   }
   ```  
   - Persists the quote record to `data/quotes.json`.

---

## JSON “Database”
- **Users** stored in `data/users.json`
- **Quotes** stored in `data/quotes.json`
- Both use the **Repository Pattern** implemented in `repositories/json_repository.py`.

---

## Testing

Use `curl` or PowerShell’s `Invoke-RestMethod`:

```bash
# Health check
curl http://localhost:8000/

# Login (ensure data/users.json contains test / xxx)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"xxx"}'

# Create a quote
curl -X POST http://localhost:8000/quote/ \
  -H "Content-Type: application/json" \
  -d '{"origin":"A","destination":"B"}'
```

Or in PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:8000/ -Method GET

# Login
Invoke-RestMethod \
  -Uri http://localhost:8000/auth/login \
  -Method POST \
  -ContentType "application/json" \
  -Body (@{ username = "test"; password = "xxx" } | ConvertTo-Json)

# Create a quote
Invoke-RestMethod \
  -Uri http://localhost:8000/quote/ \
  -Method POST \
  -ContentType "application/json" \
  -Body (@{ origin = "A"; destination = "B" } | ConvertTo-Json)
```

---

## EC2 Deployment (Backend Service)

On your AWS EC2 instance, create and configure a systemd service so that your backend runs continuously on startup:

1. **Clone the backend repo and set up a virtual environment**  
   ```bash
   cd /home/ubuntu
   git clone git@github.com:<your-user>/mover-backend.git
   cd mover-backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create the systemd service file**  
   Create `/etc/systemd/system/backend.service` with the following content:
   ```ini
   [Unit]
   Description=Bub's Movers FastAPI Backend
   After=network.target

   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/mover-backend
   ExecStart=/home/ubuntu/mover-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**  
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable backend.service
   sudo systemctl start backend.service
   ```

4. **Verify the service**  
   ```bash
   curl http://127.0.0.1:8000/
   ```
   You should see:
   ```json
   { "message": "API is running" }
   ```

