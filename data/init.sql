CREATE DATABASE IF NOT EXISTS yoga;
USE yoga;

DROP TABLE IF EXISTS yoga_poses;

CREATE TABLE yoga_poses (
    id INT NOT NULL AUTO_INCREMENT,
    english_name VARCHAR(255) NOT NULL,
    sanskrit_name VARCHAR(255) DEFAULT '',
    pose_type VARCHAR(255) DEFAULT '',
    target_body_parts VARCHAR(255) DEFAULT '',
    instructions TEXT,
    PRIMARY KEY (id)
);

INSERT INTO yoga_poses (english_name, sanskrit_name, pose_type, target_body_parts, instructions)
VALUES
    (
        "Bharadvaja's Twist",
        "Bharadvajasana I",
        "Hip-Opening Yoga Poses, Seated Yoga Poses, Twist Yoga Poses",
        "Hips, Spine, Shoulders",
        "Sit on the floor with legs straight out. Bend your knees, swing them to the left, and twist your torso to the right with the support of your hands."
    ),
    (
        "Bound Angle Pose",
        "Baddha Konasana",
        "Forward Bend Yoga Poses, Hip-Opening Yoga Poses, Seated Yoga Poses",
        "Hips, Groin, Inner Thighs",
        "Sit tall, bring the soles of your feet together, interlace your fingers around your toes, and allow the knees to release toward the floor."
    ),
    (
        "Cat-Cow Stretch",
        "Marjaryasana-Bitilasana",
        "Warm-Up Yoga Poses, Backbend Yoga Poses",
        "Spine, Neck, Shoulders",
        "Start on all fours. Inhale to arch your back and lift your head (Cow), exhale to round your spine and tuck your chin (Cat). Flow with your breath."
    ),
    (
        "Downward-Facing Dog",
        "Adho Mukha Svanasana",
        "Inversion Yoga Poses, Standing Yoga Poses, Strength Yoga Poses",
        "Hamstrings, Shoulders, Back",
        "From tabletop, tuck your toes and lift your hips high. Press through your palms, lengthen your spine, and gently pedal the heels toward the mat."
    ),
    (
        "Thread the Needle",
        "Parsva Balasana",
        "Twist Yoga Poses, Restorative Yoga Poses",
        "Shoulders, Upper Back",
        "Start in tabletop. Slide your right arm underneath your left with your palm up, resting on your shoulder. Hold and breathe, then switch sides."
    );
