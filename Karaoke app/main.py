import tkinter as tk
from tkinter import ttk
import requests # type: ignore
from PIL import Image, ImageTk # type: ignore
from io import BytesIO
import customtkinter as ctk # type: ignore
from datetime import datetime
import random

class MusicPlayer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Karaoke Player")
        self.root.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Sidebar
        self.create_sidebar()
        
        # Main content
        self.create_main_content()
        
        # Bottom player
        self.create_player_controls()
        
        # Load images
        self.load_images()
        
        # Current playing status
        self.is_playing = False
        self.current_volume = 50

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo
        logo_label = ctk.CTkLabel(sidebar, text="Karaoke", font=("Helvetica", 24, "bold"))
        logo_label.grid(row=0, column=0, pady=20, padx=20)

        # Playlists section
        playlists_label = ctk.CTkLabel(sidebar, text="PLAYLISTS", font=("Helvetica", 12))
        playlists_label.grid(row=1, column=0, pady=(20,10), padx=20, sticky="w")

        playlist_items = ["Your Favorites", "Last Listening", "Summer Party", "Chill Vibes"]
        for i, item in enumerate(playlist_items):
            btn = ctk.CTkButton(sidebar, text=item, fg_color="transparent", 
                              anchor="w", command=lambda x=item: self.show_playlist(x))
            btn.grid(row=i+2, column=0, pady=5, padx=20, sticky="ew")

        # Library section
        library_label = ctk.CTkLabel(sidebar, text="YOUR LIBRARY", font=("Helvetica", 12))
        library_label.grid(row=6, column=0, pady=(20,10), padx=20, sticky="w")

        library_items = ["Your Daily Mix", "Recently Played", "Songs", "Artists", "Albums"]
        for i, item in enumerate(library_items):
            btn = ctk.CTkButton(sidebar, text=item, fg_color="transparent", 
                              anchor="w", command=lambda x=item: self.show_library(x))
            btn.grid(row=i+7, column=0, pady=5, padx=20, sticky="ew")

    def create_main_content(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        main_frame.grid(row=0, column=1, rowspan=10, sticky="nsew", padx=0, pady=0)

        # Top navigation
        nav_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=20)

        # Navigation buttons
        back_btn = ctk.CTkButton(nav_frame, text="←", width=30, command=self.go_back)
        back_btn.pack(side="left", padx=5)
        
        forward_btn = ctk.CTkButton(nav_frame, text="→", width=30, command=self.go_forward)
        forward_btn.pack(side="left", padx=5)

        # Search bar
        search_entry = ctk.CTkEntry(nav_frame, placeholder_text="Search...", width=200)
        search_entry.pack(side="left", padx=20)

        # Profile section
        profile_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        profile_frame.pack(side="right")

        # Content area
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)

        # Featured playlist
        self.create_featured_playlist(content_frame)

        # Songs list
        self.create_songs_list(content_frame)

        # Album carousel
        self.create_album_carousel(content_frame)

    def create_featured_playlist(self, parent):
        featured_frame = ctk.CTkFrame(parent, fg_color="transparent")
        featured_frame.pack(fill="x", pady=20)

        # Title and buttons
        title_frame = ctk.CTkFrame(featured_frame, fg_color="transparent")
        title_frame.pack(fill="x")

        title_label = ctk.CTkLabel(title_frame, text="KARAOKE", 
                                 font=("Helvetica", 32, "bold"))
        title_label.pack(side="left")

        play_btn = ctk.CTkButton(title_frame, text="PLAY", 
                               fg_color="#1DB954", hover_color="#1ed760")
        play_btn.pack(side="left", padx=10)

        follow_btn = ctk.CTkButton(title_frame, text="FOLLOWING", 
                                fg_color="transparent", border_width=1)
        follow_btn.pack(side="left")

    def create_songs_list(self, parent):
        songs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        songs_frame.pack(fill="x", pady=20)

        songs = [
            ("Nevernight (feat. Starford)", "3:20", "509"),
            ("Monday (feat. Prince)", "3:45", "302"),
            ("No Bass", "4:15", "1,892"),
            ("Neon Future II", "3:30", "756")
        ]

        for i, (song, duration, plays) in enumerate(songs):
            song_frame = ctk.CTkFrame(songs_frame, fg_color="transparent")
            song_frame.pack(fill="x", pady=5)

            play_btn = ctk.CTkButton(song_frame, text="▶", width=30, 
                                  fg_color="transparent", hover_color="#1DB954")
            play_btn.pack(side="left", padx=5)

            title_label = ctk.CTkLabel(song_frame, text=song, anchor="w")
            title_label.pack(side="left", padx=10, fill="x", expand=True)

            duration_label = ctk.CTkLabel(song_frame, text=duration)
            duration_label.pack(side="right", padx=10)

            plays_label = ctk.CTkLabel(song_frame, text=f"{plays} plays")
            plays_label.pack(side="right", padx=10)

    def create_album_carousel(self, parent):
        # Create a frame to hold the canvas
        carousel_container = ctk.CTkFrame(parent, fg_color="transparent")
        carousel_container.pack(fill="x", pady=20)

        # Create a canvas for scrolling
        canvas = tk.Canvas(carousel_container, bg="#1a1a1a", highlightthickness=0, height=180)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas to hold the album items
        carousel_frame = ctk.CTkFrame(canvas, fg_color="transparent")

        # Add the frame to the canvas
        canvas.create_window((0, 0), window=carousel_frame, anchor="nw")

        # Populate the carousel with album items
        for i in range(8):
            album_frame = ctk.CTkFrame(carousel_frame, fg_color="transparent")
            album_frame.pack(side="left", padx=10)

            # Load random image
            img_url = f"https://picsum.photos/150/150?random={i}"
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            photo = ImageTk.PhotoImage(img)

            label = ttk.Label(album_frame, image=photo)
            label.image = photo  # Store reference to avoid garbage collection
            label.pack()

        # Update the canvas scroll region after adding all widgets
        carousel_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Enable mouse wheel scrolling for horizontal movement
        def on_mouse_scroll(event, canvas=canvas):
            canvas.xview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_scroll)


    def create_player_controls(self):
        player_frame = ctk.CTkFrame(self.root, height=100, fg_color="#282828")
        player_frame.grid(row=2, column=1, sticky="ew", padx=0, pady=0)
        player_frame.grid_propagate(False)

        # Control buttons
        controls_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
        controls_frame.pack(pady=10)

        shuffle_btn = ctk.CTkButton(controls_frame, text="🔀", width=30, 
                                 fg_color="transparent")
        shuffle_btn.pack(side="left", padx=5)

        prev_btn = ctk.CTkButton(controls_frame, text="⏮", width=30, 
                               fg_color="transparent")
        prev_btn.pack(side="left", padx=5)

        self.play_btn = ctk.CTkButton(controls_frame, text="▶", width=30, 
                                    fg_color="#1DB954", hover_color="#1ed760",
                                    command=self.toggle_play)
        self.play_btn.pack(side="left", padx=5)

        next_btn = ctk.CTkButton(controls_frame, text="⏭", width=30, 
                               fg_color="transparent")
        next_btn.pack(side="left", padx=5)

        repeat_btn = ctk.CTkButton(controls_frame, text="🔁", width=30, 
                                fg_color="transparent")
        repeat_btn.pack(side="left", padx=5)

        # Progress bar
        progress_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20)

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0.3)

        # Time labels
        time_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        time_frame.pack(fill="x")

        current_time = ctk.CTkLabel(time_frame, text="1:23")
        current_time.pack(side="left")

        total_time = ctk.CTkLabel(time_frame, text="3:45")
        total_time.pack(side="right")

        # Volume control
        volume_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
        volume_frame.pack(side="right", padx=20)

        volume_btn = ctk.CTkButton(volume_frame, text="🔊", width=30, 
                                fg_color="transparent")
        volume_btn.pack(side="left", padx=5)

        volume_slider = ctk.CTkSlider(volume_frame, from_=0, to=100, 
                                    width=100)
        volume_slider.pack(side="left", padx=5)
        volume_slider.set(50)

    def load_images(self):
        # Load and store images for the interface
        pass

    def toggle_play(self):
        self.is_playing = not self.is_playing
        self.play_btn.configure(text="⏸" if self.is_playing else "▶")

    def show_playlist(self, playlist):
        print(f"Showing playlist: {playlist}")

    def show_library(self, section):
        print(f"Showing library section: {section}")

    def go_back(self):
        print("Going back")

    def go_forward(self):
        print("Going forward")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MusicPlayer()
    app.run()
