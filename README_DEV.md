# 🧰 Task1 — The intersector

A command-line tool for computing, analyzing, and visualizing the intersection between a 3D shape (e.g., imported from a STEP file) and a geometric plane defined by a point and a normal vector **OpenCascade**.  
Built with **Python 3.11**, **Poetry**, and **Conda**, following modern Python packaging standards (PEP 257, 420, 440, 517/518, 621).

---

## 🚀 Features

- 🧱 Compute, analyze, and visualize 3D shapes using [OpenCascade](https://www.opencascade.com/)
- 🖥️ Beautiful terminal UI with [Rich](https://rich.readthedocs.io/)
- 🧩 Easy CLI interface with [Click](https://click.palletsprojects.com/)
- 🧪 Fully reproducible hybrid environment (Conda + Poetry)
- 📐 Style & docstring checks following [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/)

---

## 🧩 Project Structure
```
intersector/
      ├── pyproject.toml              # Poetry project configuration (dependencies, tools)
      ├── environment.yml             # Conda environment definition
      ├── README_DEV.md               # Developer documentation
      ├── README.md                   # End-user documentation
      └── src/
           └── intersector/
                    ├── __init__.py
                    └── cli.py        # CLI entry points (e.g., "task1 intersect")
```
---
## 🧰 Prerequisites

Before setting up the development environment, make sure you have:

- **Conda (Miniconda or Anaconda)**
  Used to create and manage isolated environments and to install CAD dependencies like pythonocc-core.    
  [Install Miniconda](https://docs.conda.io/en/latest/miniconda.html).

- **Git**  
  For version control and cloning the repository.

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone <repo> #TODO add repo later
cd intersector
```

### 2️⃣ Create and activate the Conda environment
```bash
conda env create -f environment.yml
conda activate intersectorenv
```

### 3️⃣ Configure Poetry to use Conda’s environment
```bash
poetry config virtualenvs.create false
```

### 4️⃣ Install dependencies with Poetry
```bash
poetry install
```
