#! python3

import Barnes_Hutt_nbody_Simulation as bh
from tkinter import *
from Distributions import *
from functools import partial
from vector import *
import time


CONSTANTS = {'dt':'0.01',
             't':'1',
             'G':'1',
             'File Name':'untitled'}

class BarnesGUI(Frame):

    def __init__(self,master=None):

        self.master = master
        Frame.__init__(self, self.master)
        self.mainFrame = Frame(self.master)
        self.distFrame = Frame(self.master)
        self.dt = StringVar()
        self.dt.set(CONSTANTS['dt'])
        self.t = StringVar()
        self.t.set(CONSTANTS['t'])
        self.G = StringVar()
        self.G.set(CONSTANTS['G'])
        self.fileName = StringVar()
        self.fileName.set(CONSTANTS['File Name'])
        self.activeDist = []

        self.dist = barnesdist_GUI.distributions(self.G.get())

        #Create the default widgets for value entry
        self.createDefaultWidgets()
        self.mainFrame.pack(side=LEFT)
        self.pack()

        #Create menu bar
        self.createDistMenu()

    def finish(self):

        for i in self.activeDist:
            output = []
            for j in i.subFrames:
                output.append(j.pValue.get())
            i.dist.run(output,self.dist)

        b = bh.BarnesHut(self.dist, self.dt.get(), self.t.get(), self.fileName.get(),self.G.get())
        t_start = time.clock()
        while True:
            if b.quit == True:
                break
            b.step()
        t_final = time.clock()
        t_total = t_final - t_start
        if t_total < 60:
            print('Time taken was ' + str(t_total) + ' seconds')
        else:
            print('Time taken was ' + str(int(t_total/60)) + ':' + str(int(t_total%60)) + ' minutes')



        self.quit()


    def quit(self):
        self.master.destroy()

    #Wizardry updating
    def update_steps(self, var):
        # var needs to be a tkinter type variable (eg. IntVar)
        try:
            self.steps_text['text'] = '  ' + str(int(float((self.t.get()))/float(self.dt.get()))) + ' steps'
        except:
            pass
        finally:
            return True

    #To create all the default widgets
    def createDefaultWidgets(self):

        # Main titles
        self.mainTitle = Label(self.mainFrame, text='Main Parameters')
        self.mainTitle.config(font = ('',20))
        self.mainTitle.pack()
        separator = Frame(self.mainFrame,height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        self.distTitleFrame = Frame(self.distFrame)
        self.distTitle = Label(self.distTitleFrame, text='Active Distributions')
        self.distTitle.config(font = ('',20))
        self.distTitle.pack()
        separator = Frame(self.distTitleFrame,height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)
        self.distTitleFrame.pack()

        #dt Entry
        self.tFrame = Frame(self.mainFrame)
        self.dt_text = Label(self.tFrame, text = 'Step size:')
        self.dt_text.pack(side=LEFT)
        self.dt_entry = Entry(self.tFrame, width = 8, textvariable=self.dt)
        self.dt_entry.pack(side=LEFT)

        # time entry
        self.t_text = Label(self.tFrame, text = '  Total time:')
        self.t_text.pack(side=LEFT)
        self.t_entry = Entry(self.tFrame, width = 8, textvariable=self.t, validate='all', validatecommand=lambda:self.update_steps(self.t))
        self.t_entry.pack(side=LEFT)

        self.steps_text = Label(self.tFrame, text='  ' + str(int(float((self.t.get()))/float(self.dt.get()))) + ' steps')
        self.steps_text.pack(side=LEFT)

        self.tFrame.pack()

        # G entry
        self.GFrame = Frame(self.mainFrame)
        self.G_text = Label(self.GFrame, text = 'Gravitational constant:')
        self.G_text.pack(side=LEFT)
        self.G_entry = Entry(self.GFrame, width = 5, textvariable=self.G)
        self.G_entry.pack(side=LEFT)
        self.GFrame.pack()

        # File name

        self.fileNameFrame = Frame(self.mainFrame)
        self.fileName_text = Label(self.fileNameFrame, text = 'File name:')
        self.fileName_text.pack(side=LEFT)
        self.fileName_entry = Entry(self.fileNameFrame, width = 10, textvariable = self.fileName)
        self.fileName_entry.pack(side=LEFT)
        self.fileNameFrame.pack()
        
        # Finish button
        self.finishFrame = Frame(self.mainFrame)
        self.finish = Button(self.finishFrame, text = 'Finish', command=self.finish)
        self.finish.pack()
        self.finishFrame.pack()

        
    # To create the distributions menu
    def createDistMenu(self):

        self.menuBar = Menu(self.master)
        self.distMenu = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label = 'Distributions', menu = self.distMenu)
        for i in DISTRIBUTIONS:
            self.distMenu.add_command(label=i['name'],command=partial(self.addDist,i['fname']))
        self.master.config(menu=self.menuBar)


    def addDist(self, distName):

        self.activeDist.append(distFrame(self.distFrame, distName))
        self.distFrame.pack()
        

class distFrame(Frame):

    def __init__(self, master, distName):
        
        self.master = master
        Frame.__init__(self, self.master)

        separator = Frame(self,width=2, bd=1, relief=SUNKEN)
        separator.pack(fill=Y, padx=5, pady=5, side=LEFT)

        self.distName = distName
        self.dist = eval(self.distName + '()')
        self.frameLabel = Label(self,text = self.dist.name)
        self.frameLabel.pack()

        self.subFrames = []

        for i in self.dist.parameters:
            self.subFrames.append(subFrame(self,i['pName'],i['pType'],i['default']))

        self.pack(side=LEFT)
        
class subFrame(Frame):

    def __init__(self, master, label, pType, default):
        
        self.master = master
        Frame.__init__(self, self.master)
        self.pValue = StringVar()
        self.pValue.set(default)
        self.label = Label(self, text=label)
        self.label.pack(side=LEFT)

        if pType == 'numeric':
            self.entry = Entry(self, width = 8, textvariable = self.pValue)
        
        self.entry.pack(side=LEFT)
        self.pack()
           
        

'''    def checkInput(self, value, vtype):

        if vytpe == 'int':


        if vtype == 'str':


        if vtype == 'decimal':
            value.get().replace('.','').isnumeric():
                return True
        else:
            agebox.showerror(message='Invalid Input! '+, title='U dun fukd up')'''
        

root = Tk()
root.title('Barnes Hutt GUI')
GUI = BarnesGUI(master = root)
GUI.mainloop()


'''each distribution has its own class. upon init define the required parameters,
pass this list into the create widgets. upon finish pass the values into the
dist run function and return the particle list, added to the main dist class
then passed into barnes'''
