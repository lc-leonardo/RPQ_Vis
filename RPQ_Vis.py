import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import re


# AVL Tree (for retroactive PQ)

class Node:
    def __init__(self, key, timestamp):
        self.key = key
        self.timestamp = timestamp
        self.left = None
        self.right = None
        self.height = 1  # Track the height for balancing

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, timestamp):
        self.root = self._insert(self.root, key, timestamp)

    def _insert(self, node, key, timestamp):
        if not node:
            return Node(key, timestamp)
        if key < node.key:
            node.left = self._insert(node.left, key, timestamp)
        else:
            node.right = self._insert(node.right, key, timestamp)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.timestamp = temp.timestamp
            node.right = self._delete(node.right, temp.key)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _balance(self, node):
        balance = self._get_balance(node)
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def inorder_traversal(self, current, result):
        if current:
            self.inorder_traversal(current.left, result)
            result.append((current.key, current.timestamp))
            self.inorder_traversal(current.right, result)
        return result


# Augmented Tree Node (for Augmented BBST view)

class AugTreeNode:
    def __init__(self, event=None):
        self.event = event  # (time_added, key, time_deleted)
        self.left = None
        self.right = None
        self.aug = float('-inf')  # Augmented value


# Update Tree Node (for the Updates BBST view)

class UpdateNode:
    def __init__(self, event=None):
        self.event = event  # (timestamp, type, value)
        self.left = None
        self.right = None
        self.val = 0      # Update value
        self.sum = 0      # Subtree sum


# Retroactive Priority Queue & Visualization

