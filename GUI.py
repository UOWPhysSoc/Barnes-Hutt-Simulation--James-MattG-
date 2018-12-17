#! python3

import Barnes_Hutt_nbody_Simulation as bh
from wckToolTips import *
#from Toggle import ToggledFrame
from tkinter import *
from tkinter.ttk import *
from Distributions import *
from functools import partial
import time
import threading
import pickle
from math import log
from math import ceil


CONSTANTS = {'dt':'0.01',
             't':'1',
             'G':'1',
             'File Name':'untitled',
             'theta':'0.2',
             'damp':'0'}

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
        self.theta = StringVar()
        self.theta.set(CONSTANTS['theta'])
        self.damp = StringVar()
        self.damp.set(CONSTANTS['damp'])
        
        self.activeDist = []
        self.running = False
        self.cont = IntVar()
        self.cont.set(0)

        self.dist = barnesdist_GUI.distributions(self.G.get())

        #Create the default widgets for value entry
        self.createDefaultWidgets()
        self.mainFrame.pack(side=LEFT)
        self.pack()

        #Create menu bar
        self.createDistMenu()

    def finish(self):

        if not self.running:

            self.finish.config(text='Stop simulation')
            self.running = True

            if self.cont.get() == 0:

                for i in self.activeDist:
                    output = []
                    for j in i.subFrames:
                        output.append(j.pValue.get())
                    i.dist.run(output,self.dist, float(self.G.get()))

                self.b = bh.BarnesHut(self.dist,
                                  float(self.dt.get()),
                                  float(self.t.get()),
                                  self.fileName.get(),
                                  float(self.G.get()),
                                  theta=float(self.theta.get()),
                                  damp=float(self.damp.get()),
                                  withGUI = True)

            else:

                self.resumeSim(self.fileName.get())
            self.simBegin()


        else:

            self.b.finish = True
            self.running = False
            self.finish.config(text='Run')
            self.progress.destroy()
            self.clockFrame.destroy()
            
    def createConfig(self):
        
        for i in self.activeDist:
            output = []
            for j in i.subFrames:
                output.append(j.pValue.get())
            i.dist.run(output,self.dist, float(self.G.get()))

        toSave = [self.dist,
                          float(self.dt.get()),
                          float(self.t.get()),
                          self.fileName.get(),
                          float(self.G.get()),
                          float(self.theta.get()),
                          float(self.damp.get())]
        
        file = open('config.config', 'wb')
        pickle.dump(toSave, file, protocol = 2)
        file.close()

    def simBegin(self):
        
        self.progress = Progressbar(self.mainFrame, orient = 'horizontal', variable = self.b.percent, length = 300)
        self.progress.pack()

        self.clockFrame = Frame(self.mainFrame)
        self.clockVar = StringVar()
        self.T = {'T':0,'10m':0,'m':0,'10s':0,'s':0}
        self.clock = Label(self.mainFrame,textvariable = self.clockVar)
        self.clock.pack()
        self.clockFrame.pack()
        
        self.secondaryThread = threading.Thread(target=self.barnesRun)
        self.secondaryThread.start()

        self.clockThread = threading.Thread(target=self.convertTime)
        self.clockThread.start()

    def barnesRun(self):
        while True:
            if self.b.quit:
                self.running = False
                break
            self.b.step()
        try:
            self.progress.destroy()
        except:
            pass
        self.finish.config(text='Run')
        self.activeDist = []


    def quit(self):
        self.master.destroy()

    def convertTime(self):
        while self.running:
            self.T['T'] = int(time.time()-self.b.t_start)
            self.T['10m'] = int(self.T['T']/600)
            self.T['m'] = int(self.T['T']/60) - 10*self.T['10m']
            self.T['10s'] = int((self.T['T'] - 60*self.T['m'] - 600*self.T['10m'])/10)
            self.T['s'] = int(self.T['T'] - 60*self.T['m'] - 600*self.T['10m'] - 10*self.T['10s'])
            self.clockVar.set('Elapsed: '+str(self.T['10m'])+str(self.T['m'])+':'+str(self.T['10s'])+str(self.T['s']))
            time.sleep(1)

    def stopSim(self):
        self.b.finish = True
        self.stopSimButton.lower(self.finishFrame)
        self.finish.lift(self.finishFrame)
        

    #Wizardry updating
    def update_steps(self, var):
        # var needs to be a tkinter type variable (eg. IntVar)
        try:
            self.steps_text['text'] = '  ' + str(int(float((self.t.get()))/float(self.dt.get()))) + ' steps  '
        except:
            pass
        finally:
            return True

    #To create all the default widgets
    def createDefaultWidgets(self):

        # Main titles
        self.mainTitle = Label(self.mainFrame, text='Main Parameters')
        self.mainTitle.config(font = ('',18))
        self.mainTitle.pack()
        separator = Frame(self.mainFrame,height=2, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        self.distTitleFrame = Frame(self.distFrame)
        self.distTitle = Label(self.distTitleFrame, text='Active Distributions')
        self.distTitle.config(font = ('',18))
        self.distTitle.pack()
        separator = Frame(self.distTitleFrame,height=2, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)
        self.distTitleFrame.pack()

        #dt Entry
        self.tFrame = Frame(self.mainFrame)
        self.dt_text = Label(self.tFrame, text = '  Step size')
        self.dt_text.pack(side=LEFT)
        register(self.dt_text,'Simulation time steps')
        self.dt_entry = Entry(self.tFrame, width = 8, textvariable=self.dt)
        self.dt_entry.pack(side=LEFT)

        # time entry
        self.t_text = Label(self.tFrame, text = '   Total time')
        self.t_text.pack(side=LEFT)
        register(self.t_text,'Total time steps simulated over')
        self.t_entry = Entry(self.tFrame, width = 8, textvariable=self.t, validate='all',validatecommand=lambda:self.update_steps(self.t))
        self.t_entry.pack(side=LEFT)

        self.steps_text = Label(self.tFrame, text='  ' + str(int(float((self.t.get()))/float(self.dt.get()))) + ' steps  ')
        self.steps_text.pack(side=LEFT)
        register(self.steps_text,'Number of time steps calculated')

        self.tFrame.pack()

        # G entry
        self.GFrame = Frame(self.mainFrame)
        self.G_text = Label(self.GFrame, text = 'Gravitational force constant')
        self.G_text.pack(side=LEFT)
        self.G_entry = Entry(self.GFrame, width = 5, textvariable=self.G)
        self.G_entry.pack(side=LEFT)
        self.GFrame.pack()

        # Sim parameters
        self.parFrame = Frame(self.mainFrame)
        self.theta_text = Label(self.parFrame, text = 'Approx parameter')
        self.theta_text.pack(side=LEFT)
        register(self.theta_text,'Bigger this is, the faster the simulation\nwill run, at the expense of accuracy.\nSetting to 0 will reduce to maximum calculations.')
        self.theta_entry = Entry(self.parFrame, width = 5, textvariable = self.theta)
        self.theta_entry.pack(side = LEFT)
        
        self.damp_text = Label(self.parFrame, text = '  Damping parameter')
        self.damp_text.pack(side=LEFT)
        register(self.damp_text,'Dampens the force at close range')
        self.damp_entry = Entry(self.parFrame, width = 5, textvariable = self.damp)
        self.damp_entry.pack(side = LEFT)
        self.parFrame.pack()

        # File name

        self.fileNameFrame = Frame(self.mainFrame)
        self.fileName_text = Label(self.fileNameFrame, text = 'File name')
        self.fileName_text.pack(side=LEFT)
        register(self.fileName_text,'The output file name to be used.\nDO NOT end the file in a number!')
        self.fileName_entry = Entry(self.fileNameFrame, width = 10, textvariable = self.fileName)
        self.fileName_entry.pack(side=LEFT)
        self.continueCheck = Checkbutton(self.fileNameFrame, text = 'Continue from file', variable=self.cont)
        self.continueCheck.pack(side=LEFT)
        self.fileNameFrame.pack()
        
        # Finish button
        self.finishFrame = Frame(self.mainFrame)
        self.finish = Button(self.finishFrame, text = 'Run', command=self.finish)
        self.finish.pack(side = LEFT)
        register(self.finish,'Run the simulation with current settings')
        self.genScript = Button(self.finishFrame, text = 'Create config file', command=self.createConfig)
        self.genScript.pack(side = RIGHT)
        register(self.genScript,'Saves the current settings to a config file to be run via scripting.')
        self.finishFrame.pack()

        
    # To create the distributions menu
    def createDistMenu(self):

        self.menuBar = Menu(self.master)
        self.distMenu = Menu(self.menuBar, tearoff = 0)
        self.menuBar.add_cascade(label = 'Distributions', menu = self.distMenu)
        for i in DISTRIBUTIONS:
            if i['name'] != None:
                self.distMenu.add_command(label=i['name'],command=partial(self.addDist,i['fname']))
        self.master.config(menu=self.menuBar)


    def addDist(self, distName):

        self.activeDist.append(distFrame(self.distFrame, distName))
        self.distFrame.pack()

    def resumeSim(self, fName):

        try:
            file = open(fName + '.barnes','rb')
        except:
            print('No file of that name')
            return
            
        j = 1
        n=1
        while True:
            try:
                n = int(fName[:-j])
                j+=1
            except:
                break
        length = ceil(log(n+0.01,10))
        data = pickle.load(file)
        data = data[-2:]
        dist = barnesdist_GUI.distributions(float(self.G.get()))
        dist.n = len(data[0])
        for i in range(0,len(data[0])):
            dist.part.append({
                'pos-1':vector(data[0][i][0],data[0][i][1],data[0][i][2]),
                'pos':vector(data[1][i][0],data[1][i][1],data[1][i][2]),
                'mass':data[0][i][3],
                'vel':vector(0,0,0),
                'acc':vector(0,0,0),
                'num':i
                })
        self.b = bh.BarnesHut(dist,
              float(self.dt.get()),
              float(self.t.get()),
              fName[:-length],
              float(self.G.get()),
              theta=float(self.theta.get()),
              damp=float(self.damp.get()),
              fileNo=n+1)
        

class distFrame(Frame):

    def __init__(self, master, distName):
        
        self.master = master
        Frame.__init__(self, self.master)

        separator = Frame(self,width=2, relief=SUNKEN)
        separator.pack(fill=Y, padx=5, pady=5, side=LEFT)

        self.distName = distName
        self.dist = eval(self.distName + '()')
        self.frameLabel = Label(self,text = self.dist.name)
        self.frameLabel.pack()

        self.subFrames = []

        for i in self.dist.parameters:
            self.subFrames.append(subFrame(self,i['pName'],i['pType'],i['default'],i['tooltip']))

        self.pack(side=LEFT)

        
class subFrame(Frame):

    def __init__(self, master, label, pType, default, tooltip):
        
        self.master = master
        Frame.__init__(self, self.master)
        self.pValue = StringVar()
        self.pValue.set(default)
        self.label = Label(self, text=label)
        self.label.pack(side=LEFT)
        if tooltip != None: 
            register(self.label,tooltip)

        if pType == 'numeric':
            self.entry = Entry(self, width = 8, textvariable = self.pValue)

        if pType == 'int':
            self.entry = Entry(self, width = 5, textvariable = self.pValue)

        if pType == 'vector':
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
