# WAVEDER reader vs PS p–r (CO2)

- Reader: NB=24, NB_CDER=16, max|CDER|=2.169e+01
- Occ→virt pairs with both |r|≥0.05 Å: **11**
- Median |r_PS−r_CDER|/max (informational): **1.0000008658715656**
- Pass (decode + ≥3 both-significant): **True**

Do **not** cite PS `get_dipole_mat` as WAVEDER-parity. Use WAVEDER as the VASP length-gauge reference; PS path remains L2-partial via optics selection rules (`ref/l2_table.md`).
