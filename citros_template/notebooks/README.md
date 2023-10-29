## Introduction

In each repository data obtained from simulations are stored in *batches*.
In the current repository 'gal_orbits', batch 'galactic orbits_1' contains the simulation results for the orbits of globular star cluster **NGC 6316**, 
calculated for 5 cases of slightly different masses of the Galaxy disk.

These notebooks aim to demonstrate the capabilities of the **citros_data_analysis package** and how it can be applied to real data.

## Batch format

The batch is a table that always contains the following columns:

||user\_id | sid | rid | time | topic | type| data |
|--|--|--|--|--|--|--|--|
|description |user name | simulation id| run id| ros time message | topic name| type name | json-format data|
|type| uuid | int | int | big int | str | str | jsonb|

The data column stores simulation data in a jsonb format. This can include json objects (the Python counterpart is the *dict* format) 
and json arrays (in Python, this corresponds to the *list* format)

## Simulation overview

The simulations were set to calculate the orbits, along with other dynamic and kinematic parameters, for five different values of 
the Galactic disk mass: 95, 97.5, 100, 102.5 and 105 billions of the Sun masses.

The output of the simulation is an array containing values for 11 variables for the next 200 million years:

0. t - time coordinate (in units of 10^7 years), 
1. R - distance from the galactic axis (in kpc), 
2. Vr - dR/dt, radial component of the velocity (in 100 km/s), 
3. fi - the position angle relative to Sun direction, counting clockwise if seen from North Galactic Pole (in radians), 
4. Vfi - R*d(fi)/dt, tangential velocity (in 100 km/s), 
5. z - vertical distance from the galactic plane (in kpc), 
6. Vz - dz/dt, vertical velocity (in 100 km/s), 
7. E - total energy (in (100 km/s)^2), 
8. C - angular momentum (in 100 kpc*km/s), 
9. xg - R*cos(fi), X galactocentric coordinates (in kpc), 
10. yg - R*sin(fi), Y galactocentric coordinates (in kpc)

For convenience, these variables are enumerated starting from 0, consistent with Python's convention where arrays and lists are indexed from 0.

In the database these values are stored in 'data' column as a json array (*list*) under the key 'data', like:

|data|
|--|
|{data: [0, 1.1, 13.2, ...]}|
|{data: [0.1, 4.5, 3.7, ...]}|
|...|