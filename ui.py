# UI module
from tkinter import filedialog
import customtkinter as ctk
# Threading
import threading
# Import modules
from audio_processor import AudioProcessor
import settings
import os

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

        # Bind keys
        self.bind("<Up>", self.up_and_down_key)
        self.bind("<Down>", self.up_and_down_key)

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
        # Load audio and transcript
        self.audio_processor.load_audio(settings.file_path)
        self.audio_processor.transcribe()
        # Set content frame
        self.content_frame = TranscriptFrame(self, self.audio_processor)

    def browseFiles(self):
        settings.file_path = filedialog.askopenfilename(
            initialdir="/Users/geoffyli/Library/CloudStorage/GoogleDrive-lyl1719770869@gmail.com/My Drive/Courses/TOEFL/23托福听力真题/23托福听力机经",
            title="Select a File",
            filetypes=(("Audio files", "*.mp3 *.wav *.ogg *.m4a"),),
        )
        self.file_path_box.delete("1.0", ctk.END)
        self.file_path_box.insert("0.0", settings.file_path)

    def set_processing_status(self):
        self.content_frame = ProcessingFrame(self)
        self.content_frame.grid(
            row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )

    def up_and_down_key(self, event):
        transcript_frame = self.content_frame
        view_top_scale = transcript_frame._parent_canvas.yview()[1]
        view_bottom_scale = transcript_frame._parent_canvas.yview()[0]
        lower_boundary = len(transcript_frame.utterances) * (view_top_scale - 0.4 * (view_top_scale - view_bottom_scale))
        upper_boundary = len(transcript_frame.utterances) * (view_top_scale - 0.6 * (view_top_scale - view_bottom_scale))
        if transcript_frame.cur_selected_no is not None:
            if event.keysym == "Up":
                if transcript_frame.cur_selected_no == 0:
                    return
                transcript_frame.select_new_utterance(
                    transcript_frame.cur_selected_no - 1
                )
                print(transcript_frame.cur_selected_no, upper_boundary)
                if transcript_frame.cur_selected_no < upper_boundary:
                    transcript_frame._parent_canvas.yview("scroll", -16, "units") 

            elif event.keysym == "Down":
                if (
                    transcript_frame.cur_selected_no
                    == len(transcript_frame.utterances) - 1
                ):
                    return
                transcript_frame.select_new_utterance(
                    transcript_frame.cur_selected_no + 1
                )
                print(transcript_frame.cur_selected_no, lower_boundary)
                if transcript_frame.cur_selected_no > lower_boundary:
                    transcript_frame._parent_canvas.yview("scroll", 16, "units") 
                



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

        # Attributes
        self.sentences = audio_processor.sentences
        self.row_num = 0
        self.columnconfigure(0, weight=1)
        # Configure selected
        self.cur_selected_no = 0
        # List of utterances
        self.utterances = []
        for sentence in self.sentences:
            self.utterances.append(
                UtteranceFrame(
                    self, audio_processor, sentence, self.row_num, self.cur_selected_no
                )
            )
            self.row_num += 1

    def select_new_utterance(self, new_no):
        if self.cur_selected_no == new_no:
            return
        self.utterances[self.cur_selected_no].configure(border_width=0)
        self.utterances[new_no].configure(
            border_width=2, border_color="DarkOliveGreen2"
        )
        self.cur_selected_no = new_no


class UtteranceFrame(ctk.CTkFrame):
    def __init__(
        self, master, audio_processor, sentence, no, cur_selected_no, **kwargs
    ):
        super().__init__(master, **kwargs)
        # Attributes
        self.sentence = sentence
        self.display = False
        self.exported = False
        self.no = no
        self.cur_selected_no = cur_selected_no

        self.audio_processor = audio_processor
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)
        self.grid_columnconfigure(4, weight=2)
        self.grid(row=no, column=0, sticky="wnes")

        # No. label
        self.no_label = ctk.CTkLabel(self, text=str(no), fg_color="transparent")
        self.no_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="nesw")

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text="", onvalue="on", offvalue="off", command=lambda: self.select()
        )

        # Play button
        self.btn = ctk.CTkButton(
            self,
            text="Play",
            command=lambda: self.play_audio_segment(sentence.start, sentence.end),
        )
        self.btn.grid(row=0, column=2, padx=(10, 10), pady=(5, 5), sticky="nesw")
        # Display/Hide button
        self.display_btn = ctk.CTkButton(
            self, text="Show", command=lambda: self.display_or_hide()
        )
        self.display_btn.grid(
            row=0, column=3, padx=(10, 10), pady=(5, 5), sticky="nesw"
        )
        # Export button
        self.export_btn = ctk.CTkButton(
            self,
            text="Export",
            command=lambda: self.export_audio_segment(sentence.start, sentence.end),
        )
        self.export_btn.grid(row=0, column=4, padx=(10, 10), pady=(5, 5), sticky="nesw")

        # Text box
        self.textbox = ctk.CTkTextbox(self, height=52, wrap="word")
        self.textbox.grid(
            row=1, column=0, columnspan=5, padx=(10, 10), pady=(0, 5), sticky="nsew"
        )

        # Set border color
        if self.no == 0:
            self.configure(border_width=2, border_color="DarkOliveGreen2")
        else:
            self.configure(border_width=0)
        # Bind the click event
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.master.select_new_utterance(self.no)  # Your function logic here

    def select(self):
        self.master.select_new_utterance(self.no)

    def display_or_hide(self):
        if self.display:
            # Hide transcript
            self.textbox.delete("1.0", ctk.END)
            self.display_btn.configure(text="Show")
            self.display = False
        else:
            # Show transcript
            self.textbox.delete("1.0", ctk.END)
            self.textbox.insert("0.0", self.sentence.text)
            self.display_btn.configure(text="Hide")
            self.display = True

    def play_audio_segment(self, start, end):
        thread = threading.Thread(
            target=self.audio_processor.play_audio_segment, args=(start, end)
        )
        thread.start()

    def export_audio_segment(self, start, end):
        folder_path = os.path.dirname(settings.file_path)
        self.audio_processor.export_audio_segment(
            start, end, folder_path, "sentence.mp3"
        )
        self.export_btn.configure(text="Exported")
