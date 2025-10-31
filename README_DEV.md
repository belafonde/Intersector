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
    ├── pyproject.toml                     # Poetry project configuration (dependencies, tools)
    ├── environment.yml                    # Conda environment definition
    ├── README_DEV.md                      # Developer documentation
    ├── README.md                          # End-user documentation
    ├── src/   
    │   └── intersector/   
    │           ├── __init__.py   
    │           ├── cli.py                 # CLI entry points (e.g., "intersector intersect")
    │           ├── operations/            # Core computational modules
    │           │   ├── __init__.py   
    │           │   ├── intersect.py       # Intersection logic implementation
    │           │   ├── check.py           # Intersection validation helpers
    │           ├── utils/                 # Supporting utilities
    │           │   ├── __init__.py   
    │           │   ├── parsing.py         # Input parsing (plane, arguments)
    │           │   ├── visualize.py       # Visualization helpers
    │           │   ├── logging.py         # Logging setup and configuration
    │           └── tests/                 # Unit tests
    │               ├── __init__.py
    │               ├── test_intersect.py
    │               ├── test_visualize.py
    │               ├── test_check.py
    │               └── test_parsing.py
    └── step_files/                        # Sample STEP files for testing
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
## ▶️ Usage

### Run the CLI application with:
```bash
poetry run intersector --help
```

### Example command:
```bash
poetry run intersector intersect --in-step <STEP_FILE> --in-plane <POINT:VECTOR>
```
### Example:
```bash
 poetry run intersector intersect --in-step ./step_files/sample.stp --in-plane 0,0,50:0,0,1
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

## 🧪 Development Workflow

### Format code automatically
```bash
poetry run black src/
```

### Run code style and docstring checks
```bash
poetry run ruff check .
```

### Run tests
```bash
poetry run pytest
```

## 🧰 Dependency Management

### Add a new dependency
```bash
poetry add somepackage
```

### Add a development-only dependency
```bash
poetry add --group dev black flake8 pytest
```

### Update dependencies
```bash
poetry update
```

## 📦 Packaging and Distribution

### Build the package:
```bash
poetry build
```

## 🧠 Standards and Conventions

| PEP                                              | Description                  |
| ------------------------------------------------ | ---------------------------- |
| [PEP 257](https://peps.python.org/pep-0257/)     | Docstring conventions        |
| [PEP 420](https://peps.python.org/pep-0420/)     | Namespace package support    |
| [PEP 440](https://peps.python.org/pep-0440/)     | Versioning scheme            |
| [PEP 517/518](https://peps.python.org/pep-0517/) | Build system interface       |
| [PEP 621](https://peps.python.org/pep-0621/)     | Metadata in `pyproject.toml` |

## 🪪 License
MIT License © 2025 Yannis Arapakis

## 🙌 Acknowledgements
- OpenCascade
- Click
- Rich
- Poetry
- Conda-Forge