import mysql.connector
from db.repository import Repository
from model.yoga_pose import YogaPose


class MySQLRepository(Repository):

    def __init__(self):
        super().__init__()
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': '3306',
            'database': 'yoga'
        }
        self.connection = mysql.connector.connect(**config)
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
            return YogaPose(id=result[0], name=result[1], instructions=result[2],
                            target_body_parts=[], category=None,
                            style=None, benefits=[])
        return None

    def add_sequence(self, sequence):
        # add a sequence
        pass

    def load_sequence(self, name: str):
        # load a sequence
        pass
