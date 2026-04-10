// CultGig Backend — Express.js + Mongoose Entry Point
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const waitlistRoutes = require("./routes/waitlist");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection — use local MongoDB (managed by platform)
const MONGO_URI =
  process.env.MONGO_URI || "mongodb://localhost:27017/cultgigDB";
const PORT = process.env.PORT || 5000;

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("MongoDB connected — CultGig DB ready"))
  .catch((err) => console.error("MongoDB connection error:", err));

// Routes
app.use("/api/waitlist", waitlistRoutes);

// Health check
app.get("/api", (req, res) => {
  res.json({ message: "CultGig Node.js API is running", status: "ok" });
});

app.get("/api/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "CultGig Node.js API",
    version: "1.0.0",
  });
});

// Start server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`CultGig server running on port ${PORT}`);
});
