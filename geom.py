import damask
import numpy as np
size = np.ones(3)*5e-5
cells = [16,16,16]
N_grains = 1
seeds = damask.seeds.from_random(size,N_grains,cells)
grid = damask.GeomGrid.from_Voronoi_tessellation(cells,size,seeds)
# grid.save(f'Polycrystal_{N_grains}_{cells[0]}x{cells[1]}x{cells[2]}')
grid.save(f'Singlecrystal_{N_grains}_{cells[0]}x{cells[1]}x{cells[2]}')
grid