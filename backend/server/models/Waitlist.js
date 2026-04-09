// Waitlist Mongoose Schema & Model
const mongoose = require('mongoose');

const waitlistSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
  },
  whatsapp: {
    type: String,
    required: true,
    trim: true,
    // Stored as string to preserve leading zeros and country codes (e.g. +91XXXXXXXXXX)
  },
  role: {
    type: String,
    enum: ['artist', 'business'],
    required: true,
  },
  joinedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Waitlist', waitlistSchema);
