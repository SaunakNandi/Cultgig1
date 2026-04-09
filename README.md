# CultGig — 3D Landing Page

A modern, single-page responsive 3D landing page for **CultGig** — a talent marketplace platform connecting artists and freelancers with businesses and venues.

---

## Tech Stack

| Layer       | Technology                                                  |
| ----------- | ----------------------------------------------------------- |
| Frontend    | React 19, Tailwind CSS 3, Framer Motion, Shadcn/UI         |
| 3D Graphics | Three.js (vanilla) with UnrealBloom post-processing         |
| Backend     | **Node.js + Express.js + Mongoose**                         |
| Database    | MongoDB                                                     |
| Proxy       | FastAPI (thin proxy layer, infrastructure requirement)      |

---

## Project Structure

```
/app/
├── backend/
│   ├── server/                    # Node.js Express backend
│   │   ├── models/
│   │   │   └── Waitlist.js        # Mongoose schema (name, email, whatsapp, role)
│   │   ├── routes/
│   │   │   └── waitlist.js        # POST/GET /api/waitlist routes
│   │   ├── server.js              # Express app entry point (port 5000)
│   │   ├── package.json           # Node.js dependencies
│   │   └── .env                   # MONGO_URI, PORT
│   ├── server.py                  # FastAPI proxy (routes to Node.js)
│   ├── requirements.txt           # Python proxy dependencies
│   └── .env                       # Platform env vars
├── frontend/
│   ├── src/
│   │   ├── App.js                 # Main app (composes all sections)
│   │   ├── App.css                # Custom animations
│   │   ├── index.css              # Global styles, fonts, Tailwind
│   │   └── components/
│   │       ├── Navbar.jsx         # Sticky nav + mobile hamburger
│   │       ├── HeroScene.jsx      # Vanilla Three.js 3D canvas + Bloom
│   │       ├── Hero.jsx           # Hero content (center-aligned)
│   │       ├── Features.jsx       # 2-column feature cards
│   │       ├── HowItWorks.jsx     # Tabbed 3-step timeline
│   │       ├── AppDownload.jsx    # Phone mockup + store buttons
│   │       ├── WaitlistSignup.jsx # Form with WhatsApp + API integration
│   │       ├── Footer.jsx         # Footer with social links
│   │       └── ui/                # Shadcn/UI components
│   ├── package.json
│   └── .env
└── README.md
```

---

## Running the Project

### Backend (Node.js)
```bash
cd /app/backend/server
npm install
npm run dev
```
The Node.js server starts on **port 5000** with Express + Mongoose.

### Frontend (React)
```bash
cd /app/frontend
yarn install
yarn start
```
The React dev server starts on **port 3000**.

---

## API Endpoints

| Method | Endpoint              | Description                         |
| ------ | --------------------- | ----------------------------------- |
| GET    | `/api/`               | Health check                        |
| GET    | `/api/health`         | Detailed health check               |
| POST   | `/api/waitlist`       | Join waitlist (name, email, whatsapp, role) |
| GET    | `/api/waitlist`       | List all waitlist entries            |
| GET    | `/api/waitlist/count` | Get total waitlist count             |

### POST /api/waitlist

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "whatsapp": "+919876543210",
  "role": "artist"
}
```

**Responses:**
- `201` — `{ "success": true, "message": "You're on the waitlist!" }`
- `400` — `{ "success": false, "message": "All fields are required" }`
- `409` — `{ "success": false, "message": "Email already registered" }`
- `500` — `{ "success": false, "message": "Server error. Try again." }`

---

## Environment Variables

### Backend Node.js (`/app/backend/server/.env`)
```
MONGO_URI=mongodb://localhost:27017/cultgigDB
PORT=5000
```

### Frontend (`/app/frontend/.env`)
```
REACT_APP_BACKEND_URL=<preview-url>
```

---

## Design System

| Element        | Value                              |
| -------------- | ---------------------------------- |
| Primary Accent | `#EAFF00` (electric yellow-green)  |
| Background     | `#000000` to `#0a0a0a`            |
| Surfaces       | `#111111` / `#1a1a1a`             |
| Heading Font   | Syne                               |
| Body Font      | Satoshi                            |

---

## License

Copyright 2025 CultGig. All rights reserved.
