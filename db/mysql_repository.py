import mysql.connector
from db.repository import Repository
from model.yoga_pose import YogaPose
from model.pose_sequence import PoseSequence
from model.enums import BodyPart

class MySQLRepository(Repository):
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': '3306',
            'database': 'yoga'
        }
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()

    def add_pose(self, pose: YogaPose):
        sql = "INSERT INTO yoga_poses (name, instructions) VALUES (%s, %s)"
        values = (pose.name, pose.instructions)
        self.cursor.execute(sql, values)
        self.connection.commit()
        pose.id = self.cursor.lastrowid
        return pose

    def load_pose(self, name: str) -> YogaPose:
        self.connection.consume_results()  # Ensure all previous results are handled
        sql = "SELECT id, name, instructions FROM yoga_poses WHERE name = %s"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        if result:
            return YogaPose(id=result[0], name=result[1], instructions=result[2])
        return None

    def get_poses_by_body_part(self, body_part: str) -> list[YogaPose]:
        self.connection.consume_results()  # Ensure all previous results are handled
        sql = (
            "SELECT p.id, p.name, p.instructions "
            "FROM yoga_poses p "
            "JOIN pose_body_parts pb ON p.id = pb.pose_id "
            "WHERE pb.body_part = %s"
        )
        self.cursor.execute(sql, (body_part,))
        results = self.cursor.fetchall()
        return [YogaPose(id=row[0], name=row[1], instructions=row[2]) for row in results]

    def add_sequence(self, sequence: PoseSequence):
        sql = "INSERT INTO yoga_sequences (name, sequence_type) VALUES (%s, %s)"
        values = (sequence.name, sequence.sequence_type.value)
        self.cursor.execute(sql, values)
        self.connection.commit()
        sequence_id = self.cursor.lastrowid

        for pose in sequence.poses:
            sql = "INSERT INTO sequence_poses (sequence_id, pose_id) VALUES (%s, %s)"
            self.cursor.execute(sql, (sequence_id, pose.id))
        self.connection.commit()
        return sequence

    def load_sequence(self, name: str) -> PoseSequence:
        self.connection.consume_results()  # Ensure all previous results are handled
        sql = (
            "SELECT s.id, s.name, s.sequence_type, p.id, p.name, p.instructions "
            "FROM yoga_sequences s "
            "JOIN sequence_poses sp ON s.id = sp.sequence_id "
            "JOIN yoga_poses p ON sp.pose_id = p.id "
            "WHERE s.name = %s"
        )
        self.cursor.execute(sql, (name,))
        results = self.cursor.fetchall()

        if results:
            poses = [YogaPose(id=row[3], name=row[4], instructions=row[5]) for row in results]
            sequence_type = results[0][2]
            return PoseSequence(name=results[0][1], poses=poses, sequence_type=sequence_type)
        return None
