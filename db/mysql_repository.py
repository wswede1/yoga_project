import mysql.connector
from db.repository import Repository
from model.yoga_pose import YogaPose
from typing import List

class MySQLRepository(Repository):

    def __init__(self):
        super().__init__()
        self.config = {
            'user': 'root',
            'password': 'strongpassword',
            'host': 'localhost',
            'port': 32000,
            'database': 'yoga'
        }
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()

    def get_poses_by_body_part(self, body_part: str) -> List[YogaPose]:
        query = """
        SELECT english_name, sanskrit_name, pose_type, target_body_parts, instructions 
        FROM yoga_poses 
        WHERE target_body_parts LIKE %s
        """
        self.cursor.execute(query, (f"%{body_part}%",))
        result = self.cursor.fetchall()
        return [YogaPose(**pose) for pose in result]

    def add_pose(self, pose: YogaPose) -> int:
        query = """
        INSERT INTO yoga_poses (english_name, sanskrit_name, pose_type, target_body_parts, instructions) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (pose.english_name, pose.sanskrit_name, pose.pose_type, pose.target_body_parts, pose.instructions))
        self.connection.commit()
        return self.cursor.lastrowid

    def load_pose(self, name: str) -> YogaPose:
        query = """
        SELECT english_name, sanskrit_name, pose_type, target_body_parts, instructions 
        FROM yoga_poses 
        WHERE english_name = %s
        """
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchone()
        if result:
            return YogaPose(**result)
        return None