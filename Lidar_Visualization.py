import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb  # type: ignore # Modern UI styles
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation
from sklearn.cluster import DBSCAN

# Global directory for dataset
data_dir = ""

def select_data_directory():
    """Allows user to change the dataset directory and updates available frames."""
    global data_dir
    new_dir = filedialog.askdirectory(title="Select Cluster File Directory")
    if new_dir:
        data_dir = new_dir
        update_frame_options()
        count_cluster_files()

def get_available_frames():
    """Gets sorted and continuous frame numbers from the dataset directory."""
    if not data_dir:
        return []
    
    files = sorted([f for f in os.listdir(data_dir) if f.startswith("clusterR") and f.endswith(".csv")])
    frames = sorted([int(f[8:-4]) for f in files])

    # Ensure frames are continuous (no missing numbers)
    if frames and list(range(frames[0], frames[-1] + 1)) == frames:
        return frames
    else:
        messagebox.showwarning("Frame Continuity Issue", "Detected missing frames! Ensure the dataset contains continuous frames.")
        return []

def update_frame_options():
    """Updates start and end frame dropdowns based on available frames."""
    frames = get_available_frames()
    start_frame_dropdown["values"] = frames
    end_frame_dropdown["values"] = frames
    if frames:
        start_frame_dropdown.current(0)
        end_frame_dropdown.current(len(frames) - 1)

def count_cluster_files():
    """Counts and displays the number of valid cluster files in the directory."""
    frames = get_available_frames()
    label_count.config(text=f"Cluster Files Count: {len(frames)}")

def apply_noise_filter(df):
    """Applies noise reduction by removing extreme outliers."""
    if df.empty:
        return df
    
    mean_x, mean_y, mean_z = df.iloc[:,7].mean(), df.iloc[:,8].mean(), df.iloc[:,9].mean()
    std_x, std_y, std_z = df.iloc[:,7].std(), df.iloc[:,8].std(), df.iloc[:,9].std()
    
    threshold = 2.5
    return df[
        (abs(df.iloc[:,7] - mean_x) < threshold * std_x) &
        (abs(df.iloc[:,8] - mean_y) < threshold * std_y) &
        (abs(df.iloc[:,9] - mean_z) < threshold * std_z)
    ]

def segment_objects(df):
    """Clusters LiDAR points into objects using DBSCAN."""
    if df.empty:
        return df
    
    clustering = DBSCAN(eps=1.5, min_samples=5).fit(df.iloc[:, 7:10].values)
    df['Cluster'] = clustering.labels_
    return df

def visualize_single_frame():
    """Visualizes a single frame in 3D with fixed colormap and axis limits."""
    file_path = filedialog.askopenfilename(initialdir=data_dir, title="Select a cluster file",
                                           filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return

    df = pd.read_csv(file_path)
    df = apply_noise_filter(df)
    df = segment_objects(df)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df.iloc[:,7], df.iloc[:,8], df.iloc[:,9], c=df['Cluster'], cmap='viridis', s=2)

    plt.colorbar(scatter)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-10, 10)
    plt.title(f"Visualization of {os.path.basename(file_path)} (Filtered & Segmented)")
    plt.show()

def visualize_all_frames():
    """Visualizes all cluster frames in 3D with fixed colormap and axis limits."""
    files = get_available_frames()
    if not files:
        messagebox.showerror("Error", "No cluster files found.")
        return

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for frame in files:
        file_path = os.path.join(data_dir, f"clusterR{frame}.csv")
        df = pd.read_csv(file_path)
        df = apply_noise_filter(df)
        df = segment_objects(df)
        ax.scatter(df.iloc[:,7], df.iloc[:,8], df.iloc[:,9], c=df['Cluster'], cmap='viridis', s=2)

    plt.colorbar(ax.collections[0])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_zlim(-10, 10)
    plt.title("Visualization of All Cluster Frames (Filtered & Segmented)")
    plt.show()

def animate_frames():
    """Animates the visualization for selected continuous frames."""
    start_frame = int(start_frame_dropdown.get())
    end_frame = int(end_frame_dropdown.get())

    if start_frame >= end_frame:
        messagebox.showerror("Invalid Input", "Start frame must be less than the end frame!")
        return

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def update(frame):
        ax.clear()
        file_path = os.path.join(data_dir, f"clusterR{frame}.csv")
        if not os.path.exists(file_path):
            return
        df = pd.read_csv(file_path)
        df = apply_noise_filter(df)
        df = segment_objects(df)
        scatter = ax.scatter(df.iloc[:,7], df.iloc[:,8], df.iloc[:,9], c=df['Cluster'], cmap='viridis', s=2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        ax.set_zlim(-10, 10)
        ax.set_title(f"Frame {frame} (Filtered & Segmented)")

    ani = animation.FuncAnimation(fig, update, frames=range(start_frame, end_frame + 1), interval=500)
    plt.show()

# GUI Setup
root = tb.Window(themename="superhero")  # Dark mode friendly UI
root.title("LiDAR Data Visualization")
root.geometry("750x550")

frame = tb.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

button_width = 30
dropdown_width = 25

tb.Button(frame, text="📁 Select Data Directory", bootstyle="primary", command=select_data_directory, width=button_width).pack(pady=5)
tb.Button(frame, text="📊 Count Cluster Files", bootstyle="info", command=count_cluster_files, width=button_width).pack(pady=5)
tb.Button(frame, text="🔍 Visualize Single Frame", bootstyle="success", command=visualize_single_frame, width=button_width).pack(pady=5)
tb.Button(frame, text="📡 Visualize All Frames", bootstyle="warning", command=visualize_all_frames, width=button_width).pack(pady=5)

tb.Label(frame, text="Select Start Frame:", font=("Arial", 12)).pack()
start_frame_dropdown = tb.Combobox(frame, state="readonly", width=dropdown_width)
start_frame_dropdown.pack(pady=5)

tb.Label(frame, text="Select End Frame:", font=("Arial", 12)).pack()
end_frame_dropdown = tb.Combobox(frame, state="readonly", width=dropdown_width)
end_frame_dropdown.pack(pady=5)

tb.Button(frame, text="▶ Animate Frames", bootstyle="danger", command=animate_frames, width=button_width).pack(pady=10)

label_count = tb.Label(frame, text="Cluster Files Count: 0", font=("Arial", 12, "bold"))
label_count.pack(pady=10)

root.mainloop()
