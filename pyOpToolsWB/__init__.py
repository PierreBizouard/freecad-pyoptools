import FreeCADGui

from sphericallens import SphericalLensMenu
FreeCADGui.addCommand('SphericalLens',SphericalLensMenu())

from roundmirror import RoundMirrorMenu
FreeCADGui.addCommand('RoundMirror',RoundMirrorMenu())

from rectmirror import RectMirrorMenu
FreeCADGui.addCommand('RectangularMirror',RectMirrorMenu())

from rayspoint import RaysPointMenu
FreeCADGui.addCommand('RaysPoint',RaysPointMenu())

from raysparallel import RaysParallelMenu
FreeCADGui.addCommand('RaysParallel',RaysParallelMenu())

from raysarray import RaysArrayMenu
FreeCADGui.addCommand('RaysArray',RaysArrayMenu())

from propagate import PropagateMenu
FreeCADGui.addCommand('Propagate',PropagateMenu())

from catalogcomponent import CatalogComponentMenu
FreeCADGui.addCommand('CatalogComponent',CatalogComponentMenu())

from sensor import SensorMenu
FreeCADGui.addCommand('Sensor',SensorMenu())

from reports import ReportsMenu
FreeCADGui.addCommand('Reports',ReportsMenu())

from doubletlens import DoubletLensMenu
FreeCADGui.addCommand('DoubletLens',DoubletLensMenu())

from optimize import OptimizeMenu
FreeCADGui.addCommand('Optimize',OptimizeMenu())
