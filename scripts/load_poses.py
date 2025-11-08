import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.mysql_repository import MySQLRepository
from model.yoga_pose import YogaPose


def load_poses(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of poses in {path}, got {type(data).__name__}")

    for item in data:
        try:
            yield {
                "english_name": item["english_name"].strip(),
                "sanskrit_name": item.get("sanskrit_name", "").strip(),
                "pose_type": item.get("pose_type", "").strip(),
                "target_body_parts": item.get("target_body_parts", "").strip(),
                "instructions": item.get("instructions", "").strip(),
            }
        except KeyError as exc:
            raise ValueError(f"Pose entry missing required field {exc!s}: {item}") from exc


def ingest(poses: Iterable[dict], dry_run: bool = False) -> Tuple[int, int]:
    repository = MySQLRepository()
    inserted, skipped = 0, 0

    for pose_dict in poses:
        english_name = pose_dict["english_name"]
        existing = repository.load_pose(english_name)
        if existing:
            skipped += 1
            continue

        if dry_run:
            inserted += 1
            continue

        pose = YogaPose(**pose_dict)
        repository.add_pose(pose)
        inserted += 1

    return inserted, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Load yoga poses into the MySQL database.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("data/pose_catalog.json"),
        help="Path to a JSON file containing pose entries (default: data/pose_catalog.json).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse the file and report how many poses would be inserted without modifying the database.",
    )

    args = parser.parse_args()

    poses = list(load_poses(args.file))
    inserted, skipped = ingest(poses, dry_run=args.dry_run)

    action = "would insert" if args.dry_run else "inserted"
    print(f"{action.capitalize()} {inserted} poses.")
    print(f"Skipped {skipped} existing poses.")
    if args.dry_run:
        print("Run again without --dry-run to write the data.")


if __name__ == "__main__":
    main()

