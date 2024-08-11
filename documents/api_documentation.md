# Yoga Pose API Documentation
## Description
The Yoga Pose API allows users to retrieve details about yoga poses based on a target body part. Users can query the API by specifying a body part, and the API will return relevant yoga poses, including their English and Sanskrit names, the pose types, the target body parts for the pose, and detailed instructions.

## Use Case
1. Find yoga poses by body part.
   2. input: Body part ("hips", "back", "shoulders")
   3. output: A list of poses and instructions that target the body part.

## Web Interface
You can access the Yoga Pose API through a web-based interface at 'http://127.0.0.1:5000' and enter a body part to retrieve relevant yoga poses. The response will display the pose information in JSON format.
For example, typing "hips" returns the following:
```
[
  {
    "english_name": "Bharadvaja's Twist",
    "sanskrit_name": "Bharadvajasana I",
    "pose_type": "Hip-Opening Yoga Poses, Seated Yoga Poses, Twist Yoga Poses",
    "target_body_parts": "Hips, Spine, Shoulders",
    "instructions": "Sit on the floor with legs straight out. Bend your knees, and swing your legs to the left. Twist your torso to the right, placing your left hand on the right knee and right hand behind you."
  },
  {
    "english_name": "Bound Angle Pose",
    "sanskrit_name": "Baddha Konasana",
    "pose_type": "Forward Bend Yoga Poses, Hip-Opening Yoga Poses, Seated Yoga Poses",
    "target_body_parts": "Hips, Groin, Inner Thighs",
    "instructions": "Sit with your legs extended. Bring the soles of your feet together and allow your knees to fall open. Hold your feet with your hands and gently press the knees towards the floor."
  }
]
```
The same results are displayed from a CURL request as well:
```
curl -X GET "http://127.0.0.1:5000/pose?body_part=Hips"
```

## Errors
If the body part is missing or there isn't a pose in the database utilizing that body part, there are two responses:
- Request without body part
```
  curl -X GET "http://127.0.0.1:5000/pose"
  ```
```
{
  "error": "Body part is required"
}
```
- No poses for requested body part
```
 curl -X GET "http://127.0.0.1:5000/pose?body_part=Neck"
```
``` 
{
  "message": "No poses found for this body part."
}
```
