from wbcommand import *
import pyoptools.raytrace.comp_lib as comp_lib
import pyoptools.raytrace.mat_lib as matlib
from sphericallens import buildlens
from math import radians

class DoubletLensGUI(WBCommandGUI):
    def __init__(self):
        WBCommandGUI.__init__(self, 'DoubletLens.ui')


        self.form.Catalog1.addItem("Value",[])
        self.form.Catalog2.addItem("Value",[])
        for i in matlib.material.liblist:
            self.form.Catalog1.addItem(i[0],sorted(i[1].keys()))
            self.form.Catalog2.addItem(i[0],sorted(i[1].keys()))
        self.form.Catalog1.currentIndexChanged.connect(self.catalog1Change)
        self.form.Catalog2.currentIndexChanged.connect(self.catalog2Change)
        self.form.ILD.valueChanged.connect(self.ILDChange)
        self.form.CS2_1.valueChanged.connect(self.CS2_1Change)

    def catalog1Change(self,*args):
        if args[0] == 0:
            self.form.Value1.setEnabled(True)
        else:
            self.form.Value1.setEnabled(False)


        while self.form.Reference1.count():
            self.form.Reference1.removeItem(0)
        self.form.Reference1.addItems(self.form.Catalog1.itemData(args[0]))

    def catalog2Change(self,*args):
        if args[0] == 0:
            self.form.Value2.setEnabled(True)
        else:
            self.form.Value2.setEnabled(False)


        while self.form.Reference2.count():
            self.form.Reference2.removeItem(0)
        self.form.Reference2.addItems(self.form.Catalog2.itemData(args[0]))

    def ILDChange(self,*args):
        d=args[0]
        if d==0.0:
            self.form.CS1_2.setValue(self.form.CS2_1.value())
            self.form.CS1_2.setEnabled(False)
        else:
            self.form.CS1_2.setEnabled(True)
    def CS2_1Change(self,*args):
        d=args[0]
        if not self.form.CS1_2.isEnabled():
            self.form.CS1_2.setValue(d)

    def accept(self):

        CS1_1=self.form.CS1_1.value()
        CS1_2=self.form.CS1_2.value()
        CS2_1=self.form.CS2_1.value()
        CS2_2=self.form.CS2_2.value()
        CT_1=self.form.CT1.value()
        CT_2=self.form.CT2.value()

        D=self.form.D.value()
        ILD = self.form.ILD.value()

        X=self.form.Xpos.value()
        Y=self.form.Ypos.value()
        Z=self.form.Zpos.value()
        Xrot=self.form.Xrot.value()
        Yrot=self.form.Yrot.value()
        Zrot=self.form.Zrot.value()


        matcat1=self.form.Catalog1.currentText()
        if matcat1=="Value":
            matref1=str(self.form.Value1.value())
        else:
            matref1=self.form.Reference1.currentText()



        matcat2=self.form.Catalog2.currentText()
        if matcat2=="Value":
            matref2=str(self.form.Value2.value())
        else:
            matref2=self.form.Reference2.currentText()


        obj=InsertDL(CS1_1,CS2_1,CT_1,CS1_2,CS2_2,CT_2,D,ILD,
                     "L",matcat1,matref1,matcat2, matref2)

        m=FreeCAD.Matrix()
        m.rotateX(radians(Xrot))
        m.rotateY(radians(Yrot))
        m.rotateZ(radians(Zrot))
        m.move((X,Y,Z))
        p1 = FreeCAD.Placement(m)
        obj.Placement = p1

        FreeCADGui.Control.closeDialog()


class DoubletLensMenu(WBCommandMenu):
    def __init__(self):
        WBCommandMenu.__init__(self,DoubletLensGUI)

    def GetResources(self):
        return {"MenuText": "Doublet Lens",
                #"Accel": "Ctrl+M",
                "ToolTip": "Add Doublet Lens",
                "Pixmap": ""}

