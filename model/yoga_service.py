from typing import List, Dict, Any
from db.repository import Repository
from model.yoga_pose import YogaPose
from model.pose_sequence import PoseSequence
from model.enums import BodyPart
from model.llm_client import get_llm_client, LLMClientError


class YogaService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_pose(self, pose: YogaPose) -> YogaPose:
        return self.repository.add_pose(pose)

    def get_pose(self, name: str) -> YogaPose:
        return self.repository.load_pose(name)

    def get_poses_by_body_part(self, body_part: str) -> list:
        poses = self.repository.get_poses_by_body_part(body_part)
        return [pose.to_dict() for pose in poses]

    def generate_routine(
        self,
        body_parts: List[str],
        duration_minutes: int,
        difficulty: str
    ) -> Dict[str, Any]:
        """
        Generate a yoga routine using the LLM client.

        Args:
            body_parts: List of body parts to focus on
            duration_minutes: Total duration in minutes
            difficulty: Difficulty level (beginner, intermediate, advanced)

        Returns:
            Dict with 'segments' and 'total_seconds'

        Raises:
            LLMClientError: If routine generation fails
        """
        # Validate inputs
        if not body_parts:
            body_parts = ["full body"]
        
        if duration_minutes < 1:
            duration_minutes = 5
        elif duration_minutes > 120:
            duration_minutes = 120

        valid_difficulties = ["beginner", "intermediate", "advanced"]
        if difficulty.lower() not in valid_difficulties:
            difficulty = "beginner"
        else:
            difficulty = difficulty.lower()

        client = get_llm_client()
        return client.generate_routine(body_parts, duration_minutes, difficulty)