class RetroactivePriorityQueue:
    def __init__(self, root):
        self.events = []         # (timestamp, type, value)
        self.queue = []          # Active insertions: (timestamp, value)
        # Plot data stored as (time_added, key, time_deleted)
        self.plot_data = []
        self.query_lines = []    # (time, max_key, bridge_status)
        self.time = 0
        self.undo_stack = []
        self.redo_stack = []
        self.bst = AVLTree()
        self.current_tree_view = "PQ"  # "PQ", "Augmented", "Updates"
        if root is not None:
            self.__init_gui(root)
        self.update_display()

    def get_update_value(self, event):
        timestamp, etype, val = event
        if etype == "add":
            if (timestamp, val) in self.queue:
                return 0
            else:
                return 1
        elif etype == "delete-min":
            return -1
        else:
            # For any other event type (like "query"), return 0.
            return 0


    def __init_gui(self, root):
        root.title("Retroactive Priority Queue Visualization")
        root.geometry("1200x800")
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.figure, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=self.top_frame)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.left_frame = tk.Frame(self.content_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.event_log = tk.Listbox(self.left_frame, height=20, width=40)
        self.event_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        button_frame = tk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X)
        tk.Button(button_frame, text="Add Insert", command=self.add_event).grid(row=0, column=0, sticky="ew")
        tk.Button(button_frame, text="Delete Min", command=self.delete_min).grid(row=0, column=1, sticky="ew")
        tk.Button(button_frame, text="Query", command=self.query).grid(row=0, column=2, sticky="ew")
        tk.Button(button_frame, text="Add Random", command=self.insert_random).grid(row=1, column=0, sticky="ew")
        tk.Button(button_frame, text="Edit Event", command=self.edit_event).grid(row=1, column=1, sticky="ew")
        tk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=1, column=2, sticky="ew")
        tk.Button(button_frame, text="Undo", command=self.undo).grid(row=2, column=0, sticky="ew")
        tk.Button(button_frame, text="Redo", command=self.redo).grid(row=2, column=1, sticky="ew")
        tk.Button(button_frame, text="Quit", command=root.quit).grid(row=2, column=2, sticky="ew")
        self.tree_frame = tk.Frame(self.content_frame)
        self.tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tree_canvas = tk.Canvas(self.tree_frame, width=800, height=400, bg="white")
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.nav_buttons_frame = tk.Frame(self.nav_frame)
        self.nav_buttons_frame.pack(side=tk.TOP, fill=tk.X)
        for view in ["PQ", "Augmented", "Updates"]:
            btn = tk.Button(self.nav_buttons_frame, text=view, command=lambda v=view: self.set_tree_view(v))
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.legend_frame = tk.Frame(self.nav_frame)
        self.legend_frame.pack(side=tk.TOP, fill=tk.X)
        self.tree_legend_label = tk.Label(self.legend_frame, text="", font=("Helvetica", 10))
        self.tree_legend_label.pack(anchor="center")

    def __init__(self, root):
        self.events = []
        self.queue = []
        self.plot_data = []
        self.query_lines = []
        self.time = 0
        self.undo_stack = []
        self.redo_stack = []
        self.bst = AVLTree()
        self.current_tree_view = "PQ"
        if root is not None:
            self.__init_gui(root)
        self.update_display()

    def set_tree_view(self, view):
        self.current_tree_view = view
        self.draw_tree_view()

    def draw_tree_view(self):
        self.tree_canvas.delete("all")
        canvas_width = int(self.tree_canvas.winfo_width())
        if canvas_width <= 1:
            canvas_width = 800
        x = canvas_width / 2
        y = 50
        x_offset = canvas_width / 4
        y_offset = 60
        if self.current_tree_view == "PQ":
            if self.bst.root:
                self._draw_bst(self.bst.root, x, y, x_offset, y_offset)
            self.tree_legend_label.config(text="Legend: PQ Tree (AVL) – Blue nodes show key and T: time")
        elif self.current_tree_view == "Augmented":
            tree = self.build_augmented_tree()
            if tree:
                self._draw_aug_tree(tree, x, y, x_offset, y_offset, self.tree_canvas)
            self.tree_legend_label.config(text="Legend: T = Time, K = Key, Del = Delete Time, Aug = Augmented Value")
        elif self.current_tree_view == "Updates":
            tree = self.build_update_tree()
            if tree:
                self._draw_update_tree(tree, x, y, x_offset, y_offset, self.tree_canvas)
            self.tree_legend_label.config(text="Legend: T = Time, K = Key, Upd = Update Value, Sum = Subtree Sum")

    def save_state(self):
        if len(self.undo_stack) >= 5:
            self.undo_stack.pop(0)
        self.undo_stack.append((list(self.events), self.time, list(self.query_lines)))
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append((list(self.events), self.time, list(self.query_lines)))
        self.events, self.time, self.query_lines = self.undo_stack.pop()
        self.reevaluate_events()

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append((list(self.events), self.time, list(self.query_lines)))
        self.events, self.time, self.query_lines = self.redo_stack.pop()
        self.reevaluate_events()

    def reevaluate_events(self):
        # Ensure events are sorted by time
        self.events = sorted(self.events, key=lambda x: x[0])
        self.queue = []
        self.plot_data = []
        self.bst = AVLTree()
        active_items = []
        for timestamp, event_type, value in self.events:
            if event_type == "add":
                active_items.append((timestamp, value))
                self.plot_data.append((timestamp, value, None))
                self.bst.insert(value, timestamp)
            elif event_type == "delete-min" and active_items:
                active_items.sort(key=lambda x: x[1])
                min_item = active_items.pop(0)
                self.bst.delete(min_item[1])
                for i, (t_added, key, t_deleted) in enumerate(self.plot_data):
                    if key == min_item[1] and t_deleted is None:
                        self.plot_data[i] = (t_added, key, timestamp)
                        break
        max_key = max([key for t_added, key, t_deleted in self.plot_data if t_deleted is None], default=0)
        self.query_lines = [(time, max_key, self.is_bridge(time)) for time, _, _ in self.query_lines]
        self.queue = active_items
        self.update_display()

    def log_event(self, action, value=None, time=None):
        if time is None:
            time = self.time
        if hasattr(self, 'event_log'):
            if action == "add":
                self.event_log.insert(tk.END, f"Time {time}: Add {value}")
            elif action == "delete-min":
                self.event_log.insert(tk.END, f"Time {time}: Delete Min")
            elif action == "query":
                self.event_log.insert(tk.END, f"Time {time}: Query")

    def insert_random(self):
        self.save_state()
        if not self.queue:
            action = random.choice(["add", "query"])
        else:
            action = random.choice(["add", "delete-min", "query"])
        if action == "add":
            value = random.randint(1, 100)
            self.events.append((self.time, "add", value))
            self.log_event("add", value, time=self.time)
        elif action == "delete-min":
            self.events.append((self.time, "delete-min", None))
            self.log_event("delete-min", time=self.time)
        elif action == "query":
            self.query()
            return
        self.time += 1
        self.reevaluate_events()

    def delete_min(self):
        if not self.queue:
            return
        self.save_state()
        self.events.append((self.time, "delete-min", None))
        self.log_event("delete-min", time=self.time)
        self.time += 1
        self.reevaluate_events()

    def is_bridge(self, query_time):
        count = 0
        for timestamp, event_type, _ in self.events:
            if timestamp > query_time:
                break
            if event_type == "add":
                count += 1
            elif event_type == "delete-min":
                count -= 1
        return count == 0

    def query(self):
        self.save_state()
        max_key = max([key for t_added, key, t_deleted in self.plot_data if t_deleted is None], default=0)
        is_bridge = self.is_bridge(self.time)
        self.events.append((self.time, "query", None))
        self.query_lines.append((self.time, max_key, is_bridge))
        self.log_event("query", time=self.time)
        self.time += 1
        self.update_plot()

    def clear_all(self):
        self.save_state()
        self.events = []
        self.time = 0
        self.queue = []
        self.plot_data = []
        self.query_lines = []
        self.bst = AVLTree()
        if hasattr(self, 'event_log'):
            self.event_log.delete(0, tk.END)
        self.update_display()

    def add_event(self):
        popup = tk.Toplevel(self.left_frame)
        popup.title("Add Insert Event")
        tk.Label(popup, text="Value to insert:").pack()
        event_value = tk.Entry(popup, width=20)
        event_value.pack()
        def save_event():
            self.save_state()
            try:
                value = int(event_value.get().strip())
                self.events.append((self.time, "add", value))
                self.log_event("add", value, time=self.time)
            except ValueError:
                pass
            self.time += 1
            popup.destroy()
            self.reevaluate_events()
        tk.Button(popup, text="Save", command=save_event).pack()

    def edit_event(self):
        selected = self.event_log.curselection()
        if not selected:
            return
        index = selected[0]
        if index >= len(self.events):
            print("Selected index is out of range. Please try again.")
            return
        event = self.events[index]
        event_type, value = event[1], event[2]
        popup = tk.Toplevel(self.left_frame)
        popup.title("Edit Event")
        tk.Label(popup, text="Event Type:").pack()
        event_type_var = tk.StringVar(value=event_type)
        def toggle_value_field():
            if event_type_var.get() != "add":
                event_value.config(state=tk.DISABLED)
            else:
                event_value.config(state=tk.NORMAL)
        tk.Radiobutton(popup, text="Add", variable=event_type_var, value="add", command=toggle_value_field).pack()
        tk.Label(popup, text="Value (if add):").pack()
        event_value = tk.Entry(popup, width=20)
        if value is not None:
            event_value.insert(0, str(value))
        event_value.pack()
        def save_edit():
            self.save_state()
            e_type = event_type_var.get()
            e_value = event_value.get().strip()
            timestamp = self.events[index][0]
            self.events.pop(index)
            if e_type == "add":
                try:
                    new_value = int(e_value)
                    self.events.insert(index, (timestamp, e_type, new_value))
                except ValueError:
                    pass
            self.event_log.delete(index)
            self.event_log.insert(index, f"Time {timestamp}: Add {e_value}")
            popup.destroy()
            self.reevaluate_events()
        tk.Button(popup, text="Save", command=save_edit).pack()

    def update_display(self):
        if hasattr(self, 'tree_canvas'):
            self.tree_canvas.delete("all")
            self.draw_tree_view()
        if hasattr(self, 'canvas_plot'):
            self.update_plot()

    def _draw_bst(self, node, x, y, x_offset, y_offset):
        if node.left:
            self.tree_canvas.create_line(x, y, x - x_offset, y + y_offset, fill="black")
            self._draw_bst(node.left, x - x_offset, y + y_offset, x_offset // 2, y_offset)
        if node.right:
            self.tree_canvas.create_line(x, y, x + x_offset, y + y_offset, fill="black")
            self._draw_bst(node.right, x + x_offset, y + y_offset, x_offset // 2, y_offset)
        self.tree_canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
        self.tree_canvas.create_text(x, y, text=f"{node.key}\nT:{node.timestamp}", fill="white")

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Key-Time Relationship")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Key")
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        max_key_ever = max([key for t_added, key, t_deleted in self.plot_data], default=0)
        for t_added, key, t_deleted in self.plot_data:
            if t_deleted is not None:
                self.ax.plot([t_added, t_deleted], [key, key], "k-")
                self.ax.plot([t_deleted, t_deleted], [0, key], "r-")
                self.ax.plot(t_added, key, "ko")
            else:
                self.ax.plot(t_added, key, "go")
                self.ax.plot([t_added, self.time], [key, key], "g--")
        for query_time, max_key, is_bridge in self.query_lines:
            color = "b-" if is_bridge else "k-"
            self.ax.plot([query_time, query_time], [0, max_key_ever], color)
        self.canvas_plot.draw()

    def _build_aug_tree(self, events, lo, hi):
        if lo >= hi:
            return None
        if hi - lo == 1:
            node = AugTreeNode(event=events[lo])
            t_added, key, t_deleted = events[lo]
            node.aug = key if t_deleted is not None else float('-inf')
            return node
        mid = (lo + hi) // 2
        left = self._build_aug_tree(events, lo, mid)
        right = self._build_aug_tree(events, mid, hi)
        node = AugTreeNode()
        node.left = left
        node.right = right
        left_aug = left.aug if left else float('-inf')
        right_aug = right.aug if right else float('-inf')
        node.aug = max(left_aug, right_aug)
        return node

    def build_augmented_tree(self):
        events = sorted(self.plot_data, key=lambda x: x[0])  # Sorted by time_added
        return self._build_aug_tree(events, 0, len(events))

    def _draw_aug_tree(self, node, x, y, x_offset, y_offset, canvas):
        if node.left:
            canvas.create_line(x, y, x - x_offset, y + y_offset)
            self._draw_aug_tree(node.left, x - x_offset, y + y_offset, x_offset / 2, y_offset, canvas)
        if node.right:
            canvas.create_line(x, y, x + x_offset, y + y_offset)
            self._draw_aug_tree(node.right, x + x_offset, y + y_offset, x_offset / 2, y_offset, canvas)
        rect_width = 60
        rect_height = 40
        left_x = x - rect_width / 2
        top_y = y - rect_height / 2
        right_x = x + rect_width / 2
        bottom_y = y + rect_height / 2
        canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill="lightblue")
        if node.event is not None:
            t_added, key, t_deleted = node.event
            text = f"T:{t_added} | K:{key}"
            if t_deleted is not None:
                text += f"\nDel:{t_deleted}"
            else:
                text += "\nDel:-"
        else:
            text = f"Aug:\n{node.aug if node.aug != float('-inf') else '-'}"
        canvas.create_text(x, y, text=text, font=("Helvetica", 8))

    def _build_update_tree(self, events, lo, hi):
        if lo >= hi:
            return None
        if hi - lo == 1:
            node = UpdateNode(event=events[lo])
            node.val = self.get_update_value(events[lo])
            node.sum = node.val
            return node
        mid = (lo + hi + 1) // 2  # Upper median to bias the split
        left = self._build_update_tree(events, lo, mid)
        right = self._build_update_tree(events, mid, hi)
        node = UpdateNode()
        node.left = left
        node.right = right
        node.sum = (left.sum if left else 0) + (right.sum if right else 0)
        return node

    def build_update_tree(self):
        events = sorted(self.events, key=lambda x: x[0])
        return self._build_update_tree(events, 0, len(events))

    def _draw_update_tree(self, node, x, y, x_offset, y_offset, canvas):
        if node.left:
            canvas.create_line(x, y, x - x_offset, y + y_offset)
            self._draw_update_tree(node.left, x - x_offset, y + y_offset, x_offset/2, y_offset, canvas)
        if node.right:
            canvas.create_line(x, y, x + x_offset, y + y_offset)
            self._draw_update_tree(node.right, x + x_offset, y + y_offset, x_offset/2, y_offset, canvas)
        rect_width = 60
        rect_height = 40
        left_x = x - rect_width/2
        top_y = y - rect_height/2
        right_x = x + rect_width/2
        bottom_y = y + rect_height/2
        canvas.create_rectangle(left_x, top_y, right_x, bottom_y, fill="lightgreen")
        if node.event is not None:
            timestamp, etype, val = node.event
            update_val = node.val
            if etype == "add":
                text = f"Add\nK:{val} | T:{timestamp}\nUpd:{update_val}"
            else:
                text = f"Del | T:{timestamp}\nUpd:{update_val}"
        else:
            text = f"Sum:\n{node.sum}"
        canvas.create_text(x, y, text=text, font=("Helvetica", 8))

    def update_update_tree(self):
        self.tree_canvas.delete("all")
        root = self.build_update_tree()
        if root:
            canvas_width = int(self.tree_canvas.winfo_width())
            if canvas_width <= 1:
                canvas_width = 800
            self._draw_update_tree(root, canvas_width/2, 50, canvas_width/4, 60, self.tree_canvas)

    def prompt_mode(self):
        print("Running in prompt mode.")
        print("Enter commands in the following format examples (all on one line):")
        print('Insert(0, 1) = Will insert a key with value 1 at time 0')
        print('Insert(7, "delete-min") = Will insert a delete-min event at time 7')
        print('Insert(16, "query") = Will insert a query at time 16')
        print('Example data structure: Insert(0, 1), Insert(1, 2), Insert(2, 3), Insert(4, "delete-min"), Insert(5, "query")')
        print('The data structure MUST end with a Query insert command!')
        print('\n')
        print('Legends of outputs:')
        print("Events: [(0, 'add', 1)] = [(time, action, key)]")
        print('Active Queue: [(0, 1)] = [(time, key)]')
        print('Plot Data: [(1, 0, None)] = [(key, time added, time deleted)]')
        input_str = input("Enter commands: ")
        pattern = re.compile(r'Insert\(([^,]+),([^)]+)\)')
        commands = pattern.findall(input_str)
        commands = sorted(commands, key=lambda x: int(x[0].strip()))
        for time_str, action_str in commands:
            cmd_time = int(time_str.strip())
            # Update global time to be maximum so far
            self.time = max(self.time, cmd_time)
            action = action_str.strip().strip('"').strip("'")
            if action.lower() == "delete-min":
                # Remove any existing delete-min at this time (if needed)
                self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="delete-min")]
                self.events.append((cmd_time, "delete-min", None))
                print(f"At time {cmd_time}: delete-min executed.")
            elif action.lower() == "query":
                self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="query")]
                self.events.append((cmd_time, "query", None))
                print(f"At time {cmd_time}: query executed.")
            else:
                try:
                    key = int(action)
                    # Remove any existing add event at this time so it is substituted
                    self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="add")]
                    self.events.append((cmd_time, "add", key))
                    print(f"At time {cmd_time}: insert {key} executed.")
                except ValueError:
                    print(f"Invalid action at time {cmd_time}: {action}")
            self.reevaluate_events()
            print("Events:", self.events)
            print("Active Queue:", self.queue)
            print("Plot Data:", self.plot_data)
            print("------")
        while True:
            more = input("Do you want to add more commands (y/n)? ")
            if more.lower().startswith("y"):
                input_str = input("Enter additional commands: ")
                commands = pattern.findall(input_str)
                commands = sorted(commands, key=lambda x: int(x[0].strip()))
                for time_str, action_str in commands:
                    cmd_time = int(time_str.strip())
                    self.time = max(self.time, cmd_time)
                    action = action_str.strip().strip('"').strip("'")
                    if action.lower() == "delete-min":
                        self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="delete-min")]
                        self.events.append((cmd_time, "delete-min", None))
                        print(f"At time {cmd_time}: delete-min executed.")
                    elif action.lower() == "query":
                        self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="query")]
                        self.events.append((cmd_time, "query", None))
                        print(f"At time {cmd_time}: query executed.")
                    else:
                        try:
                            key = int(action)
                            self.events = [ev for ev in self.events if not (ev[0]==cmd_time and ev[1]=="add")]
                            self.events.append((cmd_time, "add", key))
                            print(f"At time {cmd_time}: insert {key} executed.")
                        except ValueError:
                            print(f"Invalid action at time {cmd_time}: {action}")
                    self.reevaluate_events()
                    print("Events:", self.events)
                    print("Active Queue:", self.queue)
                    print("Plot Data:", self.plot_data)
                    print("------")
            else:
                break
        if self.events and self.events[-1][1].lower() != "query":
            print("Error: The last command must be a query to show persistence.")
        else:
            print("Final state after query:")
            print("Events:", self.events)
            print("Active Queue:", self.queue)
            print("Plot Data:", self.plot_data)

if __name__ == "__main__":
    mode = input("Choose mode (g for graphic, p for prompt): ")
    if mode.lower().startswith("p"):
        rpq = RetroactivePriorityQueue(None)
        rpq.prompt_mode()
    else:
        root = tk.Tk()
        app = RetroactivePriorityQueue(root)
        root.mainloop()