class DoubletLensPart(WBPart):
    def __init__(self,obj,CS1_1,CS2_1,CT_1,CS1_2,CS2_2,CT_2,D,ILD,
                     matcat1,matref1,matcat2,matref2):

        WBPart.__init__(self,obj,"DoubletLens")
        obj.Proxy = self
        
        obj.addProperty("App::PropertyPrecision","CS1_1","Shape lens 1",
                        "Curvature surface 1").CS1_1=(0,-10,10,1e-3)
        obj.addProperty("App::PropertyPrecision","CS2_1","Shape lens 1",
                        "Curvature surface 2").CS2_1=(0,-10,10,1e-3)

        obj.addProperty("App::PropertyLength","Thk_1","Shape lens 1",
                        "Lens 1 center thickness")

        obj.addProperty("App::PropertyPrecision","CS1_2","Shape lens 2",
                        "Curvature surface 1").CS1_2=(0,-10,10,1e-3)
        obj.addProperty("App::PropertyPrecision","CS2_2","Shape lens 2",
                        "Curvature surface 2").CS2_2=(0,-10,10,1e-3)

        obj.addProperty("App::PropertyLength","Thk_2","Shape lens 2",
                        "Lens 2 center thickness")

        obj.addProperty("App::PropertyLength","D","Global","Diameter")
        obj.addProperty("App::PropertyLength","ILD","Global","Interlens distance")

        obj.addProperty("App::PropertyString","matcat1","Material lens 1","Material catalog")
        obj.addProperty("App::PropertyString","matref1","Material lens 1","Material reference")

        obj.addProperty("App::PropertyString","matcat2","Material lens 2","Material catalog")
        obj.addProperty("App::PropertyString","matref2","Material lens 2","Material reference")

        obj.CS1_1 = CS1_1
        obj.CS2_1 = CS2_1
        obj.Thk_1 = CT_1

        obj.CS1_2 = CS1_2
        obj.CS2_2 = CS2_2
        obj.Thk_2 = CT_2

        obj.D = D
        obj.ILD = ILD

        obj.matcat1=matcat1
        obj.matref1=matref1

        obj.matcat2=matcat2
        obj.matref2=matref2

        obj.ViewObject.Transparency = 50
        obj.ViewObject.ShapeColor = (1.,1.,0.,0.)


    def pyoptools_repr(self,obj):
        matcat1=obj.matcat1
        matref1=obj.matref1
        if matcat1=="Value":
            material1=float(matref1.replace(",","."))
        else:
            material1=getattr(matlib.material,matcat1)[matref1]


        matcat2=obj.matcat2
        matref2=obj.matref2
        if matcat2=="Value":
            material2=float(matref2.replace(",","."))
        else:
            material2=getattr(matlib.material,matcat2)[matref2]

        if obj.ILD.Value==0:
            radius = obj.D.Value/2.
            curv_s1 = obj.CS1_1
            curv_s2 = obj.CS2_1
            curv_s3 = obj.CS2_2
            th1 = obj.Thk_1.Value
            th2 = obj.Thk_2.Value
            db=comp_lib.Doublet(radius, curv_s1,curv_s2,curv_s3,th1,th2,material1,material2)
        else:
            radius = obj.D.Value/2.
            curv_s1 = obj.CS1_1
            curv_s2 = obj.CS2_1
            curv_s3 = obj.CS1_2
            curv_s4 = obj.CS2_2


            th1= obj.Thk_1.Value
            th2=obj.Thk_2.Value

            ag=obj.ILD.Value
            db = comp_lib.AirSpacedDoublet(radius,curv_s1,curv_s2,curv_s3,curv_s4,th1,
                                  ag,th2,material1,material2)

        return db


    def execute(self,obj):

        #Todo: Verificat las restricciones por construccion cuando se cambian
        # los parametros a mano

        L1 = buildlens(obj.CS1_1, obj.CS2_1, obj.D.Value, obj.Thk_1.Value)
        L2 = buildlens(obj.CS1_2, obj.CS2_2, obj.D.Value, obj.Thk_2.Value)
        TT=obj.Thk_1.Value+obj.Thk_2.Value+obj.ILD.Value
        L1.translate(FreeCAD.Base.Vector(0,0,-TT/2.+obj.Thk_1.Value/2.))
        L2.translate(FreeCAD.Base.Vector(0,0,TT/2.-obj.Thk_2.Value/2.))
        obj.Shape = L1.fuse(L2)

def InsertDL(CS1_1,CS2_1,CT_1,CS1_2,CS2_2,CT_2,D,ILD,
                     ID,matcat1,matref1,matcat2,matref2):

    myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",ID)
    DoubletLensPart(myObj,CS1_1,CS2_1,CT_1,CS1_2,CS2_2,CT_2,D,ILD,
                    matcat1,matref1,matcat2,matref2)
    myObj.ViewObject.Proxy = 0 # this is mandatory unless we code the ViewProvider too
    FreeCAD.ActiveDocument.recompute()
    return myObj
