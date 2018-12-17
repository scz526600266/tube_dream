from tkinter import *
from subprocess import call, Popen, PIPE, STDOUT
from os import listdir, popen, remove
from shutil import move
from time import sleep
from getpass import getuser
import youtube_dl


class TubeDream:
    def __init__(self, master):
        self.colors = {
            'white': '#FFFFFF',
            'blue': '#2B547E',
            'black': '#000000',
            'red': '#FF3346',
            'green': '#306754',
            'grey': '#E5E4E2',
        }
        self.master = master
        self.master.title("Tube Dream")
        self.master.configure(bg=self.colors['black'])
        self.master.geometry("850x640")
        self.check_wav = IntVar()
        self.check_mp3 = IntVar()
        self.check_m4a = IntVar()
        self.base_url, self.link, self.playing = '', '', ''
        self.file_type, self.f_name = '', ''
        self.imagePath = PhotoImage(file="img/froggy.png")
        self.image = Label(
            master,
            image=self.imagePath,
            borderwidth=0
        )
        self.link_label = Label(
            master,
            fg=self.colors['grey'],
            bg=self.colors['blue'],
            text="Enter your YouTube link: ",
            width=57,
            font="Helvetica 10 bold"
        )
        self.youtube_link = Text(
            master,
            fg=self.colors['blue'],
            bg=self.colors['grey'],
            width=57,
            height=1
        )
        self.file_name_label = Label(
            master,
            fg=self.colors['grey'],
            bg=self.colors['blue'],
            text="Enter a name for your file: ",
            width=57,
            font="Helvetica 10 bold"
        )
        self.file_name = Text(
            master,
            fg=self.colors['blue'],
            bg=self.colors['grey'],
            width=57,
            height=1
        )
        self.wav = Checkbutton(
            master,
            fg=self.colors['red'],
            bg=self.colors['black'],
            text='.wav',
            variable=self.check_wav
        )
        self.wav.config(highlightbackground=self.colors['black'])
        self.mp3 = Checkbutton(
            master,
            fg=self.colors['red'],
            bg=self.colors['black'],
            text='.mp3',
            variable=self.check_mp3
        )
        self.mp3.config(highlightbackground=self.colors['black'])
        self.m4a = Checkbutton(
            master,
            fg=self.colors['red'],
            bg=self.colors['black'],
            text='.m4a',
            variable=self.check_m4a
        )
        self.m4a.config(highlightbackground=self.colors['black'])
        self.go_button = Button(
            master,
            fg=self.colors['grey'],
            bg=self.colors['green'],
            text="GO!",
            width=48,
            command=self.go
        )
        self.go_button.config(highlightbackground=self.colors['black'])
        self.clear_button = Button(
            master,
            fg=self.colors['grey'],
            bg=self.colors['green'],
            text="CLEAR",
            width=48,
            command=self.clear
        )
        self.clear_button.config(highlightbackground=self.colors['black'])
        self.explorer_label1 = Label(
            master,
            fg=self.colors['grey'],
            bg=self.colors['blue'],
            width=50,
            text="Downloaded Tracks:  "
        )
        self.explorer_label2 = Label(
            master,
            fg=self.colors['grey'],
            bg=self.colors['black'],
            width=50,
            text=""
        )
        self.explorer = Listbox(
            master,
            fg=self.colors['blue'],
            bg=self.colors['grey'],
            width=100,
            height=15,
            highlightcolor=self.colors['green']
        )
        self.delete_button = Button(
            master,
            fg=self.colors['white'],
            bg=self.colors['red'],
            text="DELETE",
            width=31,
            command=self.delete
        )
        self.delete_button.config(highlightbackground=self.colors['black'])
        self.stop_button = Button(
            master,
            fg=self.colors['grey'],
            bg=self.colors['green'],
            text="STOP",
            width=31,
            command=self.stop
        )
        self.stop_button.config(highlightbackground=self.colors['black'])
        self.play_button = Button(
            master,
            fg=self.colors['grey'],
            bg=self.colors['green'],
            text="PLAY",
            width=31,
            command=self.play
        )
        self.play_button.config(highlightbackground=self.colors['black'])
        self.status_label = Label(
            master,
            fg=self.colors['grey'],
            bg=self.colors['black'],
            width=60,
            text="Hello " + getuser()
        )
        # begin grid placement
        self.image.grid(
            row=0,
            sticky=W+E
        )
        self.link_label.grid(
            row=1,
            sticky=W,
            padx=20,
            pady=5
        )
        self.youtube_link.grid(
            row=1,
            sticky=E,
            padx=20,
            pady=5
        )
        self.file_name_label.grid(
            row=2,
            sticky=W,
            padx=20
        )
        self.file_name.grid(
            row=2,
            sticky=E,
            padx=20
        )
        self.wav.grid(
            row=3,
            sticky=W,
            padx=100,
            pady=5
        )
        self.mp3.grid(
            row=3,
            pady=5
        )
        self.m4a.grid(
            row=3,
            sticky=E,
            padx=100,
            pady=5
        )
        self.go_button.grid(
            row=5,
            sticky=W,
            padx=20,
            pady=10
        )
        self.clear_button.grid(
            row=5,
            sticky=E,
            padx=20,
            pady=10
        )
        self.explorer_label1.grid(
            row=6,
            sticky=W,
            padx=20
        )
        self.explorer_label2.grid(
            row=6,
            sticky=E,
            padx=20
        )
        self.explorer.grid(
            row=7,
            sticky=E+W,
            padx=20
        )
        self.play_button.grid(
            row=8,
            sticky=W,
            padx=20,
            pady=20
        )
        self.stop_button.grid(
            row=8,
            pady=20
        )
        self.delete_button.grid(
            row=8,
            sticky=E,
            padx=20,
            pady=20
        )
        self.status_label.grid(
            row=13,
            sticky=E+W
        )
        self.populate_explorer()

    def finished(self, crnt_trk):
        d = "FINISHED DOWNLOAD"
        base = 0
        for char in range(len(d) + 1):
            self.set_status_label(d[base:char])
            self.status_label.update_idletasks()
            sleep(0.1)

    def download(self):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': self.f_name + '.' + self.file_type,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': self.file_type,
                        'preferredquality': '192'
                    }
                ]
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.link])
            move(self.f_name + '.' + self.file_type, "downloads/")
            self.set_status_label("FINISHED")
        except:
            self.set_status_label("ERROR DOWNLOADING")

    def get_chkbtn_status(self):
        btn_status = [
            ('wav', self.check_wav.get()),
            ('mp3', self.check_mp3.get()),
            ('m4a', self.check_m4a.get())
        ]
        choice = []
        for i in range(len(btn_status)):
            if btn_status[i][1] != 1:
                continue
            else:
                choice.append(btn_status[i])
        if not choice:
            self.set_status_label("Please choose a file type")
            return None
        elif len(choice) > 1:
            self.set_status_label("Please choose only one file type")
            return None
        else:
            return choice[0][0]

    def populate_explorer(self):
        self.explorer.delete(0, 'end')
        downloads = sorted(listdir("downloads/"))
        self.explorer.insert("end", *downloads)
        self.set_explorer_status_label(str(self.explorer.size()))

    def go(self):
        self.link = self.youtube_link.get("1.0", END).strip()
        self.f_name = self.file_name.get("1.0", END).strip()
        self.file_type = self.get_chkbtn_status()
        current_track = self.f_name + '.' + self.file_type
        self.set_status_label('DOWNLOADING ' + current_track)
        self.status_label.update_idletasks()
        if not self.link or not self.f_name:
            message = "Check your URL and ensure you entered a filename..."
            self.set_status_label(message)
        else:
            if self.file_type is not None:
                self.download()
                self.populate_explorer()
                idx = sorted(listdir("downloads/")).index(current_track)
                self.explorer.selection_clear(0, END)
                self.explorer.selection_set(idx)
                self.finished(current_track)

    def clear(self):
        self.file_name.delete("1.0", END)
        self.youtube_link.delete("1.0", END)
        self.check_wav.set(0)
        self.check_mp3.set(0)
        self.check_m4a.set(0)
        self.set_status_label("Hello " + getuser())

    def delete(self):
        track = self.explorer.get(self.explorer.curselection())
        try:
            path = "downloads/" + track
            remove(path)
            d_message = path + " DELETED"
            self.set_status_label(d_message)
        except:
            message = "Unable to delete selected track"
            self.set_status_label(message)
        self.populate_explorer()

    def stop(self):
        if self.playing:
            self.set_status_label('STOPPING ' + self.playing)
            self.status_label.update_idletasks()
            psaux = []
            for line in popen("ps -aux | grep ffplay"):
                if 'ffplay' in line:
                    psaux = line.split()
                    break
            try:
                call('kill ' + psaux[1].strip(), shell=True)
            except Exception as e:
                self.set_status_label(e)

    def play(self):
        self.playing = self.explorer.get(self.explorer.curselection())
        self.set_status_label('PLAYING ' + self.playing)
        self.status_label.update_idletasks()
        ffplay = [
            "ffplay", "downloads/" + self.playing,
            "-nodisp", "-autoexit"
        ]
        Popen(ffplay, stdout=PIPE, stderr=STDOUT)

    def set_status_label(self, incoming_message1):
        self.status_label.config(text=incoming_message1)

    def set_explorer_status_label(self, incoming_message2):
        incoming_message2 += " Files Found"
        self.explorer_label2.config(text=incoming_message2)


if __name__ == "__main__":
    root = Tk()
    tube_dream = TubeDream(root)
    root.mainloop()
