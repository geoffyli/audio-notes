# Python modules
from tkinter import filedialog
import customtkinter as ctk
import threading
import os
from enum import Enum

# Project modules
from audio_processor import AudioProcessor
from settings import settings


# Set tkinter appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ProcessingStatus(Enum):
    """This enum class represents the status of audio file processing
    0: initial status
    1: processing status
    2: done status
    """

    INIT = 0
    PROCESSING = 1
    DONE = 2


class App(ctk.CTk):
    """This class represents the GUI of the application."""

    def __init__(self):
        super().__init__()
        # Set the audio file path
        self.audio_file_path = None
        # Configure window properties
        self.title("Audio Notes")
        self.geometry(f"{1100}x{880}")
        # Configure the grid layout (4x4)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # First column weight 0
        self.grid_columnconfigure(0, minsize=200)  # First column fixed width
        self.grid_columnconfigure(1, weight=1)  # Second column takes remaining space

        # Sidebar frame
        self.sidebar_frame = SiderbarFrame(self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        # Active frame
        self.active_frame_flag = 0  # 0: main frame, 1: settings frame
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=0, column=1, sticky="nsew")
        # Initially show only the main frame
        self.main_frame.tkraise()
        # Set up key bindings
        self.bind("<Up>", self.on_key_press)
        self.bind("<Down>", self.on_key_press)
        self.bind("<q>", self.on_key_press)
        self.bind("<w>", self.on_key_press)
        self.bind("<e>", self.on_key_press)

    def on_key_press(self, event):
        if self.active_frame_flag == 0:
            self.main_frame.handle_key_event(event)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        # Set the file processing status
        self.status = ProcessingStatus.INIT
        # Initialize audio processor
        self.audio_processor = AudioProcessor()
        # Configure the grid layout
        self.grid_rowconfigure(0, weight=20)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # Content frame
        self._set_content_frame()
        # Control frame
        self._set_control_frame()
        # File frame
        self._set_file_frame()
        # Bind application-level keys
        # self.bind("<Up>", self.select_utterance)
        # self.bind("<Down>", self.select_utterance)
        # self.bind("<q>", self.control_keys)
        # self.bind("<w>", self.control_keys)
        # self.bind("<e>", self.control_keys)


    def _set_control_frame(self):
        self.control_frame = ControlFrame(self)
        self.control_frame.grid(
            row=1, column=0, columnspan=3, padx=(20, 20), pady=(10, 10), sticky="nsew"
        )

    def _set_content_frame(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(
            row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )

    def _set_file_frame(self):
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(
            row=2, column=0, columnspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew"
        )
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
            command=self.browse_files,
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
        if self.status == ProcessingStatus.PROCESSING:
            return
        # Set processing status
        self.status = ProcessingStatus.PROCESSING
        # Set content frame the processing frame
        self.content_frame = ProcessingFrame(self)
        self.content_frame.grid(
            row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )
        # Start a new thread to process the audio file and load the result
        thread = threading.Thread(target=self.load_transcript_result, args=())
        thread.start()

    def load_transcript_result(self):
        # Load audio and transcript
        self.audio_processor.load_audio(self.audio_file_path)
        self.audio_processor.transcribe()
        # Set content frame the transcript frame
        self.content_frame = TranscriptFrame(self)
        self.content_frame.grid(
            row=0, column=0, columnspan=3, padx=(20, 20), pady=(20, 10), sticky="nsew"
        )
        self.control_frame.transcript_frame = self.content_frame
        # Set the done status
        self.status = ProcessingStatus.DONE

    def browse_files(self):
        # Open the file selector
        self.audio_file_path = filedialog.askopenfilename(
            initialdir=settings.initial_audio_dir,
            title="Select a File",
            filetypes=(("Audio files", "*.mp3 *.wav *.ogg *.m4a"),),
        )
        # Insert the chosen file path into the text box
        self.file_path_box.delete("1.0", ctk.END)
        self.file_path_box.insert("0.0", self.audio_file_path)

    def select_utterance(self, event):
        if self.status != ProcessingStatus.DONE:
            return
        transcript_frame = self.content_frame
        # Get the current view range of the parent canvas
        view_top_scale = transcript_frame._parent_canvas.yview()[1]
        view_bottom_scale = transcript_frame._parent_canvas.yview()[0]
        # Calculate the utterance no. of the lower boundary and the upper boundary of the center area
        lower_boundary_no = len(transcript_frame.utterances) * (
            view_top_scale - 0.4 * (view_top_scale - view_bottom_scale)
        )
        upper_boundary_no = len(transcript_frame.utterances) * (
            view_top_scale - 0.6 * (view_top_scale - view_bottom_scale)
        )

        if transcript_frame.cur_selected_no is not None:
            if event.keysym == "Up":
                if transcript_frame.cur_selected_no == 0:
                    return
                transcript_frame.select_new_utterance(
                    transcript_frame.cur_selected_no - 1
                )
                # Scroll the list if it exceeds the upper boundary
                if transcript_frame.cur_selected_no < upper_boundary_no:
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
                # Scroll the list if it exceeds the lower boundary
                if transcript_frame.cur_selected_no > lower_boundary_no:
                    transcript_frame._parent_canvas.yview("scroll", 16, "units")

    def control_keys(self, event):
        if event.keysym == "q":
            self.control_frame.play_audio_segment()
        elif event.keysym == "w":
            self.control_frame.display_or_hide()
        elif event.keysym == "e":
            self.control_frame.export_audio_segment()

    def handle_key_event(self, event):
        if event.keysym in ["Up", "Down"]:
            self.select_utterance(event)
        elif event.keysym in ["q", "w", "e"]:
            self.control_keys(event)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        # Grid layout 5*3
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=250)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)

        # Conponents
        self.settings_title_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="sw",
            fg_color="transparent",
        )
        self.settings_title_label.grid(
            row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nesw"
        )
        self.export_path_label = ctk.CTkLabel(
            self,
            text="Export folder path",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="sw",
            fg_color="transparent",
        )
        self.export_path_label.grid(
            row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="nesw"
        )
        self.export_path_btn = ctk.CTkButton(
            self,
            text="Choose",
            command=lambda: self.select_export_folder(),
        )
        self.export_path_btn.grid(
            row=2, column=5, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        # Create a frame with rounded corners
        self.export_path_frame = ctk.CTkFrame(
            self, height=16, fg_color="white", corner_radius=5
        )
        self.export_path_frame.grid(
            row=2, column=0, columnspan=5, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        # Place a label inside the frame
        self.path_text_label = ctk.CTkLabel(
            self.export_path_frame, text=settings.export_folder_path
        )
        self.path_text_label.pack(padx=10, pady=5)

        self.init_path_label = ctk.CTkLabel(
            self,
            text="Initial folder path",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="sw",
            fg_color="transparent",
        )
        self.init_path_label.grid(
            row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="nesw"
        )
        self.init_path_btn = ctk.CTkButton(
            self,
            text="Choose",
            command=lambda: self.select_init_folder(),
        )
        self.init_path_btn.grid(
            row=4, column=5, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        # Create a frame with rounded corners
        self.init_path_frame = ctk.CTkFrame(
            self, height=16, fg_color="white", corner_radius=5
        )
        self.init_path_frame.grid(
            row=4, column=0, columnspan=5, padx=(20, 20), pady=(5, 5), sticky="nsew"
        )
        # Place a label inside the frame
        self.init_path_text_label = ctk.CTkLabel(
            self.init_path_frame, text=settings.initial_audio_dir
        )
        self.init_path_text_label.pack(padx=10, pady=5)

    def select_export_folder(self):
        # Open the file selector
        settings.export_folder_path = filedialog.askdirectory(
            initialdir="/Users/geoffyli/Downloads",
            title="Select a folder",
        )
        # Insert the chosen file path into the text box
        self.path_text_label.configure(text=settings.export_folder_path)
        settings.save()

    def select_init_folder(self):
        # Open the file selector
        settings.initial_audio_dir = filedialog.askdirectory(
            initialdir="/Users/geoffyli/Downloads",
            title="Select a folder",
        )
        # Insert the chosen file path into the text box
        self.init_path_text_label.configure(text=settings.initial_audio_dir)
        settings.save()


class SiderbarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#c0c2c1", width=140, corner_radius=0)
        self.grid_rowconfigure(3, weight=1)
        self.logo_label = ctk.CTkLabel(
            self,
            text="Audio Notes",
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(
            self, text="Main", command=self.switch_to_main_frame
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(
            self, text="Settings", command=self.switch_to_settings_frame
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = ctk.CTkButton(self, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")

    def switch_to_main_frame(self):
        if self.master.active_frame_flag == 1:
            # Switch to main page
            self.master.main_frame.tkraise()
            self.master.active_frame_flag = 0

    def switch_to_settings_frame(self):
        if self.master.active_frame_flag == 0:
            # Switch to settings page
            self.master.settings_frame.tkraise()
            self.master.active_frame_flag = 1


class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(
            row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        # Transcript frame
        self.transcript_frame = None
        # Play button
        self.btn = ctk.CTkButton(
            self,
            text="Play",
            command=lambda: self.play_audio_segment(),
        )
        self.btn.grid(row=0, column=0, padx=(10, 10), pady=(25, 25), sticky="nesw")
        # Display/Hide button
        self.display_btn = ctk.CTkButton(
            self, text="Show/Hide", command=lambda: self.display_or_hide()
        )
        self.display_btn.grid(
            row=0, column=1, padx=(10, 10), pady=(25, 25), sticky="nesw"
        )
        # Export button
        self.export_btn = ctk.CTkButton(
            self,
            text="Export",
            command=lambda: self.export_audio_segment(),
        )
        self.export_btn.grid(
            row=0, column=2, padx=(10, 10), pady=(25, 25), sticky="nesw"
        )

    def display_or_hide(self):
        if self.master.status != ProcessingStatus.DONE:
            return
        sentence_frame = self.transcript_frame.utterances[
            self.transcript_frame.cur_selected_no
        ]
        if sentence_frame.display:
            # Hide transcript
            sentence_frame.textbox.delete("1.0", ctk.END)
            sentence_frame.display = False
        else:
            # Show transcript
            sentence_frame.textbox.delete("1.0", ctk.END)
            sentence_frame.textbox.insert("0.0", sentence_frame.sentence.text)
            sentence_frame.display = True

    def play_audio_segment(self):
        if self.master.status != ProcessingStatus.DONE:
            return
        sentence_frame = self.transcript_frame.utterances[
            self.transcript_frame.cur_selected_no
        ]
        start = sentence_frame.sentence.start
        end = sentence_frame.sentence.end
        thread = threading.Thread(
            target=self.master.audio_processor.play_audio_segment, args=(start, end)
        )
        thread.start()

    def export_audio_segment(self):
        if self.master.status != ProcessingStatus.DONE:
            return
        sentence_frame = self.transcript_frame.utterances[
            self.transcript_frame.cur_selected_no
        ]
        start = sentence_frame.sentence.start
        end = sentence_frame.sentence.end

        base_name_with_extension = os.path.basename(
            self.master.audio_file_path
        )  # Gets 'xxx.mp3'
        base_name = os.path.splitext(base_name_with_extension)[0]  # Gets 'xxx'

        sentence_file_name = (
            base_name + "_s" + str(self.transcript_frame.cur_selected_no) + ".mp3"
        )
        settings.sentence_counter += 1
        self.master.audio_processor.export_audio_segment(
            start, end, settings.export_folder_path, sentence_file_name
        )


class ProcessingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # configure grid layout (4x4)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.processing_bar = ctk.CTkProgressBar(self)
        self.processing_bar.grid(
            row=0, column=0, padx=(80, 80), pady=(10, 0), sticky="we"
        )
        self.processing_bar.configure(mode="indeterminnate")
        self.processing_bar.start()


class TranscriptFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Attributes
        self.sentences = master.audio_processor.sentences
        self.row_num = 0
        self.columnconfigure(0, weight=1)
        # Configure selected
        self.cur_selected_no = 0
        # List of utterances
        self.utterances = []
        for sentence in self.sentences:
            self.utterances.append(
                UtteranceFrame(self, sentence, self.row_num, self.cur_selected_no)
            )
            self.row_num += 1

    def select_new_utterance(self, new_no):
        if self.cur_selected_no == new_no:
            return
        self.utterances[self.cur_selected_no].configure(border_width=0)
        self.utterances[new_no].configure(
            border_width=2, border_color="DarkOliveGreen3"
        )
        self.cur_selected_no = new_no


class UtteranceFrame(ctk.CTkFrame):
    def __init__(self, master, sentence, no, cur_selected_no, **kwargs):
        super().__init__(master, **kwargs)
        # Attributes
        self.sentence = sentence
        self.display = False
        self.exported = False
        self.no = no
        self.cur_selected_no = cur_selected_no

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)
        self.grid_columnconfigure(4, weight=2)
        self.grid(row=no, column=0, padx=(10, 10), pady=(5, 0), sticky="wnes")

        # No. label
        self.no_label = ctk.CTkLabel(self, text=str(no), fg_color="transparent")
        self.no_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nesw")

        # Checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text="", onvalue="on", offvalue="off", command=lambda: self.select()
        )

        # Text box
        self.textbox = ctk.CTkTextbox(self, height=52, wrap="word")
        self.textbox.grid(
            row=1, column=0, columnspan=5, padx=(10, 10), pady=(0, 5), sticky="nsew"
        )

        # Set border color
        if self.no == 0:
            self.configure(border_width=2, border_color="DarkOliveGreen3")
        else:
            self.configure(border_width=0)
        # Bind the click event
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.master.select_new_utterance(self.no)  # Your function logic here

    def select(self):
        self.master.select_new_utterance(self.no)
