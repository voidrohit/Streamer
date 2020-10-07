from tkinter import *
import requests
import subprocess
import sys

root = Tk()
root.title('Movie Streamer')
HEIGHT = 600
WIDTH = 900

canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = Frame(root, bg="#80cbe0")
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

label = Label(frame, text="Movie Streamer", fg='red', bg='yellow')
label.config(font=("Yu Gothic UI Semibold",15))
label.place(relx=0.37,relwidth=0.3, relheight=0.1)

entry1 = Entry(frame, bd=5 )
entry1.place(relx=0.1, rely=0.16, relwidth=0.8, relheight=0.08)
entry1.insert(5, 'Movie Name')
entry1.configure(state=DISABLED)

frame2 = Frame(root, bg="blue")
frame2.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.4)

my_canvas = Canvas(frame2)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = Scrollbar(frame2, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0,0), window=second_frame, anchor="nw")

button=[]

def main(entry1):
	url = f"https://api.sumanjay.cf/torrent/?query={entry1}"
	magnet=[]
	torrent_link = requests.get(url).json()

	def index_num(index):
		window=Tk()
		magnet_link = magnet[index]
		canvas2 = Canvas(window, height=HEIGHT, width=WIDTH)
		canvas2.pack()


		link_frame = Frame(window, bg="#80cbe0")
		link_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

		text = Text(link_frame)
		text.pack()

		def link():
			text.insert("0.0", magnet_link)

		entry_button = Button(link_frame, text="Enter to get link and paste the link to webtorrent app", command=lambda:link())
		entry_button.config(font=("Yu Gothic UI Semibold",15))
		entry_button.place(relx=0.25, rely=0.7)

		window.mainloop()

	index = 0
	for result in torrent_link:
		button.append(Button(second_frame, text=result['name']+'  '+result['size'], command=lambda index=index: index_num(index)).grid(row=index+1, column=0, pady=10, padx=10))
		magnet.append(result['magnet'])
		index+=1

def stream(magnet_link):
		cmd=[]
		cmd.append('webtorrent')
		cmd.append(magnet_link)
		cmd.append('--vlc')

		if sys.platform.startswith('linux'):
			subprocess.call(cmd)
		elif sys.platform.startswith('win32'):
			subprocess.call(cmd, shell=True)


def on_click(event):
    entry1.configure(state=NORMAL)
    entry1.delete(0, END)

    entry1.unbind('<Button-1>', on_click_id)

on_click_id = entry1.bind('<Button-1>', on_click)

submit_button = Button(frame, text="Fetch Movie", command=lambda:main(entry1.get()))
submit_button.config(font=("Yu Gothic UI Semibold",15))
submit_button.place(relx=0.35, rely=0.24, relwidth=0.3, relheight=0.09)

root.mainloop()
