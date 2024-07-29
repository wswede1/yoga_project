CREATE DATABASE yoga;
USE yoga;

CREATE TABLE IF NOT EXISTS yoga_poses (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    instructions TEXT,
    PRIMARY KEY (id)
);

INSERT INTO yoga_poses (name, instructions) VALUES ('Test Pose', 'Test instructions');
