# vtk_tools 

This package provides useful utilities for working with vtk output files. It's current focus is on handling tasks related to cell ordering and underlying shape functions for different cell types to facilitate adding new element types to *yt*. Depending on development, it may make sense to add this functionality directly to *yt* rather than maintaining a second package.

Note that a major limitation at present is that the package's shape function methods are limited to VTK cell type 72, see [Issue 1](https://github.com/data-exp-lab/vtk_tools/issues/1). 

## installation 

none yet.... 

## requirements 

While `setup.py` (doesn't exist yet) contains requirements, it is important to stress that this package requires vtk version of `9.0.1` or later. At present, the latest vtk version on conda is 8.2, so if you already have installed vtk from conda (or from source), you will need to upgrade. The easiest way is to use pip: 

`pip install vtk`

If you already have a vtk version installed, you can try `pip install vtk -upgrade` but this will likely fail if the previous version of vtk was not installed with pip, in which case the previous version must be uninstalled frist. 

Also, note that while this package requires vtk `9.0.1` or later, it can process output that was created with lower vtk versions.

## example usage

### accessing underlying `vtk` cell methods

`vtk_tools.vtk_tools.init_vtk_cell` instantiates a `vtk` cell by cell type name or ID, without having to know the full `vtk` class name: 

```
>>> from vtk_tools.vtk_tools import init_vtk_cell
>>> v_cell_72,_ = init_vtk_cell(72)
>>> print(type(v_cell_72))
<class 'vtkmodules.vtkCommonDataModel.vtkLagrangeHexahedron'>
>>> 
>>> v_cell_28,_ = init_vtk_cell(28)
>>> print(type(v_cell_28))
<class 'vtkmodules.vtkCommonDataModel.vtkBiQuadraticQuad'>
```
The cell objects, `v_cell_72` and `v_cell_28` are instances of python `vtk` objects, with all the associated methods and attributes. 

### shape function mapping 

To build a shape function mapping for a lagrange hexahedron, use  `vtk_tools.shapefunctions(72,order)` where order is the element order. E.g., a first order element: 

```
>>> import vtk_tools.shapefunctions as sfs
>>> sf_72_O1 = sfs.sf(72,1)
```
The two most useful attributes are the `node_order_hash` and `shape_functions` attributes. The `node_order_hash` is a dictionary mapping from VTK node ordering convention to ijk ordering. In this case we have 8 entries corresponding to the hexahedral vertices:

```
>>> print(sf_72_O1.node_order_hash)
{0: 0, 4: 1, 3: 2, 7: 3, 1: 4, 5: 5, 2: 6, 6: 7}
```

The corresponding shape functions are 

```
>>> print(sf_72_O1.shape_functions)
[-0.125*(x - 1)*(y - 1)*(z - 1), 0.125*(x - 1)*(y - 1)*(z + 1), 0.125*(x - 1)*(y + 1)*(z - 1), -0.125*(x - 1)*(y + 1)*(z + 1), 0.125*(x + 1)*(y - 1)*(z - 1), -0.125*(x + 1)*(y - 1)*(z + 1), -0.125*(x + 1)*(y + 1)*(z - 1), 0.125*(x + 1)*(y + 1)*(z + 1)]
```
The shape functions can be appended to a yaml file with

```
>>> sf_72_O1.write_yaml('testyaml.yaml','a','test_hex8','hex8')
```

The default yaml formatting follows that used by *yt*'s mesh generator configuration file, `yt/utilities/mesh_types.yaml`.
