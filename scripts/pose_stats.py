import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.mysql_repository import MySQLRepository


def load_catalog(path: Path) -> Iterable[Dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"Expected list of poses in {path}, got {type(data).__name__}")
    return data


def summarise_targets(poses: Iterable[Dict[str, str]]) -> Counter:
    counter: Counter = Counter()
    for pose in poses:
        parts = [part.strip() for part in pose["target_body_parts"].split(",")]
        counter.update(part for part in parts if part)
    return counter


def fetch_database_total() -> int:
    repository = MySQLRepository()
    connection = repository._get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM yoga_poses")
    total = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise pose catalog statistics.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("data/pose_catalog.json"),
        help="Path to the pose catalog JSON file (default: data/pose_catalog.json).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top targeted body parts to display (default: 10).",
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip connecting to the database for a live count.",
    )
    args = parser.parse_args()

    poses = load_catalog(args.file)
    print(f"Catalog entries: {len(poses)}")

    if not args.skip_db:
        try:
            total_db = fetch_database_total()
            print(f"Database rows  : {total_db}")
        except Exception as exc:  # pragma: no cover
            print(f"Warning: unable to query database ({exc})")

    distribution = summarise_targets(poses)
    print("\nTarget coverage (top {}):".format(args.top))
    for body_part, count in distribution.most_common(args.top):
        print(f"- {body_part}: {count}")


if __name__ == "__main__":
    main()

