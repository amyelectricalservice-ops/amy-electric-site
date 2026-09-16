-- AMY Electric Gallery — D1 Database Schema
-- Run: npx wrangler d1 execute amyelectric_db --remote --file=schema.sql

-- Gallery images table
CREATE TABLE IF NOT EXISTS gallery_images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  width INTEGER DEFAULT 0,
  height INTEGER DEFAULT 0,
  alt_text TEXT,
  featured INTEGER DEFAULT 0,
  display_order INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE IF NOT EXISTS gallery_categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  display_order INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_gallery_category ON gallery_images(category);
CREATE INDEX IF NOT EXISTS idx_gallery_featured ON gallery_images(featured);
CREATE INDEX IF NOT EXISTS idx_gallery_order ON gallery_images(display_order);

-- Insert default categories
INSERT OR IGNORE INTO gallery_categories (slug, name, display_order) VALUES
  ('ev-charger', 'EV Charger Installation', 1),
  ('panel-upgrade', 'Panel Upgrade', 2),
  ('commercial', 'Commercial Electrical', 3),
  ('lighting', 'Lighting Installation', 4),
  ('rewiring', 'Whole-Home Rewiring', 5),
  ('repair', 'Electrical Repair', 6),
  ('residential', 'Residential', 7),
  ('emergency', 'Emergency Service', 8);
