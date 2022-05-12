from tkinter import *
from tkinter import ttk
from hmm_pos_tagger import PosTagger

class PosTaggerGui:

    def __init__(self, tagger, title='HMM POS Tagger'):
        self.tagger = tagger

        self.root = Tk()
        self.root.title = title
        self._create_gui(self.root)

    def start(self):
        self.sample_entry.focus()
        self.root.mainloop()

    def _create_gui(self, root):
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        ttk.Label(self.mainframe, text="Sample:").grid(column=1, row=1, sticky=(W,E))

        self.sample = StringVar()
        self.sample_entry = ttk.Entry(self.mainframe, width=40, textvariable=self.sample)
        self.sample_entry.grid(column=2, row=1, sticky=(W,E))

        self.tagged_sample = StringVar()
        ttk.Label(self.mainframe, textvariable=self.tagged_sample).grid(column=2, row=2, sticky=(W,E))

        ttk.Label(self.mainframe, text="Tagged Sample:").grid(column=1, row=2, sticky=(W,E))

        ttk.Button(self.mainframe, text="Quit", command=self._quit).grid(column=2,row=3,sticky=E)
        ttk.Button(self.mainframe, text="Tag", command=self._tag).grid(column=3, row=3, sticky=W)

        # Styling in post
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)

        # Key Binds
        root.bind("<Return>", self._tag)
        root.bind("q", self._quit)

    def _tag(self, *args):
        tags = self.tagger.predict(self.sample.get())
        split_sample = self.sample.get().split(' ')

        self.tagged_sample.set(' '.join([f'{word}/{tag}' for word, tag in zip(split_sample, tags)]))

    def _quit(self, *args):
        self.root.destroy()

