# ONI Rocket Calculator 🚀

A fan-made rocket range calculator for the game **Oxygen Not Included** by Klei Entertainment.

This web application allows players to:

- Build rockets interactively
- Calculate rocket range in real time
- Automatically configure rockets for a desired target range
- Use the tool in both English and Turkish

---

## Live Demo

Frontend:
https://onirocketcalculator.vercel.app/

Backend API:
https://onirocketcalculator.onrender.com/

---

## Features

### Rocket Builder

- Select engines
- Add/remove fuel tanks
- Configure oxidizers
- Add cargo and research modules
- Adjust internal fuel

### Real-Time Calculations

- Dry mass
- Propellant mass
- Wet mass
- Rocket range

### Automatic Rocket Configuration

Given:

- a target range
- an oxidizer type

the backend attempts to automatically configure the rocket to reach the desired destination.

### Validation & Warnings

The app warns users about:

- Missing engines
- Insufficient fuel
- Insufficient oxidizer
- Steam engine fuel requirements
- Inefficient fuel/oxidizer ratios

### Localization

- English
- Turkish

### Dark Mode

Supports light and dark themes.

---

# Tech Stack

## Frontend

- React
- TypeScript
- Chakra UI
- Axios
- Vite

## Backend

- FastAPI
- Python
- Pydantic

## Deployment

- Frontend hosted on Vercel
- Backend hosted on Render

---

# Running Locally

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/onirocketcalculator.git
cd onirocketcalculator
```

---

# Frontend Setup

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

---

# Backend Setup

Go into backend directory:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn api:app --reload
```

Backend will run on:

```txt
http://localhost:8000
```

---

# Notes

This is an unofficial fan-made project.

All Oxygen Not Included assets, logos, rocket designs, images, and related intellectual property belong to Klei Entertainment.

This project is not affiliated with Klei Entertainment.

---

# Author

Created by Burak Şahintürk.

GitHub:
https://github.com/https://github.com/BurakSahinturk

---

# License

This project is for educational and fan-use purposes only.
