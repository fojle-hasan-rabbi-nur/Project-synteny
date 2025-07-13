import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import webbrowser

class GenomeComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Genome Sequence Comparator Pro")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # App variables
        self.genome_file = tk.StringVar()
        self.chromo_file = tk.StringVar()
        self.results_text = ""
        self.dark_mode = False
        
        self.create_widgets()
        self.create_menu()
        
    def configure_styles(self):
        # Base styles
        self.style.configure('.', background='#f0f2f5', foreground='#2c3e50')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground='#2c3e50')
        self.style.configure('Accent.TButton', background='#3498db', foreground='white')
        self.style.map('Accent.TButton',
                      background=[('active', '#2980b9'), ('pressed', '#1a5276')])
        
        # Nucleotide color styles
        self.style.configure('A.TLabel', background='#4CAF50', foreground='white', font=('Consolas', 10, 'bold'))
        self.style.configure('T.TLabel', background='#FF5722', foreground='white', font=('Consolas', 10, 'bold'))
        self.style.configure('C.TLabel', background='#2196F3', foreground='white', font=('Consolas', 10, 'bold'))
        self.style.configure('G.TLabel', background='#FFC107', foreground='black', font=('Consolas', 10, 'bold'))
        self.style.configure('N.TLabel', background='#9E9E9E', foreground='white', font=('Consolas', 10, 'bold'))
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Genome File", command=lambda: self.browse_file(self.genome_file))
        file_menu.add_command(label="Open Chromosome File", command=lambda: self.browse_file(self.chromo_file))
        file_menu.add_separator()
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Run Comparison", command=self.run_comparison)
        analysis_menu.add_command(label="Clear Results", command=self.clear_results)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # DNA icon as text (could be replaced with actual image)
        dna_icon = ttk.Label(header_frame, text="🧬", font=('Segoe UI', 24))
        dna_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        title_label = ttk.Label(header_frame, 
                              text="Genome Sequence Comparator Pro", 
                              style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, 
                                   text=" Input Files ",
                                   padding=(15, 10),
                                   style='Card.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Genome file input
        genome_frame = ttk.Frame(input_frame)
        genome_frame.pack(fill=tk.X, pady=5)
        ttk.Label(genome_frame, text="Genome Sequence File:").pack(side=tk.LEFT, padx=(0, 10))
        genome_entry = ttk.Entry(genome_frame, 
                               textvariable=self.genome_file, 
                               width=50,
                               font=('Segoe UI', 10))
        genome_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        ttk.Button(genome_frame, 
                  text="Browse...", 
                  command=lambda: self.browse_file(self.genome_file)).pack(side=tk.LEFT)
        
        # Chromosome file input
        chromo_frame = ttk.Frame(input_frame)
        chromo_frame.pack(fill=tk.X, pady=5)
        ttk.Label(chromo_frame, text="Chromosome Details File:").pack(side=tk.LEFT, padx=(0, 10))
        chromo_entry = ttk.Entry(chromo_frame, 
                               textvariable=self.chromo_file, 
                               width=50,
                               font=('Segoe UI', 10))
        chromo_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        ttk.Button(chromo_frame, 
                  text="Browse...", 
                  command=lambda: self.browse_file(self.chromo_file)).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 15))
        
        ttk.Button(button_frame, 
                  text="Run Comparison", 
                  style='Accent.TButton',
                  command=self.run_comparison).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=(0, 10))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, 
                                     text=" Analysis Results ",
                                     padding=(15, 10))
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create custom tags for text coloring
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            font=('Consolas', 10), 
            padx=15, 
            pady=15, 
            width=100, 
            height=25,
            relief=tk.FLAT,
            bd=2
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for coloring
        self.results_text.tag_config('header', font=('Segoe UI', 12, 'bold'), spacing3=5)
        self.results_text.tag_config('subheader', font=('Segoe UI', 10, 'bold'), foreground='#2c3e50')
        self.results_text.tag_config('highlight', background='#FFF9C4', font=('Segoe UI', 10, 'bold'))
        self.results_text.tag_config('best', foreground='#D81B60', font=('Segoe UI', 11, 'bold'))
        self.results_text.tag_config('A', foreground='#4CAF50', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('T', foreground='#FF5722', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('C', foreground='#2196F3', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('G', foreground='#FFC107', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('N', foreground='#9E9E9E', font=('Consolas', 10, 'bold'))
        self.results_text.tag_config('match', background='#E8F5E9')
        self.results_text.tag_config('mismatch', background='#FFEBEE')
        self.results_text.tag_config('gap', background='#E0E0E0')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, 
                              textvariable=self.status_var, 
                              relief=tk.SUNKEN, 
                              anchor=tk.W,
                              font=('Segoe UI', 9))
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def browse_file(self, target_var):
        filetypes = (
            ('FASTA files', '*.fasta'),
            ('Text files', '*.txt'),
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title="Select file", 
            filetypes=filetypes
        )
        if filename:
            target_var.set(filename)
            self.status_var.set(f"Selected file: {os.path.basename(filename)}")
    
    def colorize_sequence(self, sequence):
        """Insert sequence with color-coded nucleotides"""
        for char in sequence:
            upper_char = char.upper()
            if upper_char == 'A':
                self.results_text.insert(tk.END, char, 'A')
            elif upper_char in ('T', 'U'):
                self.results_text.insert(tk.END, char, 'T')
            elif upper_char == 'C':
                self.results_text.insert(tk.END, char, 'C')
            elif upper_char == 'G':
                self.results_text.insert(tk.END, char, 'G')
            else:
                self.results_text.insert(tk.END, char, 'N')
    
    def visualize_alignment(self, seq1, seq2, alignment_line):
        """Visualize alignment with color-coded matches/mismatches"""
        self.results_text.insert(tk.END, "\nAlignment Visualization:\n", 'subheader')
        
        # Top sequence (seq1)
        self.results_text.insert(tk.END, "Reference: ")
        self.colorize_sequence(seq1)
        self.results_text.insert(tk.END, "\n")
        
        # Alignment indicators
        self.results_text.insert(tk.END, "           ")
        for i, char in enumerate(alignment_line):
            if char == 'R':
                self.results_text.insert(tk.END, "|", 'match')
            elif char == 'W':
                self.results_text.insert(tk.END, "·", 'mismatch')  # Middle dot character
            else:
                self.results_text.insert(tk.END, " ", 'gap')
        self.results_text.insert(tk.END, "\n")
        
        # Bottom sequence (seq2)
        self.results_text.insert(tk.END, "Comparison: ")
        self.colorize_sequence(seq2)
        self.results_text.insert(tk.END, "\n")
    
    def calculate_statistics(self, seq1, seq2):
        """Calculate additional statistics about the alignment"""
        len1, len2 = len(seq1), len(seq2)
        max_len = max(len1, len2)
        min_len = min(len1, len2)
        
        return {
            "length_ratio": f"{min_len/max_len:.1%}",
            "gc_content1": f"{((seq1.count('G') + seq1.count('C'))/len1):.1%}" if len1 > 0 else "N/A",
            "gc_content2": f"{((seq2.count('G') + seq2.count('C'))/len2):.1%}" if len2 > 0 else "N/A"
        }
    
    def run_comparison(self):
        genome_file = self.genome_file.get()
        chromo_file = self.chromo_file.get()
        
        if not genome_file or not chromo_file:
            messagebox.showerror("Input Error", "Please select both genome and chromosome files")
            return
        
        if not os.path.exists(genome_file) or not os.path.exists(chromo_file):
            messagebox.showerror("File Error", "One or both files do not exist")
            return
        
        try:
            self.status_var.set("Processing... Please wait")
            self.root.update()
            
            # Read files
            genome_seq = self.read_genome_file(genome_file)
            chromo_list = self.read_chromosome_file(chromo_file, genome_seq)
            
            # Prepare results display
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "GENOME COMPARISON REPORT\n", 'header')
            self.results_text.insert(tk.END, "="*60 + "\n\n")
            
            # Genome information
            self.results_text.insert(tk.END, "Genome Information:\n", 'subheader')
            self.results_text.insert(tk.END, f"• File: {os.path.basename(genome_file)}\n")
            self.results_text.insert(tk.END, f"• Length: {len(genome_seq):,} bp\n")
            self.results_text.insert(tk.END, f"• GC Content: {((genome_seq.count('G') + genome_seq.count('C'))/len(genome_seq)):.1%}\n\n")
            
            # Chromosome information
            self.results_text.insert(tk.END, "Chromosome Information:\n", 'subheader')
            self.results_text.insert(tk.END, f"• File: {os.path.basename(chromo_file)}\n")
            self.results_text.insert(tk.END, f"• Chromosomes to compare: {len(chromo_list)}\n\n")
            
            # Comparison section
            self.results_text.insert(tk.END, "Pairwise Comparisons:\n", 'subheader')
            self.results_text.insert(tk.END, "="*60 + "\n\n")
            
            best_pair = None
            best_similarity = 0
            best_alignment_result = []
            comparison_count = 0
            
            # Compare all chromosome pairs
            for i in range(len(chromo_list)):
                for j in range(i+1, len(chromo_list)):
                    id1, seq1 = chromo_list[i]
                    id2, seq2 = chromo_list[j]
                    
                    # Calculate alignment and similarity
                    similarity, alignment_visual = self.calculate_alignment(seq1, seq2)
                    stats = self.calculate_statistics(seq1, seq2)
                    
                    # Display comparison header
                    self.results_text.insert(tk.END, f"Comparison {comparison_count + 1}: {id1} vs {id2}\n", 'highlight')
                    self.results_text.insert(tk.END, f"• Similarity: {similarity:.2f}%\n")
                    self.results_text.insert(tk.END, f"• Length ratio: {stats['length_ratio']}\n")
                    self.results_text.insert(tk.END, f"• GC Content: {id1}={stats['gc_content1']}, {id2}={stats['gc_content2']}\n\n")
                    
                    # Visualize the alignment if sequences are not too long
                    if len(alignment_visual) >= 3 and len(seq1) < 100 and len(seq2) < 100:
                        self.visualize_alignment(alignment_visual[0], alignment_visual[2], alignment_visual[1])
                    elif len(alignment_visual) >= 3:
                        self.results_text.insert(tk.END, "[Alignment visualization available for sequences < 100bp]\n")
                    
                    self.results_text.insert(tk.END, "-"*60 + "\n\n")
                    comparison_count += 1
                    
                    # Track best match
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_pair = (id1, id2)
                        best_alignment_result = alignment_visual
            
            # Display best match
            if best_pair:
                self.results_text.insert(tk.END, "\n" + "="*60 + "\n")
                self.results_text.insert(tk.END, "★ BEST MATCH RESULT ★\n", 'best')
                self.results_text.insert(tk.END, f"• Chromosome Pair: {best_pair[0]} and {best_pair[1]}\n")
                self.results_text.insert(tk.END, f"• Similarity Score: {best_similarity:.2f}%\n\n")
                
                if len(best_alignment_result) >= 3:
                    if len(best_alignment_result[0]) < 100 and len(best_alignment_result[2]) < 100:
                        self.visualize_alignment(best_alignment_result[0], best_alignment_result[2], best_alignment_result[1])
                    else:
                        self.results_text.insert(tk.END, "[Full alignment not shown for long sequences]\n")
            
            self.status_var.set(f"Analysis complete. {comparison_count} comparisons performed.")
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred during analysis:\n{str(e)}")
            self.status_var.set("Error occurred during processing")
    
    def read_genome_file(self, genome_filename):
        with open(genome_filename, 'r') as f:
            lines = f.readlines()
            seq = ''.join([line.strip() for line in lines if not line.startswith('>')])
        return seq
    
    def read_chromosome_file(self, chromo_filename, genome_seq):
        chromo_list = []
        genome_length = len(genome_seq)
        with open(chromo_filename, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # skip header
                parts = line.strip().split(',')
                if len(parts) < 3:
                    continue
                
                chromo_id = parts[0]
                try:
                    start = int(parts[1])
                    end = int(parts[2])
                except ValueError:
                    continue
                
                if start >= genome_length:
                    chromo_seq = ""
                    self.results_text.insert(tk.END, f"⚠ Warning: Chromosome {chromo_id} start position {start} is out of genome range.\n")
                else:
                    end = min(end, genome_length)
                    chromo_seq = genome_seq[start:end]
                    if chromo_seq == "":
                        self.results_text.insert(tk.END, f"⚠ Warning: Chromosome {chromo_id} sequence is empty.\n")

                chromo_list.append((chromo_id, chromo_seq))
        return chromo_list
    
    def calculate_alignment(self, seq1, seq2):
        if len(seq1) == 0 or len(seq2) == 0:
            return 0.0, []

        max_match = 0
        best_alignment = []

        for offset in range(-len(seq2)+1, len(seq1)):
            match_count = 0
            alignment_line = ""

            for i in range(len(seq2)):
                pos_in_seq1 = i + offset
                if 0 <= pos_in_seq1 < len(seq1):
                    if seq1[pos_in_seq1] == seq2[i]:
                        alignment_line += "R"
                        match_count += 1
                    else:
                        alignment_line += "W"
                else:
                    alignment_line += "X"

            similarity = (match_count / len(seq2)) * 100

            visual_top = seq1
            visual_mid = (" " * max(0, offset)) + alignment_line
            visual_bottom = (" " * max(0, offset)) + seq2

            if match_count > max_match:
                max_match = match_count
                best_alignment = [visual_top, visual_mid, visual_bottom, f"Similarity: {similarity:.2f}%"]

        final_similarity = (max_match / len(seq2)) * 100
        return final_similarity, best_alignment
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")
    
    def export_results(self):
        content = self.results_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Export Warning", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), 
                      ("HTML files", "*.html"),
                      ("All files", "*.*")],
            title="Save analysis report as"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                self.status_var.set(f"Report saved to {os.path.basename(filename)}")
                messagebox.showinfo("Export Success", "Report exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report:\n{str(e)}")
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            # Dark theme colors
            bg_color = '#2c3e50'
            fg_color = '#ecf0f1'
            text_bg = '#34495e'
            text_fg = '#ffffff'
            self.style.configure('.', background=bg_color, foreground=fg_color)
        else:
            # Light theme colors
            bg_color = '#f0f2f5'
            fg_color = '#2c3e50'
            text_bg = '#ffffff'
            text_fg = '#000000'
            self.style.configure('.', background=bg_color, foreground=fg_color)
        
        # Update widget colors
        self.root.config(bg=bg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
                widget.config(bg=text_bg, fg=text_fg, insertbackground=fg_color)
    
    def show_help(self):
        help_text = """Genome Sequence Comparator Pro - User Guide

1. INPUT FILES:
   - Genome File: FASTA format containing the complete genome sequence
   - Chromosome File: CSV format with chromosome IDs and positions

2. RUNNING ANALYSIS:
   - Click "Run Comparison" to analyze all chromosome pairs
   - Results show pairwise alignments and similarity scores
   - Best match is highlighted at the end

3. RESULTS INTERPRETATION:
   - Nucleotides are color-coded (A=green, T=orange, C=blue, G=yellow)
   - Alignment shows matching positions with vertical bars (|)
   - Mismatches are shown with middle dots (·)

4. EXPORTING:
   - Save complete results to text file
   - Copy sections directly from the results window

Keyboard Shortcuts:
   - Ctrl+O: Open genome file
   - Ctrl+S: Save results
   - F1: Show this help"""

        help_window = tk.Toplevel(self.root)
        help_window.title("User Guide")
        help_window.geometry("700x500")
        
        text = scrolledtext.ScrolledText(help_window, 
                                       wrap=tk.WORD, 
                                       padx=15, 
                                       pady=15,
                                       font=('Segoe UI', 10))
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)
        
        ttk.Button(help_window, 
                  text="Close", 
                  command=help_window.destroy).pack(pady=10)
    
    def show_about(self):
        about_text = """Genome Sequence Comparator Pro v2.0

A sophisticated tool for comparing chromosome sequences 
within a genome with advanced visualization features.

Features:
- Color-coded nucleotide display
- Pairwise chromosome comparison
- Visual alignment display
- Similarity percentage calculation
- Comprehensive statistics
- Exportable results

Developed for Bioinformatics Applications
© 2023 Bioinformatics Tools"""

        messagebox.showinfo("About Genome Comparator Pro", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (replace with actual icon file if available)
    try:
        root.iconbitmap("dna_icon.ico")  # Provide your icon file
    except:
        pass  # Use default icon if custom icon not available
    
    app = GenomeComparatorApp(root)
    root.mainloop()