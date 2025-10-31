# 🧰 Task1 — The intersector

A command-line tool for computing, analyzing, and visualizing the intersection between a 3D shape (e.g., imported from a STEP file) and a geometric plane defined by a point and a normal vector.

# 🚀 Installation and Usage

## ✅ Prerequisites
- Conda or Mamba installed (Anaconda, Miniconda, or Miniforge)
- Python ≥ 3.11
- pip

## 📦 Installation

Download the file intersector-0.1.0-py3-none-any.whl (or a newer version).

Follow the steps:

```bash
# 1. Create environment
conda create -n intersector python=3.11
conda activate intersector

# 2. Install pythonocc-core from conda-forge
conda install -c conda-forge pythonocc-core

# 3. Install your package wheel
pip install intersector-1.0.0-py3-none-any.whl
```
Once installed, the command-line tool intersector will be available in your terminal.

## ⚙️ Command-Line Usage
The main entry point is the intersect command, which computes and visualizes the intersection between a STEP shape and a plane.
```bash
 intersector intersect --in-step <STEP_FILE> --in-plane <POINT:VECTOR>
```
Example:
```bash
 intersector intersect --in-step ./step_files/sample.stp --in-plane 0,0,50:0,0,1
```

This command will:
- Load the STEP file sample.stp
- Define a plane passing through the point (0, 0, 50) with normal vector (0, 0, 1)
- Compute the intersection between the plane and the shape
- Display the shape, and the intersection curve in a 3D viewer window

## 🧩 Plane Syntax

Planes are given using the format:
```bash
X,Y,Z:NX,NY,NZ
```
where:

- (X, Y, Z) → a point on the plane
- (NX, NY, NZ) → the normal direction of the plane

## ✅ Example:
```bash
0,0,100:0,0,1
```
This defines a plane parallel to the XY plane at Z = 100.

## 🖼️ Visualization

If there is an intersection, the viewer will show:
- The original shape (gray)
- The intersection curve (red)

Use your mouse to zoom, rotate, or pan around the scene.

## 🧹 Uninstallation

To uninstall the package:
```bash
pip uninstall intersector
```