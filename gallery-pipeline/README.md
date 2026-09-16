# AMY Electric Gallery Pipeline

Automated image processing, R2 storage, and D1 database seeding for the AMY Electric project gallery.

## Quick Start

```bash
# 1. Setup dependencies
./setup.sh

# 2. Place raw images in raw/
cp /path/to/photos/* raw/

# 3. Run pipeline
./build_gallery.sh

# 4. Upload to R2 and seed D1
./build_gallery.sh --upload --db
```

## Directory Structure

```
gallery-pipeline/
├── raw/              # Place unprocessed images here
├── processed/        # Output directory (auto-created)
├── sql/              # Generated SQL files (auto-created)
├── scripts/          # Helper scripts
├── build_gallery.sh  # Main pipeline script
├── setup.sh          # Dependency installer
├── schema.sql        # D1 database schema
└── rclone-config.conf # R2 config template
```

## What It Does

### 1. Image Processing
- Force-lowercases uppercase extensions (`.JPG` → `.jpg`)
- Replaces spaces/punctuation with hyphens
- Adds sequential numbers to prevent collisions
- Resizes to max 1200px width (preserves aspect ratio)
- Creates WebP versions for modern browsers

**Before:** `IMG_20260611_080337908_HDR.JPG`  
**After:** `ev-charger-img-20260611-080337908-hdr-01.jpg`

### 2. R2 Upload
- Syncs processed images to `amyelectric-gallery` bucket
- Uses rclone for parallel uploads
- Zero egress fees via Cloudflare R2

### 3. D1 Database Seeding
- Generates `batch_insert.sql` with all image metadata
- Inserts filename, category, title, dimensions
- Ready for dynamic gallery rendering

## Configuration

### R2 Credentials
Edit `~/.config/rclone/rclone.conf`:
```ini
[amyelectric]
type = s3
provider = Cloudflare
access_key_id = YOUR_KEY
secret_access_key = YOUR_SECRET
endpoint = https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
acl = public-read
bucket_policy = true
```

### D1 Database
```bash
# Create database
npx wrangler d1 create amyelectric_db

# Run schema
npx wrangler d1 execute amyelectric_db --remote --file=schema.sql
```

### Image Settings (in build_gallery.sh)
```bash
MAX_WIDTH=1200      # Max output width
QUALITY=85          # JPEG quality
WEBP_QUALITY=80     # WebP quality
```

## Auto-Categorization

Images are auto-categorized based on filename patterns:

| Pattern | Category |
|---------|----------|
| ev, charger, tesla | EV Charger |
| panel, breaker, subpanel | Panel Upgrade |
| commercial, bus duct | Commercial |
| light, recessed | Lighting |
| rewire, knob tube | Rewiring |
| repair, outlet | Repair |

## Frontend Usage

Query D1 for gallery:
```sql
-- Get all images
SELECT * FROM gallery_images ORDER BY display_order;

-- Get by category
SELECT * FROM gallery_images WHERE category = 'ev-charger';

-- Get featured only
SELECT * FROM gallery_images WHERE featured = 1;
```

## Dependencies

- `rclone` — R2 sync
- `npx` — D1 execution
- `imagemagick` — Image processing (optional, falls back to copy)
- `jq` — JSON parsing (optional)
