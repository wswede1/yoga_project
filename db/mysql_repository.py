from typing import List, Optional

import mysql.connector

from db.repository import Repository
from model.yoga_pose import YogaPose


class MySQLRepository(Repository):
    """MySQL-backed implementation of the repository interface."""

    def __init__(self):
        super().__init__()
        self.config = {
            "user": "root",
            "password": "strongpassword",
            "host": "localhost",
            "port": 32000,
            "database": "yoga",
        }

    def _get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_poses_by_body_part(self, body_part: str) -> List[YogaPose]:
        query = """
            SELECT english_name, sanskrit_name, pose_type, target_body_parts, instructions
            FROM yoga_poses
            WHERE LOWER(target_body_parts) LIKE %s
        """
        like_pattern = f"%{body_part.lower()}%"
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query, (like_pattern,))
            result = cursor.fetchall()
            return [YogaPose(**pose) for pose in result]
        finally:
            cursor.close()
            connection.close()

    def add_pose(self, pose: YogaPose) -> int:
        query = """
            INSERT INTO yoga_poses (english_name, sanskrit_name, pose_type, target_body_parts, instructions)
            VALUES (%s, %s, %s, %s, %s)
        """
        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                query,
                (
                    pose.english_name,
                    pose.sanskrit_name,
                    pose.pose_type,
                    pose.target_body_parts,
                    pose.instructions,
                ),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            connection.close()

    def load_pose(self, name: str) -> Optional[YogaPose]:
        query = """
            SELECT english_name, sanskrit_name, pose_type, target_body_parts, instructions
            FROM yoga_poses
            WHERE english_name = %s
        """
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            if result:
                return YogaPose(**result)
            return None
        finally:
            cursor.close()
            connection.close()