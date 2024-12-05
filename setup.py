#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import webbrowser
from pathlib import Path

def get_git_path():
    """Get platform-specific Git path."""
    if platform.system() == "Windows":
        return r"C:\Program Files\Git\bin"
    return "/usr/bin"  # Default for Unix-like systems

def check_git():
    """Check if Git is installed and accessible."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("Git is in path.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Git not found in PATH")
        if platform.system() == "Windows":
            os.environ["PATH"] += os.pathsep + get_git_path()
        return False

def update_repository():
    """Update Git repository if exists."""
    if Path('.git').exists():
        print("Updating repository...")
        try:
            subprocess.run(["git", "pull"], check=True)
            print("Repository updated successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to update repository. Error code: {e.returncode}")
    else:
        print("No .git directory found. Skipping git pull.")

def get_python_path():
    """Get virtual environment Python path."""
    base_dir = Path(__file__).parent
    if platform.system() == "Windows":
        return base_dir / "venv" / "Scripts" / "python.exe"
    return base_dir / "venv" / "bin" / "python"

def setup_virtual_environment():
    """Create and setup virtual environment with requirements."""
    venv_path = Path("venv")
    python_executable = "python3" if platform.system() != "Windows" else "python"
    pip_cmd = "pip3" if platform.system() != "Windows" else "pip"
    
    # Create venv if it doesn't exist
    if not venv_path.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run([python_executable, "-m", "venv", "venv"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create virtual environment: {e}")
            sys.exit(1)

    # Determine venv activation script path
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        activate_cmd = str(activate_script)
    else:
        activate_script = venv_path / "bin" / "activate"
        activate_cmd = f"source {activate_script}"

    # Install requirements
    if Path("requirements.txt").exists():
        print("Installing requirements...")
        venv_pip = str(venv_path / "bin" / pip_cmd)
        if platform.system() == "Windows":
            venv_pip = str(venv_path / "Scripts" / "pip.exe")
        
        try:
            subprocess.run([
                venv_pip, "install", "-r", "requirements.txt"
            ], check=True)
            print("Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e}")
            sys.exit(1)
    else:
        print("No requirements.txt found")

def run_django_server():
    """Start Django development server."""
    python_path = get_python_path()

    print("Running Django application...")
    try:
        # Start Django server
        subprocess.run([
            str(python_path),
            "manage.py",
            "runserver"
        ], check=True)

        # Open browser
        webbrowser.open('http://127.0.0.1:8000')
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Django server. Error: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped by user")

def main():
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Setup steps
    check_git()
    update_repository()
    setup_virtual_environment()
    run_django_server()

if __name__ == "__main__":
    main()