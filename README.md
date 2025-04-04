# Retroactive Priority Queue Visualization Tool

An interactive software tool for visualizing retroactive data structures—specifically a retroactive priority queue and its associated augmented binary search trees. This project is designed to help students better understand the theory behind retroactive operations by providing a practical, visual demonstration.

---

## Table of Contents

- [Overview](#overview)
- [How to Use the Software](#how-to-use-the-software)
  - [Installation](#installation)
  - [Graphic Mode](#graphic-mode)
  - [Prompt Mode](#prompt-mode)
- [Design Document](#design-document)
  - [Project Motivation and Objectives](#project-motivation-and-objectives)
  - [Key Features](#key-features)
  - [Design Decisions](#design-decisions)
  - [Challenges Faced and Solutions](#challenges-faced-and-solutions)
  - [Future Extensions](#future-extensions)

---

## Overview

This project implements an interactive visualization tool for retroactive data structures. The software supports both a graphical user interface (GUI) and a command-line prompt mode. Key functionalities include:

- Visualizing a retroactive priority queue using an AVL tree.
- Displaying augmented binary search trees (BBST) that capture historical operations of the **Augmented BBST**, showing the insertion events with the format `[time added, key, time deleted]`, and **Updates BBST** that racks every update (insertion and delete‑min) along with update values and subtree sums.
- Allowing retroactive modifications by letting users insert operations with a past timestamp.
- Real-time re‑evaluation and display of the internal state (events, active queue, and plot data).

---

## How to Use the Software

### Installation

1. Download the file RPQ_Vis.py or Clone the repository:
    git clone <repository-url>

2. Navigate to the project folder:
    cd "project-folder"

3. Install dependencies (if needed):
    pip install matplotlib
    pip install tkinter

### Graphic Mode

1. **Launching the Application:**
   - Run the application using Python. When prompted with:
     ```
     Choose mode (g for graphic, p for prompt):
     ```
     type `g` (or any input not starting with "p") to launch the graphical interface.

2. **User Interface Overview:**
   - **Top Panel:** Displays a matplotlib plot showing the key-time relationship of operations.
   - **Left Panel:** Contains an event log and control buttons:
     - **Add Insert:** Opens a pop-up to add an insertion event.
     - **Delete Min:** Triggers a delete-min operation.
     - **Query:** Issues a query to visualize the state.
     - **Add Random:** Inserts a random operation.
     - **Edit Event:** Opens a pop-up to edit an existing insertion.
     - **Clear All, Undo, Redo, Quit:** Standard controls.
   - **Right Panel (Tree Canvas):** Visualizes one of three binary tree views.
   - **Navigation (Below Content):**
     - Use the navigation buttons to switch among:
       - **PQ:** The AVL tree for the retroactive priority queue.
       - **Augmented:** The augmented BBST (displaying operations as `[time added, key, time deleted]`).
       - **Updates:** The BBST of update operations (with update values and subtree sums).
   - **Legend:** A label that updates based on the selected tree view.

3. **Interacting with the Tool:**
   - Use the provided buttons to add, delete, query, or edit events.
   - Navigate among tree views using the navigation buttons below the tree canvas.
   - The visualization updates automatically with each change.

### Prompt Mode

1. **Launching Prompt Mode:**
   - Run the application and type `p` when prompted:
     ```
     Choose mode (g for graphic, p for prompt):
     ```

2. **Input Format:**
   - Enter a complete dataset of commands in one line. Use the following format:
     ```
     Insert(0, 1), Insert(1, 12), Insert(3, 5), Insert(4, "delete-min"), Insert(5, 10), Insert(6, 8), Insert(7, "delete-min"), Insert(8, 9), Insert(9, "delete-min"), Insert(10, "delete-min"), Insert(11, 3), Insert(12, 6), Insert(13, "delete-min"), Insert(14, "delete-min"), Insert(15, 14), Insert(16, "query")
     ```
   - In each command:
     - The first argument is the time.
     - The second argument is the action: a number (for insertion), `"delete-min"`, or `"query"`.
   - **Note:** The final command must be a query to show the final state.

3. **Retroactive Edits:**
   - After processing the initial input, the program will ask:
     ```
     Do you want to add more commands (y/n)?
     ```
   - If you choose `y`, you can input additional commands (in the same format) that may have timestamps earlier than the current maximum. These retroactive commands will replace any existing event at the same time and be processed in chronological order.

4. **Output:**
   - After each batch of commands, the current state is printed:
     - **Events:** A sorted list of all operations.
     - **Active Queue:** List of active insertions.
     - **Plot Data:** A list of tuples in the format `(time added, key, time deleted)`.

---

## Design Document

### Project Motivation and Objectives

This project was created to connect abstract retroactive data structure principles with tangible visual illustrations. An interactive tool that can cease student difficulties with abstract data structure theories through visual demonstrations of retroactive operations in real time. This project works simultaneously to deliver educational assistance to students and exhibit theoretical transformations into interactive software through implementation.

### Key Features

- Having a **Dual Mode Operation** with a **Graphic Mode** that is an interactive GUI built with Tkinter and Matplotlib. And a **Prompt Mode** with a command-line interface for entering and testing operations.
- **Retroactive Operations** simulations that support inserting operations with past timestamps, thereby retroactively modifying the state.
- **Augmented Visualizations** while displays multiple tree views to illustrate different aspects of retroactive operations from **PQ Tree (AVL)**, **Augmented BBST** displaying insertion events in the format `(time added, key, time deleted)`, and **Updates BBST** tracking update operations with update values and subtree sums.
- **Interactive Editing** enabling users to perform add, delete, edit, and query operations in real time, with changes immediately reflected in the visualization.
- **Educational Impact** providing a tangible, interactive method to help students understand complex retroactive operations and the behavior of dynamic data structures.

### Design Decisions

- The **Programming Language and Libraries** chosen were Python due to its ease of use and the availability of robust libraries like Tkinter and Matplotlib.
- **Data Structures** selected were AVL tree to implement the priority queue due to its efficient balancing properties and the augmented BSTs to track historical changes and updates.
- About the **User Interface**, the GUI is divided into logical panels: a top panel for the plot, a left panel for the event log and controls, and a right panel for tree visualizations, and a separate navigation area allows users to switch between different tree views.
- The **Event Ordering** is based on the events stored in a list and re-sorted by timestamp upon re-evaluation to handle retroactive operations consistently.

### Challenges Faced and Solutions

- When **Handling Retroactive Operations** the retroactive commands needed to replace previous events with the same timestamp. This was achieved by checking for existing events and removing them before appending new ones.
- For the **Visualization Layout**, centering the tree visualization and aligning navigation controls required careful use of Tkinter layout managers and separate frames.
- To keep the **Maintaining State Consistency**, keeping the event log, active queue, and plot data in sync was challenging. Regular re-sorting and re-evaluation of events ensured consistency.

### Future Extensions

- Implement **Additional Data Structures** extending the tool to visualize other retroactive data structures (e.g., retroactive stacks or queues).
- **Enhance Interactivity** adding detailed on-screen annotations and tooltips to further explain changes in the data structure.
- Try a **Web-Based Version** developing a web interface to make the tool accessible to a wider audience.
- Add **Customization Options** allowing users to customize appearance settings such as colors, fonts, and layouts.
