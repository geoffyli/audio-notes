# UI module
from tkinter import filedialog
import customtkinter as ctk
# Threading
import threading
# Import modules
from audio_processor import AudioProcessor


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Audio processor
        self.audio_processor = AudioProcessor()

        # configure window
        self.title("Audio Helper")
        self.geometry(f"{1100}x{880}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=20)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create sidebar frame
        self.sidebar_frame = SiderbarFrame(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        # Content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(
            row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )

        # Player frame
        self.player_frame = ctk.CTkFrame(self)
        self.player_frame.grid(
            row=1, column=1, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="nsew"
        )
        self.set_player_frame()

        # File frame
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(
            row=2, column=1, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="nsew"
        )
        self.set_file_frame()

        # set default values
        self.slider_2.configure(command=self.progressbar_3.set)
    
    def set_player_frame(self):
        self.player_frame.rowconfigure((0, 1), weight=1)
        self.player_frame.columnconfigure(0, weight=1)
        self.slider_2 = ctk.CTkSlider(self.player_frame, orientation="horizontal")
        self.slider_2.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="we")
        self.progressbar_3 = ctk.CTkProgressBar(
            self.player_frame, orientation="horizontal"
        )
        self.progressbar_3.grid(
            row=1, column=0, padx=(10, 20), pady=(10, 10), sticky="we"
        )

    def set_file_frame(self):
        self.file_frame.columnconfigure(0, weight=6)
        self.file_frame.columnconfigure(1, weight=1)
        self.file_frame.columnconfigure(2, weight=1)
        self.file_path_box = ctk.CTkTextbox(self.file_frame, height=30)
        self.file_path_box.grid(
            row=0, column=0, padx=(20, 0), pady=(20, 15), sticky="nsew"
        )
        self.choose_file_btn = ctk.CTkButton(
            master=self.file_frame,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            text="Choose a file",
            command=self.browseFiles,
        )
        self.choose_file_btn.grid(
            row=0, column=1, padx=(20, 20), pady=(20, 15), sticky="nsew"
        )
        self.process_btn = ctk.CTkButton(
            master=self.file_frame,
            border_width=2,
            text="Process",
            command=self.process_audio,
        )
        self.process_btn.grid(
            row=0, column=2, padx=(20, 20), pady=(20, 15), sticky="nsew"
        )

    def process_audio(self):
        self.set_processing_status()
        thread = threading.Thread(target=self.set_transcript_result, args=())
        thread.start()
    
    def set_transcript_result(self):
        # Get audio path
        file_path = self.file_path_box.get("1.0", ctk.END).strip()
        # Load audio and transcript
        self.audio_processor.load_audio(file_path)
        self.audio_processor.transcribe()
        # Set content frame
        self.content_frame = TranscriptFrame(self, self.audio_processor)

    def browseFiles(self):
        filename = filedialog.askopenfilename(
            initialdir="/Users/geoffyli/Documents/Projects/Python/SpeechToText",
            title="Select a File",
            filetypes=(("Audio files", "*.mp3 *.wav *.ogg *.m4a"),),
        )
        self.file_path_box.delete("1.0", ctk.END)
        self.file_path_box.insert("0.0", filename)

    def set_processing_status(self):
        self.content_frame = ProcessingFrame(self)
        self.content_frame.grid(
            row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )


class SiderbarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=140, corner_radius=0)
        self.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(
            self,
            text="ctk",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")

    def sidebar_button_event(self):
        print("sidebar_button click")


class ProcessingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # configure grid layout (4x4)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.processing_bar = ctk.CTkProgressBar(self)
        self.processing_bar.grid(
            row=0, column=0, padx=(50, 50), pady=(10, 0), sticky="we"
        )
        self.processing_bar.configure(mode="indeterminnate")
        self.processing_bar.start()


class TranscriptFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, audio_processor, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(
            row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )
        self.sentences = audio_processor.sentences
        self.row_num = 0
        # configure grid layout (4x4)
        # self.grid_columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        for sentence in self.sentences:
            UtteranceFrame(self, audio_processor, sentence, self.row_num)
            self.row_num += 1        

class UtteranceFrame(ctk.CTkFrame):
    def __init__(self, master, audio_processor, sentence, no, **kwargs):
        super().__init__(master, **kwargs)
        self.audio_processor = audio_processor
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid(row=no, column=0, sticky="wnes")
        # button
        self.btn = ctk.CTkButton(self, text="Play", command=lambda: self.play_audio_segment(sentence.start, sentence.end))
        self.btn.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="nesw")
        self.textbox = ctk.CTkTextbox(self, height=52, wrap="word")
        self.textbox.grid(
            row=1, column=0, columnspan=2, padx=(10, 10), pady=(0, 5), sticky="nsew"
        )
        self.textbox.insert(index="0.0", text=sentence.text)

    def play_audio_segment(self, start, end):
        thread = threading.Thread(target=self.audio_processor.play_audio_segment, args=(start, end))
        thread.start()

