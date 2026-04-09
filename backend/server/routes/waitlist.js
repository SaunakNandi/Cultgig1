// Waitlist API Routes — POST /api/waitlist
const express = require('express');
const router = express.Router();
const Waitlist = require('../models/Waitlist');

// POST /api/waitlist — Add user to waitlist
router.post('/', async (req, res) => {
  try {
    const { name, email, whatsapp, role } = req.body;

    // Validate all fields are present
    if (!name || !email || !whatsapp || !role) {
      return res.status(400).json({
        success: false,
        message: 'All fields are required',
      });
    }

    // Check if email already exists
    const existing = await Waitlist.findOne({ email: email.toLowerCase().trim() });
    if (existing) {
      return res.status(409).json({
        success: false,
        message: 'Email already registered',
      });
    }

    // Save new waitlist entry
    const entry = new Waitlist({ name, email, whatsapp, role });
    await entry.save();

    return res.status(201).json({
      success: true,
      message: "You're on the waitlist!",
    });
  } catch (err) {
    console.error('Waitlist error:', err);
    return res.status(500).json({
      success: false,
      message: 'Server error. Try again.',
    });
  }
});

// GET /api/waitlist — List all entries
router.get('/', async (req, res) => {
  try {
    const entries = await Waitlist.find().sort({ joinedAt: -1 });
    return res.json({ success: true, data: entries });
  } catch (err) {
    return res.status(500).json({ success: false, message: 'Server error' });
  }
});

// GET /api/waitlist/count — Count entries
router.get('/count', async (req, res) => {
  try {
    const count = await Waitlist.countDocuments();
    return res.json({ success: true, count });
  } catch (err) {
    return res.status(500).json({ success: false, message: 'Server error' });
  }
});

module.exports = router;
