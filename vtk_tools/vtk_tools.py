import vtk
from .vtk_cell_support import vtk_cell_hash

def listCells():
    for ID,vals in vtk_cell_hash.items():
        print(f"{vals['vtk_type']} : {ID}")
        
def init_vtk_cell(vtk_type):
    """initializes a vtk cell of a given type. 

    Parameters
    ----------
    vtk_type : int or str
        either the VTK ID or the VTK cell type name

    Returns
    -------
    vtk class : 
        a new instance of a vtk class of type vtk_type 

    To instantiate a 27 node lagrange hexahedron (VTK type 72): 
    
    >>> from vtk_tools.vtk_tools import init_vtk_cell
    >>> new_cell = init_vtk_cell('VTK_LAGRANGE_HEXAHEDRON')
    >>> type(new_cell)
    <class 'vtkmodules.vtkCommonDataModel.vtkLagrangeHexahedron'>

    Or 
        
    >> new_cell = init_vtk_cell(72)
    >>> type(new_cell)
    <class 'vtkmodules.vtkCommonDataModel.vtkLagrangeHexahedron'>
    
    The new instance can access all of the vtk methods associated with that cell. 
    """
    
    if isinstance(vtk_type,str):
        if hasattr(vtk,vtk_type):
            vtk_type = getattr(vtk,vtk_type)
        else:
            raise ValueError(f"vtk_type {vtk_type} does not exist.")
        
    if isinstance(vtk_type,int) and vtk_type in vtk_cell_hash.keys():
        cell_info = vtk_cell_hash[vtk_type]
        return getattr(vtk,cell_info['vtk_class'])(), vtk_type
    else:
        raise ValueError(f"vtk_type {vtk_type} is not a valid vtk type.")
    
def require_vtk_min_version(version='9.0.1'):
    Major = vtk.vtkVersion.GetVTKMajorVersion()
    Minor = vtk.vtkVersion.GetVTKMinorVersion()
    
    if Major >= int(version.split('.')[0]):
        if Minor >= int(version.split('.')[1]): 
            return 
            
    vtkver = vtk.vtkVersion.GetVTKSourceVersion()    
    raise ModuleNotFoundError((
        f"vtk version >= 9.0.1 required, but you have {vtkver}."
        " To upgrade to the latest vtk version, try 'pip install vtk --upgrade' ."
        " If you did not use pip to install vtk initially, you will likely need to " 
        " uninstall your existing vtk package first."
    ))    

# https://vtk.org/doc/nightly/html/vtkCellType_8h_source.html        
# https://vtk.org/doc/nightly/html/vtkCellType_8h.html
