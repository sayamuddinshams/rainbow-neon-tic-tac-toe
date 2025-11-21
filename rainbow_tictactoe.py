"""
tic_tac_toe_rainbow_gui.py
Rainbow Gradient Neon Tic-Tac-Toe with Minimax AI - RESPONSIVE VERSION
Created by Sayam-ud-Din
Requires: customtkinter, standard tkinter (python3-tk)
"""
import customtkinter as ctk
import tkinter as tk
import math

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ------------- Game logic (minimax) -------------
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a], (a,b,c)
    if "" not in board:
        return "Draw", None
    return None, None

def minimax(board, is_maximizing):
    winner, _ = check_winner(board)
    if winner == "O": return 1
    if winner == "X": return -1
    if winner == "Draw": return 0
    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best = min(best, score)
        return best

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# --------- Helper: rainbow color generator ----------
def rainbow_color(t):
    r = int((0.5 + 0.5*math.sin(2*math.pi*t + 0)) * 255)
    g = int((0.5 + 0.5*math.sin(2*math.pi*t + 2)) * 255)
    b = int((0.5 + 0.5*math.sin(2*math.pi*t + 4)) * 255)
    def boost(x): return max(0, min(255, int((x*1.1) + 20)))
    r,g,b = boost(r), boost(g), boost(b)
    return f"#{r:02x}{g:02x}{b:02x}"

