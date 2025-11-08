from dataclasses import dataclass
from typing import Dict, List


def _split_csv(value: str) -> List[str]:
    if not value:
        return []
    return [segment.strip() for segment in value.split(",") if segment.strip()]


@dataclass
class YogaPose:
    """Container object describing a single yoga pose."""

    english_name: str
    sanskrit_name: str
    pose_type: str
    target_body_parts: str
    instructions: str

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serialisable representation."""
        return {
            "english_name": self.english_name,
            "sanskrit_name": self.sanskrit_name,
            "pose_type": _split_csv(self.pose_type),
            "target_body_parts": _split_csv(self.target_body_parts),
            "instructions": self.instructions,
        }
