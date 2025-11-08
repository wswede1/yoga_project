## YogaDB – Yoga Pose Finder

YogaDB is a small Flask + MySQL application I built for LING 508 at the University of Arizona. It helps knowledge workers (and grad students!) quickly discover yoga poses that target specific areas of tension—perfect for stretching between Pomodoro sessions.

### Highlight Reel
- Modern single-page UI styled with Bootstrap and a subtle gradient aesthetic
- `/pose` API endpoint returning curated pose data (names, benefits, step-by-step instructions)
- Clean service layer with MySQL repository + unit tests that mock database access
- Dockerised MySQL seed data for instant demo content


---

## Tech Stack
- Backend: Flask, `flask-cors`
- Database: MySQL 8 (via `mysql-connector-python`)
- Frontend: Jinja2 template + Bootstrap 5 + vanilla ES modules
- Tests: Pytest-style unit tests with lightweight stubs

---

## Getting Started

### 1. Clone & install dependencies
```bash
git clone https://github.com/wswede1/yoga_project.git
cd yoga_project
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start MySQL with seed data
```bash
docker compose up db
```
The compose file provisions MySQL on `localhost:32000` with the database `yoga` and seeds a handful of showcase poses from `data/init.sql`.

### 3. Run the Flask API + UI
```bash
export FLASK_APP=app.py
flask run --reload
```
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to play with the new interface. Enter a focus area (e.g., `hips`, `shoulders`, `hamstrings`) and explore detailed instructions.

---

## Pose Catalog
- The curated dataset in `data/pose_catalog.json` lists **100** unique poses spanning hips, shoulders, spine, core, hamstrings, wrists, and more.
- Load the catalog into MySQL with the helper script:
  ```bash
  source .venv/bin/activate
  python scripts/load_poses.py          # adds any missing poses
  python scripts/pose_stats.py          # prints coverage summary
  ```
- Current coverage highlights (top 10 body parts):
  - Shoulders 44
  - Spine 36
  - Hamstrings 28
  - Core 24
  - Hips 24
  - Glutes 13
  - Hip Flexors 12
  - Ankles 11
  - Inner Thighs 10
  - Side Body 10

---

## API Overview

| Verb | Route    | Query Params | Description                                  |
|------|----------|--------------|----------------------------------------------|
| GET  | `/pose`  | `body_part`  | Returns curated poses targeting the keyword. |

Example:
```bash
curl "http://127.0.0.1:5000/pose?body_part=hips"
```
Response:
```json
{
  "poses": [
    {
      "english_name": "Bharadvaja's Twist",
      "sanskrit_name": "Bharadvajasana I",
      "pose_type": ["Hip-Opening Yoga Poses", "Seated Yoga Poses", "Twist Yoga Poses"],
      "target_body_parts": ["Hips", "Spine", "Shoulders"],
      "instructions": "Sit on the floor with legs straight out..."
    }
  ]
}
```

---

## Testing
- All unit tests live under `test/`
- They mock the repository layer so you can run them without a live database

```bash
pytest
```

---

Feel free to reach out if you’d like to collaborate!  

