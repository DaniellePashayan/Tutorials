# Docker Academy

This project is a self-contained, local-only interactive tutorial designed for Windows laptops. Since your work computers cannot use containerization or WSL, it uses Python's standard library and browser HTML/CSS/JavaScript to mimic behaviors and does **not** install or run WSL, Linux, Docker, or a virtual machine.

## Start
1. Open the folder in VS Code.
2. Run `start-tutorial.bat`, or open a VS Code terminal and run:
   ```powershell
   python start_tutorial.py
   ```
3. The tutorial opens at http://127.0.0.1:8765.
4. Press Ctrl+C in the terminal to stop it.

The server binds only to 127.0.0.1 (localhost), so it is not exposed to other computers on your network.

## Important training boundary
This module teaches concepts. It does not emulate a complete operating system, install WSL, create VMs, or execute Linux/Docker commands. The diagrams and activities are explanatory simulations.