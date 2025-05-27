import damask

result = damask.Result('Singlecrystal_1_16x16x16_Load_Material_a.hdf5')
result.add_stress_Cauchy()   # computes σ from stored P and F
result.add_equivalent_Mises('sigma','stress')
result.add_strain()          # computes logarithmic strain ε_V^0.0(F) from F
result.add_equivalent_Mises('epsilon_V^0.0(F)','strain')
result.export_VTK(output=['F', 'F_e', 'F_p', 'sigma', 'epsilon_V^0.0(F)', 'xi_sl','sigma_vM','epsilon_V^0.0(F)_vM'], mode='cell')


import numpy as np

# Grid dimensions (manually known)
nx, ny, nz = 16, 16, 16

# Get last time step
timesteps = list(result.get('sigma_vM').keys())
last_step = timesteps[-1]

# Fields to extract
fields = ['sigma_vM', 'epsilon_V^0.0(F)_vM']

# Export voxel data to text
with open('damask_output_ascii.txt', 'w') as f:
    header = ['voxel_ID', 'x', 'y', 'z'] + fields
    f.write(' '.join(header) + '\n')

    for idx, (i, j, k) in enumerate(np.ndindex(nx, ny, nz)):
        line = [str(idx), str(i), str(j), str(k)]
        for field in fields:
            flat_data = result.get(field)[last_step]
            value = flat_data[idx]  # flat index access
            line.append(f"{value:.6e}")
        f.write(' '.join(line) + '\n')
        
        
# Load data, skipping the header
data = np.loadtxt('damask_output_ascii.txt', skiprows=1)

# Columns: voxel_ID, x, y, z, sigma_vM, epsilon_V^0.0(F)_vM
sigma_vM = data[:, 4]      # 5th column (0-indexed)
epsilon_vM = data[:, 5]    # 6th column

# Compute averages
avg_sigma_vM = np.mean(sigma_vM)
avg_epsilon_vM = np.mean(epsilon_vM)

# Print results
print(f"Average equivalent stress (von Mises): {avg_sigma_vM:.6e} Pa")
print(f"Average equivalent strain: {avg_epsilon_vM:.6e}")
