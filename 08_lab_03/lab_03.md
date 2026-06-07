# Lab 3: TF Tree & Robot Localization

> **Before You Start:**
> - Add these dependencies to `package.xml`: `rclpy`, `sensor_msgs`, `nav_msgs`, `tf2_ros`, `robot_localization`
> - Mark Python scripts as executable and install them with `install(PROGRAMS ...)` in `CMakeLists.txt`
> - Install `config/` and `launch/` directories with `install(DIRECTORY ...)` in `CMakeLists.txt`

---

## Objective

Set up a complete **TF (Transform) tree** for the mobile robot by:
1. Defining **static transforms** for all sensor frames
2. Running the **`robot_localization`** EKF node for odometry
3. Creating a custom **`orientation_analysis`** node to compare sensor orientations

---

## Robot Specifications

![Robot Diagram](robot_lab03.png)

| Property | Value |
|---|---|
| Size | Width = 30 cm, Length = 60 cm |
| `base_link` | Center of the rear wheels, 5 cm above ground |
| `base_footprint` | Ground projection of `base_link` (directly below it) |
| `imu_link` | 5 cm from the front edge, 15 cm above ground |
| `gps_link` | Center of the robot (X), 30 cm above ground |

### Ultrasonic Sensor Positions

Corner sensors are oriented at **±45°** or **±135°** to face diagonally outward.

| Frame | Position | Yaw |
|---|---|---|
| `ultrasonic1_link` | Front-Left corner | +45° |
| `ultrasonic2_link` | Front-Center | 0° |
| `ultrasonic3_link` | Front-Right corner | -45° |
| `ultrasonic4_link` | Rear-Left corner | +135° |
| `ultrasonic5_link` | Rear-Center | 180° |
| `ultrasonic6_link` | Rear-Right corner | -135° |

---

## TF Tree

The expected transform tree for this lab is:

```
odom
└── base_footprint          ← published by robot_localization EKF node
    └── base_link           ← static transform (z = 0.05 m)
        ├── imu_link        ← static transform
        ├── gps_link        ← static transform
        ├── ultrasonic1_link ← static transform
        ├── ultrasonic2_link ← static transform
        ├── ultrasonic3_link ← static transform
        ├── ultrasonic4_link ← static transform
        ├── ultrasonic5_link ← static transform
        └── ultrasonic6_link ← static transform
```

---

## Input Data: Bag File

All sensor topics come from the **`sample_bag_for_localization`** bag: [Google Drive Link](https://drive.google.com/file/d/1XH8KIQFJvyxsSFaHu7aGLWY3Y4idwF46/view?usp=sharing)

The bag topics are named with a `/bag` suffix — you will need to **remap** them :

| Bag Topic | Remapped To |
|---|---|
| `/imu/data/bag` | `/imu/data` |
| `/odometry/wheel/bag` | `/odometry/wheel` |
| `/odometry/gps/bag` | `/odometry/gps` |

> **Important:** This bag was recorded with the **`sensor_data`** QoS profile (Best Effort reliability). Any node subscribing to these topics **must** use a compatible QoS profile, otherwise no messages will be received.

---

## Requirements

### 1. Static Transform Publishers

Using the robot specifications above, define all the necessary static transforms in your launch file. You should compute the correct x, y, z translation and yaw values yourself based on the robot dimensions.

The following transforms are required:

- `base_footprint` → `base_link`
- `base_link` → `imu_link`
- `base_link` → `gps_link`
- `base_link` → `ultrasonic1_link` through `ultrasonic6_link` (with correct yaw for corner sensors)

---

### 2. robot_localization EKF Node

Configure the EKF node (`config/ekf.yaml`) with:

| Setting | Value |
|---|---|
| Input: `/odometry/wheel` | Fuse **linear velocity x** and **angular velocity z** |
| Input: `/imu/data` | Fuse **angular velocity z** only |
| `base_link_frame` | `base_footprint` |
| `world_frame` | `odom` |
| `publish_tf` | `true` → publishes `odom → base_footprint` |
| Output topic | `/odometry/local` |


---

### 3. Orientation Analysis Node (`orientation_analysis`)

Create a Python node that:
- Subscribes to `/imu/data` using `qos_profile_sensor_data`
- Subscribes to `/odometry/local` using `qos_profile_sensor_data`
- Periodically logs and compares the **yaw** orientation from each source

---

### 4. Launch File (`robot_tf_localization.launch.py`)

The launch file must start **all** of the following:
- All static transform publishers
- The `robot_localization` EKF node (with `ekf.yaml` loaded)
- The `orientation_analysis` node
- RViz with the `robot_tf.rviz` configuration


---

### 5. RViz Configuration (`config/robot_tf.rviz`)

| Setting | Value |
|---|---|
| Fixed Frame | `odom` |
| TF display | All frames enabled |
| Odometry display | Topic: `/odometry/local`, Style: Arrow |

---

## Deliverables

Submit a complete ROS 2 package named **`robot_tf_localization`** containing:

```
robot_tf_localization/
├── package.xml
├── CMakeLists.txt
├── README.md
├── config/
│   ├── ekf.yaml
│   └── robot_tf.rviz
├── launch/
│   └── robot_tf_localization.launch.py
└── scripts/
    └── orientation_analysis.py
```

The `README.md` must explain:
- How to build and run the launch file
- The TF tree structure
- Notes about QoS compatibility with the recorded bag

---

## Optional Extension: GPS-Aided Localization (map → odom)


Add a second EKF node that fuses GPS data to produce the global `map → odom` transform.

### Configuration

Modify the ekf yaml file or create a new one with:

| Setting | Value |
|---|---|
| Input: `/odometry/wheel` | Fuse **twist linear x** and **angular velocity z** (same as local EKF) |
| Input: `/imu/data` | Fuse **angular velocity z** only (same as local EKF) |
| Input: `/odometry/gps` | Fuse **X, Y position** only |
| `world_frame` | `map` |
| `odom_frame` | `odom` |
| `base_link_frame` | `base_footprint` |
| `publish_tf` | `true` → publishes `map → odom` |
| Output topic | `/odometry/global` |

### Updated TF Tree (with GPS EKF)

```
map
└── odom                    ← published by GPS EKF node
    └── base_footprint      ← published by wheel/IMU EKF node
        └── base_link       ← static transform
            └── ...
```

### Notes
- In RViz, change the Fixed Frame to `map` to see the global trajectory.
