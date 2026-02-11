# LLM Document Assistant

> An asynchronous PDF processing system using Google Gemini AI for intelligent document analysis

----

## 📋 What It Does

Upload a PDF → System converts it to images → Gemini AI analyzes content → Get AI-generated insights

**Use Case**: Automated resume roaster and feedback (can be adapted for any document type)

----

## 🏗️ Architecture

```
Client → FastAPI → MongoDB (metadata) → Redis Queue → Worker
                ↓                                        ↓
           File Storage                          PDF → Images → Gemini AI
                                                         ↓
                                                   Store Result
```

**Flow**:
1. Client uploads PDF via REST API
2. File saved to disk, metadata stored in MongoDB
3. Processing job queued in Redis
4. Background worker converts PDF pages to images
5. Images sent to Gemini AI for analysis
6. AI response stored back in MongoDB
7. Client retrieves result via API

----

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI + Uvicorn |
| **Database** | MongoDB (async) |
| **Queue** | Redis + RQ |
| **AI Model** | Google Gemini (via OpenAI SDK) |
| **PDF Processing** | pdf2image + Pillow |
| **Async I/O** | aiofiles |

----

## 🚀 Quick Start

### Option 1: Using DevContainer (Recommended)

1. **Prerequisites**: Docker + VS Code with Dev Containers extension

2. **Clone & Open**:
   ```bash
   git clone https://github.com/pmmaster12/LLM-Document-Assistant.git
   cd LLM-Document-Assistant
   ```

3. **Open in DevContainer**: 
   - VS Code → `F1` → "Dev Containers: Reopen in Container"
   - All dependencies (MongoDB, Redis, Python) auto-configured!

4. **Set API Key**:
   ```bash
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```

5. **Run**:
   ```bash
   # Terminal 1: Start API
   python -m app.main

   # Terminal 2: Start Worker
   rq worker --with-scheduler
   ```

### Option 2: Manual Setup

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Services**:
   ```bash
   # MongoDB
   docker run -d -p 27017:27017 --name mongo \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=admin mongo

   # Redis
   docker run -d -p 6379:6379 --name valkey valkey/valkey
   ```

3. **Configure & Run** (same as steps 4-5 above)

----

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload PDF (returns `file_id`) |
| `GET` | `/{id}` | Get status & result |

**Example**:
```bash
# Upload
   curl -X POST http://localhost:8000/upload -F "file=@resume.pdf"
# Response: {"file_id": "507f1f77bcf86cd799439011"}

# Check status
   curl http://localhost:8000/507f1f77bcf86cd799439011
# Response: {"status": "processed", "result": "AI analysis..."}
```

----

## 📁 Project Structure

```
app/
├── main.py           # Entry point
├── server.py         # FastAPI routes
├── db/               # MongoDB client & schemas
├── queue/            # Redis queue & workers
└── utils/            # File I/O helpers
```

----

## 🎯 Key Features

✅ **Async-first design** - Non-blocking I/O for scalability  
✅ **Distributed processing** - Redis queue for horizontal scaling  
✅ **Multimodal AI** - Gemini vision model for document understanding  
✅ **Production-ready** - Status tracking, error handling, modular code  
✅ **DevContainer support** - One-click development environment

----

## 👨‍💻 Developer

**Tarun Gupta** | [@pmmaster12](https://github.com/pmmaster12)