import tkinter as tk               
from tkinter import font  as tkfont 
import back as bck

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
       
        #Background Colour
        self.configure(background='skyblue')

        #Label Heading 
        lh=tk.Label(self, text="Type of Data?",width=180)
        lh.config(font=("Helvetica", 25),bg='skyBlue',anchor='center',fg='black')
        lh.place(x = 270, y = 100, width=850, height=40)

        #Add Image Label(Online)
        from PIL import ImageTk, Image
        image = Image.open("logo.png")
        BTC_img = ImageTk.PhotoImage(image)
        
        #Button Online
        onb = tk.Button(self, image= BTC_img ,text="ONLINE", fg="red",command=lambda: controller.show_frame("PageOne"))
        onb.place(x=380, y=250, width=250, height=250)
        onb.image = BTC_img

        #Add Image Label(Offline)
        image1 = Image.open("logo2.png")
        BTC_img1 =ImageTk.PhotoImage(image1)
        
        lss=tk.Label(self, text="OR",width=180)
        lss.config(font=("Helvetica", 25),bg='skyBlue',anchor='center',fg='black')
        lss.place(x = 650, y = 350, width=50, height=40)
        
        #Button Offline
        ofb = tk.Button(self, image= BTC_img1 ,text="OFFLINE", fg="red",command=lambda: controller.show_frame("PageTwo"))
        ofb.place(x=720, y=250, width=250, height=250)
        ofb.image = BTC_img1

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #global Variable
        #Background Colour
        self.configure(background='skyblue')
        
        #Create Frame
        frame1 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='skyblue')
        frame1.place(x=240,y=90, width=870,height=270)
        
        #Label Heading 
        lh=tk.Label(self, text="Online Summary Generator",width=180)
        lh.config(font=("Helvetica", 25),bg='blue',anchor='center',fg='black')
        lh.place(x = 250, y = 100, width=850, height=40)

        #LABEL 1
        lba = tk.Label(self, text="Enter URL:",width=90)
        lba.config(font=("Courier", 20),bg='red',anchor='center',fg='white')
        lba.grid(column=0,row=0)
        lba.place(x = 250, y = 200, width=400, height=40)
        
        #Entry of PAT4
        self.e1= tk.Entry(self,width="50")
        self.e1.grid(column=1,row=0)
        self.e1.place(x = 700, y = 200, width=400, height=40)

        #declare label
        self.lbl=tk.Label(self,wraplength=700)
        self.lb1=tk.Label(self)
                
        #Button to Submit
        button = tk.Button(self, text="ENTER", fg="red",command=lambda: bck.online(self.e1.get(),self.lbl,self.lb1))
        button.place(x = 550, y =285, width=100, height=50)
        button1 = tk.Button(self, text="START PAGE",fg='red',command=lambda: controller.show_frame("StartPage"))
        button1.place(x = 700, y =285, width=100, height=50)
        
        #Clear Input Button
        clear_button = tk.Button(self, text=" Clear Text ", command=self.clear_text,bg='red')
        clear_button.place(x = 1050, y = 35, width = 60, height = 50)

    def clear_text(self):
        self.e1.delete(0, 'end')
        self.lbl.place_forget()
        self.lb1.place_forget()
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        #Background Colour
        self.configure(background='skyblue')
        
        #Create Frame
        frame1 = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, bd= 0, bg='skyblue')
        frame1.place(x=240,y=90, width=870,height=270)

        #Label Heading 
        lh=tk.Label(self, text="Offline Summary Generator",width=180)
        lh.config(font=("Helvetica", 25),bg='blue',anchor='center',fg='black')
        lh.place(x = 250, y = 100, width=850, height=40)

        #LABEL 1
        lba = tk.Label(self, text="Enter Path:",width=90)
        lba.config(font=("Courier", 20),bg='red',anchor='center',fg='white')
        lba.grid(column=0,row=0)
        lba.place(x = 250, y = 200, width=400, height=40)
        
        #Entry of PAT4
        self.e1= tk.Entry(self,width="50")
        self.e1.grid(column=1,row=0)
        self.e1.place(x = 700, y = 200, width=400, height=40)


        #declare label
        self.lbl=tk.Label(self,wraplength=700)
        self.lb1=tk.Label(self)
        
        #Button to Submit
        button = tk.Button(self, text="ENTER", fg="red",command=lambda: bck.offline(self.e1.get(),self.lbl,self.lb1))
        button.place(x = 550, y =285, width=100, height=50)
        button1 = tk.Button(self, text="START PAGE",fg='red',command=lambda: controller.show_frame("StartPage"))
        button1.place(x = 700, y =285, width=100, height=50)
    
        #Clear Input Button
        clear_button = tk.Button(self, text=" Clear Text ", command=self.clear_text,bg='red')
        clear_button.place(x = 1050, y = 35, width = 60, height = 50)

    def clear_text(self):
        self.e1.delete(0, 'end')
        self.lbl.place_forget()
        self.lb1.place_forget()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()