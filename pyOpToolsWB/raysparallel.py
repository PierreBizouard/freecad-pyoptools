# -*- coding: utf-8 -*-
from wbcommand import *
from pyoptools.misc.pmisc.misc import wavelength2RGB
import pyoptools.raytrace.ray.ray_source as rs_lib
from Units import Quantity
from math import radians

class RaysParallelGUI(WBCommandGUI):
    def __init__(self):
        WBCommandGUI.__init__(self, 'RaysParallel.ui')

    def accept(self):

        X=self.form.Ox.value()
        Y=self.form.Oy.value()
        Z=self.form.Oz.value()

        Xrot = self.form.Xrot.value()
        Yrot = self.form.Yrot.value()
        Zrot = self.form.Zrot.value()



        nr = self.form.nr.value()
        na = self.form.na.value()
        distribution = self.form.RayDistribution.currentText()
        wavelenght = self.form.wavelenght.value()
        enabled = self.form.Enabled.isChecked()

        D = self.form.D.value()
        m=FreeCAD.Matrix()

        m.rotateX(radians(Xrot))
        m.rotateY(radians(Yrot))
        m.rotateZ(radians(Zrot))

        m.move((X,Y,Z))
        obj=InsertRPar(nr,na, distribution,wavelenght,D,"S",enabled)

        p1 = FreeCAD.Placement(m)
        obj.Placement = p1
        FreeCADGui.Control.closeDialog()

class RaysParallelMenu(WBCommandMenu):
    def __init__(self):
        WBCommandMenu.__init__(self, RaysParallelGUI)

    def GetResources(self):
        return {"MenuText": "Add Parallel Ray Source",
                #"Accel": "Ctrl+M",
                "ToolTip": "Add Parallel Ray Source",
                "Pixmap": ""}





class RaysParPart(WBPart):
    def __init__(self,obj,nr=6,na=6,distribution="polar",wavelenght=633, D=5,enabled=True):
        WBPart.__init__(self,obj,"RaysPar",enabled)

        obj.addProperty("App::PropertyIntegerConstraint","nr","Shape","Number of rays (radial)").nr=(0,0,10000,1)
        obj.addProperty("App::PropertyIntegerConstraint","na","Shape","Number of rays (angular)").na=(0,0,10000,1)
        obj.addProperty("App::PropertyString","distribution","Options","Ray distribution (Polar for the moment)")
        obj.addProperty("App::PropertyLength","wl","Options","Wavelength of the source")
        obj.addProperty("App::PropertyLength","D","Shape","Ray Source Diameter")
        #obj.addProperty("App::PropertyVector","axis","","Direction of propagation")

        obj.nr=nr
        obj.na=na
        obj.distribution=distribution.lower()
        obj.wl = Quantity("{} nm".format(wavelenght)) # wavelenght is received in nm

        obj.D = D
        obj.enabled=enabled
        r,g,b = wavelength2RGB(obj.wl.getValueAs("µm").Value)



        obj.ViewObject.ShapeColor = (r,g,b,0.)



    def propertyChanged(self, obj, prop):

        # To keep all the housekeeping that WBPart do, this method replaces
        # the standard onChanged

        if prop == "wl":
            r,g,b = wavelength2RGB(obj.wl.getValueAs("µm").Value)
            obj.ViewObject.ShapeColor = (r,g,b,0.)



    def pyoptools_repr(self,obj):
        X,Y,Z = obj.Placement.Base
        RZ,RY,RX = obj.Placement.Rotation.toEuler()
        dist=obj.distribution
        nr=obj.nr
        na=obj.na
        wl=obj.wl.getValueAs("µm").Value
        R=obj.D/2.
        r=[]
        if obj.enabled:
            if dist=="polar":
                r=rs_lib.parallel_beam_p(origin=(X,Y,Z),direction=(radians(RX),radians(RY),radians(RZ)),
                                         radius=R, num_rays=(nr,na),wavelength=wl,
                                         label="")
            elif dist=="cartesian":
                print "cartesian ray distribution, not implemented yet"
            elif dist=="random":
                print "random ray distribution, not implemented yet"
            else:
                print "Warning ray distribution {} not recognized".format(dist)
        return r


    def execute(self,obj):
        import Part,FreeCAD

        dist = obj.distribution.lower()


        if dist not in ["polar","cartesian"]:
            obj.distribution="polar"
            print "Ray Distribution not understood, changing it to polar"

        if dist == "polar":
            r=obj.D.Value/2.
            d=Part.makeCylinder(r,5)
            #d.translate(FreeCAD.Base.Vector(0,0,-0.5))
        else: #Cartesian
            #Todo: Crear una piramide en lugar de un cono
            d=Part.makeCone(0,10,10,dir)
            d.translate(FreeCAD.Base.Vector(0,0,-0.5))
        obj.Shape = d



def InsertRPar(nr=6, na=6,distribution="polar",wavelenght=633,D=5,ID="S",enabled = True):
    import FreeCAD
    myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",ID)
    RaysParPart(myObj,nr,na,distribution,wavelenght,D,enabled)
    myObj.ViewObject.Proxy = 0 # this is mandatory unless we code the ViewProvider too
    FreeCAD.ActiveDocument.recompute()
    return myObj