# ----------------- Main App -----------------
class RainbowTicTacToe(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe — Rainbow Neon (Created by Sayam-ud-Din)")
        self.geometry("520x700")
        self.minsize(400, 550)  # Set minimum size
        self.resizable(True, True)  # Make resizable
        
        # game state
        self.board = [""] * 9
        self.buttons = []
        self.animating = False
        self.rainbow_phase = 0.0
        
        # Configure grid weights for main window
        self.grid_rowconfigure(0, weight=0)  # menu
        self.grid_rowconfigure(1, weight=0)  # logo
        self.grid_rowconfigure(2, weight=0)  # title
        self.grid_rowconfigure(3, weight=0)  # status
        self.grid_rowconfigure(4, weight=1)  # board (expandable)
        self.grid_rowconfigure(5, weight=0)  # footer
        self.grid_rowconfigure(6, weight=0)  # buttons
        self.grid_columnconfigure(0, weight=1)
        
        # Top menu
        self.create_menu()
        
        # Top logo area (canvas drawn)
        self.logo_canvas = tk.Canvas(self, highlightthickness=0, bg="#0b0b0d", height=100)
        self.logo_canvas.grid(row=1, column=0, sticky="ew", padx=10, pady=(10,5))
        
        # Title and status
        self.title_label = ctk.CTkLabel(self, text="Tic-Tac-Toe (Neon Rainbow)", font=("Inter", 24, "bold"))
        self.title_label.grid(row=2, column=0, pady=(4,2))
        
        self.status_label = ctk.CTkLabel(self, text="Your turn — You are X", font=("Inter", 16))
        self.status_label.grid(row=3, column=0, pady=(2,10))
        
        # Board container frame
        self.board_container = ctk.CTkFrame(self, corner_radius=20)
        self.board_container.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.board_container.grid_rowconfigure(0, weight=1)
        self.board_container.grid_columnconfigure(0, weight=1)
        
        # Inner frame for board to maintain aspect ratio
        self.board_frame = tk.Frame(self.board_container, bg="#0b0b0b")
        self.board_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Canvas for neon winning line
        self.line_canvas = tk.Canvas(self.board_frame, highlightthickness=0, bg="#0b0b0b")
        self.line_canvas.grid(row=0, column=0)
        
        # Button frame
        self.btn_frame = tk.Frame(self.board_frame, bg="#0b0b0b")
        self.btn_frame.grid(row=0, column=0)
        
        # Create 3x3 buttons
        for i in range(9):
            b = ctk.CTkButton(self.btn_frame, text="", 
                              fg_color="#111213", corner_radius=18,
                              font=("Inter", 36, "bold"),
                              command=lambda idx=i: self.on_player_move(idx))
            r, c = divmod(i, 3)
            b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            self.buttons.append(b)
        
        # Configure grid weights for buttons
        for i in range(3):
            self.btn_frame.grid_rowconfigure(i, weight=1, uniform="row")
            self.btn_frame.grid_columnconfigure(i, weight=1, uniform="col")
        
        # Footer
        self.footer = ctk.CTkLabel(self, text="Created by Sayam-ud-Din", font=("Inter", 12))
        self.footer.grid(row=5, column=0, pady=(10,5))
        
        # Restart & exit buttons at bottom
        self.bottom_frame = tk.Frame(self, bg="#0b0b0b")
        self.bottom_frame.grid(row=6, column=0, pady=(2,15))
        
        self.restart_btn = ctk.CTkButton(self.bottom_frame, text="Restart", command=self.reset_board, width=120)
        self.restart_btn.pack(side="left", padx=8)
        
        self.exit_btn = ctk.CTkButton(self.bottom_frame, text="Exit", command=self.quit, width=120)
        self.exit_btn.pack(side="left", padx=8)
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        
        # Initial sizing
        self.after(100, self.update_board_size)
        
        # Start rainbow animation loop
        self.after(60, self.animate_rainbow)
    
    def on_resize(self, event=None):
        """Handle window resize events"""
        self.after_cancel(getattr(self, '_resize_timer', None))
        self._resize_timer = self.after(50, self.update_board_size)
    
    def update_board_size(self):
        """Update board size based on window size"""
        # Get available space
        container_width = self.board_container.winfo_width()
        container_height = self.board_container.winfo_height()
        
        if container_width <= 1 or container_height <= 1:
            self.after(100, self.update_board_size)
            return
        
        # Calculate board size (square, with padding)
        max_size = min(container_width - 40, container_height - 40)
        board_size = max(200, min(max_size, 500))  # Between 200 and 500
        
        # Calculate cell size
        cell_size = (board_size - 48) // 3  # 48 for padding (4*6*2)
        button_size = cell_size
        
        # Update button sizes
        font_size = max(20, min(36, cell_size // 3))
        for btn in self.buttons:
            btn.configure(width=button_size, height=button_size, 
                         font=("Inter", font_size, "bold"))
        
        # Update canvas size
        self.line_canvas.configure(width=board_size, height=board_size)
        
        # Update logo canvas
        self.update_logo_size()
    
    def update_logo_size(self):
        """Update logo canvas size"""
        width = self.winfo_width() - 20
        self.logo_canvas.configure(width=max(300, width))
        self.draw_logo()
    
    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Restart", command=self.reset_board)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)
    
    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("400x200")
        about_window.resizable(False, False)
        
        label = ctk.CTkLabel(about_window, 
                            text="Rainbow Neon Tic-Tac-Toe\n\nCreated by Sayam-ud-Din\n\nMinimax AI — Unbeatable",
                            font=("Inter", 16))
        label.pack(expand=True, pady=20)
        
        ok_btn = ctk.CTkButton(about_window, text="OK", command=about_window.destroy, width=100)
        ok_btn.pack(pady=10)
    
    def draw_logo(self):
        """Draw the logo with responsive sizing"""
        w = self.logo_canvas.winfo_width()
        h = self.logo_canvas.winfo_height()
        
        if w <= 1:
            return
        
        self.logo_canvas.delete("all")
        self.logo_canvas.create_rectangle(0,0,w,h, fill="#070709", outline="")
        
        # Responsive circle size
        r = min(35, h // 3)
        cx, cy = min(70, w // 8), h // 2
        
        for i in range(6,0,-1):
            color = rainbow_color((self.rainbow_phase + i*0.02) % 1.0)
            self.logo_canvas.create_oval(cx-r-i, cy-r-i, cx+r+i, cy+r+i, outline=color, width=2)
        
        self.logo_canvas.create_oval(cx-r+8, cy-r+8, cx+r-8, cy+r-8, fill="#0b0b0b", outline="")
        
        font_size = max(16, min(26, r // 2))
        self.logo_canvas.create_text(cx, cy, text="SD", fill=rainbow_color(self.rainbow_phase), 
                                     font=("Inter", font_size, "bold"))
        
        # Responsive text positioning and sizing
        text_x = cx + r + 30
        title_size = max(12, min(18, w // 30))
        subtitle_size = max(9, min(11, w // 40))
        
        if w > 400:
            self.logo_canvas.create_text(text_x, cy-10, text="Rainbow Neon Tic-Tac-Toe", 
                                        anchor="w", fill="#dbe6ff", font=("Inter", title_size, "bold"))
            self.logo_canvas.create_text(text_x, cy+15, text="Unbeatable AI • Animated • Pure Python", 
                                        anchor="w", fill="#9fb2ff", font=("Inter", subtitle_size))
    
    def on_player_move(self, idx):
        if self.animating or self.board[idx] != "":
            return
        
        self.click_animation(idx)
        self.board[idx] = "X"
        self.buttons[idx].configure(text="X", state="disabled", fg_color="#0b0b0b")
        
        winner, line = check_winner(self.board)
        if winner:
            self.finish_game(winner, line)
            return
        
        self.status_label.configure(text="AI is thinking...")
        self.update()
        self.after(180, self.do_ai_move)
    
    def do_ai_move(self):
        mv = best_move(self.board)
        if mv is not None:
            self.button_glow(mv, times=2, duration=80)
            self.board[mv] = "O"
            self.buttons[mv].configure(text="O", state="disabled")
        
        winner, line = check_winner(self.board)
        if winner:
            self.finish_game(winner, line)
        else:
            self.status_label.configure(text="Your turn — You are X")
    
    def animate_rainbow(self):
        self.rainbow_phase = (self.rainbow_phase + 0.008) % 1.0
        
        for i,btn in enumerate(self.buttons):
            phase = (self.rainbow_phase + i*0.07) % 1.0
            c1 = rainbow_color(phase)
            
            if self.board[i] == "":
                btn.configure(fg_color=c1)
            else:
                btn.configure(fg_color="#0b0b0b")
        
        self.draw_logo()
        self.after(60, self.animate_rainbow)
    
    def click_animation(self, idx):
        btn = self.buttons[idx]
        orig = btn.cget("fg_color")
        bright = rainbow_color((self.rainbow_phase + idx*0.15) % 1.0)
        btn.configure(fg_color=bright)
        
        current_font = btn.cget("font")
        smaller_size = max(20, int(current_font[1] * 0.85))
        btn.configure(font=(current_font[0], smaller_size, "bold"))
        self.update()
        self.after(140, lambda: btn.configure(fg_color=orig, font=current_font))
    
    def button_glow(self, idx, times=3, duration=120):
        btn = self.buttons[idx]
        def blink(count):
            if count <= 0:
                btn.configure(fg_color="#0b0b0b")
                return
            btn.configure(fg_color=rainbow_color((self.rainbow_phase + idx*0.2) % 1.0))
            self.update()
            self.after(duration//2, lambda: btn.configure(fg_color="#0b0b0b"))
            self.after(duration, lambda: blink(count-1))
        blink(times)
    
    def finish_game(self, winner, line):
        if winner == "Draw":
            self.status_label.configure(text="It's a Draw!")
            for b in self.buttons:
                b.configure(state="disabled")
        else:
            self.status_label.configure(text=f"{winner} WINS!")
            if line:
                self.play_winning_line_animation(line)
            for b in self.buttons:
                b.configure(state="disabled")
    
    def play_winning_line_animation(self, triple):
        """Draw winning line with responsive coordinates"""
        canvas_width = self.line_canvas.winfo_width()
        cell_size = canvas_width / 3
        
        centers = []
        for i in range(9):
            r, c = divmod(i, 3)
            cx = c * cell_size + cell_size / 2
            cy = r * cell_size + cell_size / 2
            centers.append((cx, cy))
        
        x1, y1 = centers[triple[0]]
        x2, y2 = centers[triple[2]]
        
        self.animating = True
        glow_ids = []
        
        def animate_step(step_i=0, max_steps=24):
            nonlocal glow_ids
            t = step_i / max_steps
            
            for gid in glow_ids:
                try: self.line_canvas.delete(gid)
                except: pass
            glow_ids = []
            
            line_width = max(6, canvas_width // 50)
            
            for j in range(6):
                width = line_width - j
                phase = (self.rainbow_phase + j*0.05 + t*0.6) % 1.0
                color = rainbow_color(phase)
                gid = self.line_canvas.create_line(
                    x1 + (x2-x1)*t, y1 + (y2-y1)*t,
                    x1 + (x2-x1)*min(1, t + 0.03*(j+1)),
                    y1 + (y2-y1)*min(1, t + 0.03*(j+1)),
                    fill=color, width=width, capstyle=tk.ROUND, joinstyle=tk.ROUND)
                glow_ids.append(gid)
            
            if step_i < max_steps:
                self.after(35, lambda: animate_step(step_i+1, max_steps))
            else:
                def pulse(k):
                    if k <= 0:
                        self.animating = False
                        return
                    for gid in glow_ids:
                        self.line_canvas.itemconfigure(gid, state="normal")
                    self.after(180, lambda: [self.line_canvas.itemconfigure(gid, state="hidden") for gid in glow_ids] or self.after(80, lambda: pulse(k-1)))
                pulse(6)
        
        animate_step()
    
    def reset_board(self):
        if self.animating:
            return
        
        self.board = [""] * 9
        for btn in self.buttons:
            btn.configure(text="", state="normal", fg_color="#111213")
        self.line_canvas.delete("all")
        self.status_label.configure(text="Your turn — You are X")

# ------------ Run ------------
if __name__ == "__main__":
    app = RainbowTicTacToe()
    app.mainloop()