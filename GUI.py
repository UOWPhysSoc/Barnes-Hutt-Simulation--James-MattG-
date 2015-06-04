#! python3

import Barnes_Hutt_nbody_Simulation as bh
from tkinter import *
from Distributions import *

CONSTANTS = {'dt':'0.01',
             't':'1',
             'G':'1'}

class BarnesGUI(Frame):

    def __init__(self,master=None):

        self.master = master
        Frame.__init__(self, self.master)
        self.master.title = 'Barnes Hutt GUI'
        self.mainFrame = Frame(self.master)
        self.distFrame = Frame(self.master)
        self.dt = StringVar()
        self.dt.set(CONSTANTS['dt'])
        self.t = StringVar()
        self.t.set(CONSTANTS['t'])
        self.G = StringVar()
        self.G.set(CONSTANTS['G'])
        self.fileName = StringVar()
        self.activeDist = []
        self.activeDistWidgets = []

        #Create the default widgets for value entry
        self.createDefaultWidgets()
        self.mainFrame.pack()
        self.pack()

        #Create menu bar
        self.createDistMenu()

    def finish(self):
        if self.dt.get().replace('.','').isnumeric():
            print(self.dt.get())
            self.quit()
        else:
            messagebox.showerror(message='Invalid Input! Try again.', title='U dun fukd up')


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

        # dt Entry
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
            print(i)
            self.distMenu.add_command(label=i['name'],command=lambda:self.addDist(i['fname']))
        self.master.config(menu=self.menuBar)


    def addDist(self, distName):
        print(distName)
        self.activeDist.append(exec(distName + '()'))
        self.activeDistWidgets.append(Frame(self.master))
        
        pass

    def makeWidget(self, pname,ptype,pdefault):

        if ptype == 'numeric':
            pass
        
           
        

'''    def checkInput(self, value, vtype):

        if vytpe == 'int':


        if vtype == 'str':


        if vtype == 'decimal':
            value.get().replace('.','').isnumeric():
                return True
        else:
            agebox.showerror(message='Invalid Input! '+, title='U dun fukd up')'''
        

'''class Dist(Toplevel):

    def __init__(self, parent, master):

        self.parent = parent
        self.master = master
        Toplevel.__init__(self, self.master)
        Toplevel.title = 'Distributions'

        self.l = Label(self, text = 'hello')
        self.l.pack()'''

root = Tk()
root.title('Barnes GUI')
GUI = BarnesGUI(master = root)
GUI.mainloop()


'''each distribution has its own class. upon init define the required parameters,
pass this list into the create widgets. upon finish pass the values into the
dist run function and return the particle list, added to the main dist class
then passed into barnes'''
