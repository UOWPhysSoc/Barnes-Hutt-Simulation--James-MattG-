from .vector import *

class exampleDist:  # MAKE SURE TO CHANGE THIS! AND ADD THE SAME FUNCTION
                   # NAME TO BARNESDIST_GUI.PY AND __INIT__.PY  

    def __init__(self):

        # Text name goes here. 'None' emmits from being imported
        self.name = None
        #self.name = 'Distribution name as string'
        # Parameters imported to GUI to be entered. Leave the dict names,
        # but the entries can be changed. Currently 'pType' can be:
            # numeric, vector, int.
        self.parameters = [
            {'pName':'Mass 1', 'pType':'numeric', 'default':1, 'tooltip':},
            {'pName':'Centre', 'pType':'vector', 'default':vector(0,0,0), 'tooltip':'Initial position of the central mass'},
            {'pName':'Net velocity','pType':'vector','default':vector(0,0,0),'tooltip':'Initial net velocity of group.\nOnly important for relative velocity\nbetween different distributions as\nthe total momentum is set to zero.'},
            {'pName':, 'pType':, 'default':, 'tooltip':}

    def run(self, imports, dist, G):

        # Only thing to change here is the imports. It should be the
        # self.parameters stuff as a list, in the same order. Values will
        # be Stringvar() so they need explicit conversion to correct type.

        # All changes are to the dist dictionary. Example format below.
        # You MUST do dist.n += n for the number of masses in the current dist,
        # and the dist.index must be incremented (AFTER adding the mass) for each mass so all the
        # masses in the master dist list have a unique index.

        dist.n += n

        dist.part.append({
            'pos-1':r1,
            'pos':r1,
            'mass':mass1,
            'vel':sqrt(mass2**2/(mag(r)*(mass1 + mass2))) * vector(0,1,0),
            'acc':vector(0,0,0),
            'num':dist.index
            })
        dist.index += 1

        
