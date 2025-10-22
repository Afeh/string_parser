# 🧠 String Analyzer API

A RESTful API service built with **FastAPI** that analyzes strings and stores their computed properties.  
Developed as part of the **HNG Backend — Stage 1 Task**.

---

## Features

The String Analyzer API can:
- Analyze any input string and compute key properties such as:
  - **Length** — number of characters
  - **Palindrome detection** — checks if the string reads the same backward
  - **Unique characters count**
  - **Word count**
  - **SHA-256 hash** — used as the unique ID
  - **Character frequency map**
- Retrieve analyzed strings individually or collectively
- Filter strings via query parameters
- Perform **natural language-based filtering** (e.g. _“all single word palindromic strings”_)
- Delete specific strings

---

## Tech Stack

- **Language:** Python  
- **Framework:** FastAPI  
- **Database:** SQLite (default, can be changed to PostgreSQL)  
- **ORM:** SQLAlchemy  
- **Deployed On:** Railway  

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/string-analyzer-api.git
cd string-analyzer-api
