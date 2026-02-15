## Introduction
This project implements a low-latency, deterministic Reward Decision microservice using FastAPI.
The service evaluates transactions and returns a reward outcome based on configurable policies.

# Components
 FastAPI – HTTP interface

 RewardService – Core business logic

 PolicyConfig – YAML-driven configuration

 MemoryCache - Cache abstraction

 Pytest – Unit testing

 k6 – Load testing

# Architecture

The service follows a layered architecture:
`API Layer → Service Layer → Policy Engine → Cache Layer`

- API Layer handles HTTP requests and validation.
- RewardService contains business logic.
- PolicyConfig loads rules from YAML configuration.
- CacheBase abstracts memory/Redis caching.
- Business logic is fully deterministic and side-effect controlled.

# API ## Endpoint
  POST /reward/decide

### Request Body

{
  "txn_id": "string",
  "user_id": "string",
  "merchant_id": "string",
  "amount": 100,
  "txn_type": "ONLINE",
  "ts": 1700000000
}

### Response

{
  "decision_id": "string",
  "policy_version": "v1",
  "reward_type": "XP",
  "reward_value": 300,
  "xp": 300,
  "reason_codes": [],
  "meta": {
    "persona": "NEW"
  }
}

# Core Features
  Deterministic Decision Logic - SHA256(txn_id + user_id + merchant_id + policy_version)
  Idempotency - idem:{txn_id}:{user_id}:{merchant_id}
  XP Calculation - xp = min(amount × xp_per_rupee × persona_multiplier, max_xp_per_txn)
  Daily CAC Cap Enforcement - Monetary rewards blocked
  Caching Strategy - MemoryCache (Redis not available)

# Running the Service
   Create Virtual Environment Windows/Mac/Linux - `python -m venv venv`
   Install Dependencies -  `pip install -r requirements.txt`
   Run Server - `uvicorn app.main:app --reload`
   Access Swagger UI - [http://127.0.0.1:8000/docs]

# Unit Testing
 Tests cover:
    Reward logic
    Idempotency behavior
    CAC cap enforcement
 
###### Run pytest
 
# Load Testing
  Load testing was performed using k6 - >  
Scenario:
300 requests per second
30 seconds duration
Constant arrival rate

###### Run k6 run load_test.js 

# Performance Results (Windows, Single Worker - uvicorn app.main:app)
    Sustained throughput: ~227 RPS
    Median latency: ~17ms
    p95 latency: ~1.95s
    0% request failures
    Dropped iterations observed due to CPU saturation

# Bottlenecks Identified
    Single-threaded Uvicorn worker
    Python GIL limitations
    SHA256 hashing overhead
    JSON serialization cost
    Windows environment limiting multi-worker scaling

# Suggested Improvements
  Deploy using multiple Uvicorn/Gunicorn workers (Linux)
  Use Redis for distributed caching
  Horizontal scaling behind load balancer
  Use faster JSON serialization (e.g., orjson)
  Optimize hashing if necessary

# Assumptions
    Persona data is mocked using in-memory mapping.
    Reward types are simplified to XP for this implementation.
    Redis support is implemented but optional.
    Performance results were measured locally on Windows.

