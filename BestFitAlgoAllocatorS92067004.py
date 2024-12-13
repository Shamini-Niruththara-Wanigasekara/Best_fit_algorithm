import tkinter as tk
from tkinter import messagebox  # Module imports

class BestFitAllocator:
    def __init__(self, block_sizes, process_sizes):  # Initializes block sizes, process sizes, and allocation list
        self.block_sizes = block_sizes
        self.process_sizes = process_sizes
        self.original_block_sizes = block_sizes[:]  # Keep track of original sizes for better visualization
        self.allocation = []

    def best_fit(self):  # Performs memory allocation
        """
        Allocates memory to processes using the Best Fit algorithm.
        """
        # n = The number of processes, m = The number of memory blocks
        m = len(self.block_sizes)  # list containing the sizes of memory blocks available
        n = len(self.process_sizes)  # list containing the sizes of processes that need memory

        self.allocation = [-1] * n  # no process is allocated initially

        for i in range(n):  # using i as the index
            best_idx = -1  # which will later hold the index of the most suitable block for the current process
            for j in range(m):  # check all the memory blocks
                if self.block_sizes[j] >= self.process_sizes[i]:
                    if best_idx == -1 or self.block_sizes[best_idx] > self.block_sizes[j]:
                        best_idx = j

            if best_idx != -1:
                self.allocation[i] = best_idx
                self.block_sizes[best_idx] -= self.process_sizes[i]

        return self.allocation


class BestFitGUI:  # responsible for building the graphical user interface using Tkinter
    def __init__(self, root):
        self.root = root
        self.root.title("Best Fit Memory Allocator")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        # Initializes block_sizes, process_sizes, and allocator as empty or None
        self.block_sizes = []
        self.process_sizes = []
        self.allocator = None

        # Input UI elements
        self.create_input_ui()

    def create_input_ui(self):
        # Header
        tk.Label(self.root, text="Best Fit Memory Allocation", font=("Arial", 18), bg="#f0f0f0").pack(pady=10)

        # Frame for inputs
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=20)

        # Block Sizes Input
        tk.Label(input_frame, text="Block Sizes (comma-separated):", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
        self.block_input = tk.Entry(input_frame, width=40, font=("Arial", 12))
        self.block_input.grid(row=0, column=1, padx=10, pady=10)

        # Process Sizes Input
        tk.Label(input_frame, text="Process Sizes (comma-separated):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
        self.process_input = tk.Entry(input_frame, width=40, font=("Arial", 12))
        self.process_input.grid(row=1, column=1, padx=10, pady=10)

        # Action Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        self.simulate_button = tk.Button(button_frame, text="Simulate", command=self.simulate_allocation, bg="#4CAF50", fg="white", font=("Arial", 12), width=15)
        self.simulate_button.grid(row=0, column=0, padx=10, pady=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_inputs, bg="#f44336", fg="white", font=("Arial", 12), width=15)
        self.reset_button.grid(row=0, column=1, padx=10, pady=10)

        # Output Frame
        output_frame = tk.Frame(self.root, bg="#f0f0f0")
        output_frame.pack(pady=20)

        self.output_text = tk.Text(output_frame, height=15, width=70, state="disabled", font=("Courier", 12), bg="#ffffff")
        self.output_text.grid(row=0, column=0, padx=10, pady=10)

        # Visualization Frame
        self.visual_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.visual_frame.pack(pady=20)

    def simulate_allocation(self):
        try:
            block_sizes = list(map(int, self.block_input.get().split(",")))
            process_sizes = list(map(int, self.process_input.get().split(",")))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers, separated by commas.")
            return

        # Perform best fit allocation
        self.allocator = BestFitAllocator(block_sizes, process_sizes)
        allocation = self.allocator.best_fit()

        # Display results
        self.display_results(allocation, block_sizes, process_sizes)
        self.visualize_allocation()

    def display_results(self, allocation, block_sizes, process_sizes):
        output = "Process No.   Process Size   Block No.\n"
        output += "-" * 40 + "\n"

        for i in range(len(process_sizes)):
            output += f"{i + 1:<12}{process_sizes[i]:<15}"
            if allocation[i] != -1:
                output += f"{allocation[i] + 1}\n"
            else:
                output += "Not Allocated\n"

        # Add summary of block memory usage
        output += "\nMemory Blocks Summary:\n"
        output += "Block No.   Original Size   Used Size   Free Size\n"
        output += "-" * 50 + "\n"
        for i, (original_size, current_size) in enumerate(zip(self.allocator.original_block_sizes, self.allocator.block_sizes)):
            used_size = original_size - current_size
            output += f"{i + 1:<11}{original_size:<15}{used_size:<12}{current_size}\n"

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state="disabled")

    def visualize_allocation(self):
        for widget in self.visual_frame.winfo_children():
            widget.destroy()

        tk.Label(self.visual_frame, text="Memory Blocks Visualization", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

        if not self.allocator:
            return

        for i, (original_size, current_size) in enumerate(zip(self.allocator.original_block_sizes, self.allocator.block_sizes)):
            used_size = original_size - current_size

            block_frame = tk.Frame(self.visual_frame, width=300, height=50, bg="white", highlightbackground="black", highlightthickness=1)
            block_frame.pack(pady=5)

            used_label = tk.Label(block_frame, text=f"Used: {used_size}B", bg="#4CAF50", fg="white", width=int(used_size / original_size * 30))
            used_label.pack(side="left", fill="y")

            free_label = tk.Label(block_frame, text=f"Free: {current_size}B", bg="#f44336", fg="white", width=int(current_size / original_size * 30))
            free_label.pack(side="left", fill="y")

    def reset_inputs(self):
        self.block_input.delete(0, tk.END)
        self.process_input.delete(0, tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        for widget in self.visual_frame.winfo_children():
            widget.destroy()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = BestFitGUI(root)
    root.mainloop()
