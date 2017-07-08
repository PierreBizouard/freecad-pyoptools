import FreeCAD, Part

from math import radians
from wbcommand import *


from pyoptools.raytrace.system import System

from pyoptools.misc.pmisc.misc import wavelength2RGB

class PropagateMenu:
    def __init__(self):
        #Esta no tiene GUI, no necesitamos heredar de WBCommandMenu
        #WBCommandMenu.__init__(self,None)
        pass

    def GetResources(self):
        return {"MenuText": "Propagate",
                #"Accel": "Ctrl+M",
                "ToolTip": "Propagate Rays",
                "Pixmap": ""}

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True

    def Activated(self):

        myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","PROP")
        PP=PropagatePart(myObj)
        myObj.ViewObject.Proxy = 0


        doc=FreeCAD.activeDocument()

        #Se agrupan los rayos para poder eliminarlos facil
        grp=doc.addObject("App::DocumentObjectGroup", "Rays")
        for ray in PP.S.prop_ray:
            #lines = Part.Wire(get_prop_shape(ray))
            lines = get_prop_shape(ray)
            wl=ray.wavelength

            myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Ray")
            myObj.Shape=lines
            r,g,b = wavelength2RGB(wl)
            myObj.ViewObject.LineColor = (r,g,b,0.)
            myObj.ViewObject.Proxy = 0
            grp.addObject(myObj)
        FreeCAD.ActiveDocument.recompute()




        FreeCAD.ActiveDocument.recompute()

def get_prop_shape(ray):
    P1 = FreeCAD.Base.Vector(tuple(ray.pos))
    if len(ray.childs)>0:
        P2=FreeCAD.Base.Vector(tuple(ray.childs[0].pos))
    else:
        P2 = FreeCAD.Base.Vector(tuple(ray.pos + 10. * ray.dir))

    L1 = Part.makeLine(P1,P2)

    for i in ray.childs:
        L1=L1.fuse(get_prop_shape(i))

    return L1

class PropagatePart(WBPart):
    def __init__(self, obj):
        WBPart.__init__(self,obj,"Propagation")
        objs = FreeCAD.ActiveDocument.Objects
        rays=[]
        complist=[]
        for obj in objs:
            if not obj.enabled:
                continue
            X,Y,Z = obj.Placement.Base
            #No entiendo el orden pero parece que funciona
            RZ,RY,RX = obj.Placement.Rotation.toEuler()

            # Hay que buscar una mejor forma de hacer esto, es decir como no tener
            # que pasar obj en los parametros
            e=obj.Proxy.pyoptools_repr(obj)
            if isinstance(e,list):
                rays.extend(e)
            else:
                complist.append((e,(X,Y,Z),(radians(RX),radians(RY),radians(RZ)),obj.Label))

        self.S=System(complist)
        self.S.ray_add(rays)
        self.S.propagate()

    def execute(self,obj):
        pass

    def pyoptools_repr(self,obj):
        # Solo para que no se estrelle
        return []