# LiDAR Data Visualization & Clustering


## 📌 Overview

This project provides an intuitive and interactive graphical user interface (GUI) for visualizing and analyzing LiDAR point cloud data. The application allows users to:

✅ Load and manage LiDAR dataset files  
✅ Filter noise from raw data  
✅ Cluster objects using DBSCAN (Density-Based Spatial Clustering of Applications with Noise)  
✅ Visualize individual and multiple frames in 3D  
✅ Animate frames for dynamic data representation  

---

## 🎯 Features

- 🖥 **User-Friendly GUI**: Built with `tkinter` and `ttkbootstrap` for a modern, clean look.

- 📁 **Data Selection**: Allows users to select a directory containing cluster files.
- 🛠 **Noise Filtering**: Removes outliers using standard deviation-based filtering.
- 📌 **Clustering with DBSCAN**: Segments point clouds into meaningful clusters.
- 🎥 **3D Visualization**: Displays LiDAR frames with adjustable axes and color mapping.
- 🔄 **Animation Support**: Dynamically visualizes continuous LiDAR frames in sequence.
- 🌙 **Dark Mode Friendly**: Enhanced user experience with a superhero-themed UI.

---

## 🚀 Installation & Requirements

### 🛠 Prerequisites

Ensure you have Python installed (preferably Python 3.8+). Install dependencies using:

```bash
pip install pandas numpy matplotlib scikit-learn ttkbootstrap
```

---

## 🔧 Usage

### 1️⃣ Running the Application

Open a terminal and navigate to the project folder:

```bash
cd /path/to/your/project
```

Execute the following command:

```bash
python Lidar_Visualization.py
```

### 2️⃣ Selecting Data Directory

Click **📁 Select Data Directory** to choose the folder containing LiDAR cluster files (`clusterR*.csv`).

### 3️⃣ Counting Cluster Files

Click **📊 Count Cluster Files** to get the total number of valid cluster files.

### 4️⃣ Visualizing a Single Frame

Click **🔍 Visualize Single Frame**, select a `.csv` file, and a 3D scatter plot will appear with clustered objects.

### 5️⃣ Visualizing All Frames

Click **📡 Visualize All Frames** to render all cluster files in one 3D space.

### 6️⃣ Animating Frames

- Select **Start** and **End** frames from the dropdowns.
- Click **▶ Animate Frames** to create a 3D animation of point cloud evolution.

---

## 🔬 How It Works

### 🧹 Noise Filtering

- Uses a **2.5 standard deviation threshold** to remove outliers.
- Ensures cleaner data input for clustering.

### 🔍 Clustering Algorithm

- Implements **DBSCAN**, which groups nearby points and labels noise.
- Points are clustered based on spatial proximity (**X, Y, Z** coordinates).

### 📡 3D Visualization

- Uses `matplotlib` and `mpl_toolkits.mplot3d` for rendering.
- **Color mapping** differentiates clusters.
- Axes are set within a reasonable range to maintain clarity.

---

## 📂 File Structure

```
📁 Project Directory
 ├── Lidar_Visualization.py  # Main application script
 ├── clusterR*.csv  # LiDAR cluster data files (to be selected by the user)
```

---

## 🔮 Future Enhancements

🚀 **Real-time LiDAR Data Processing**  
⚙️ **Customizable Clustering Parameters**  
🤖 **Integration with ROS (Robot Operating System)**  
🔍 **More Advanced Noise Filtering Techniques**  
📊 **User-defined DBSCAN Parameters for Better Customization**  

---


## ✨ Author
**Md A Rahman**

---

## 📜 License

This project is licensed under the TransTech Lab License.

---

## 💬 Contact

For any questions or issues, feel free to open an issue or reach out!

📧 Email: ara02434@ttu.edu  
  
