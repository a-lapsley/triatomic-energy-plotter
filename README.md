# Exercise 2: Triatomic energy plotter
Program to plot energies of specific triatomic molecules as a function of their geometry and find their equillibrium geometry, and find vibration frequencies of their symmetric stretching and bending modes for Part II Chemistry Programming Practical Exercise 2.

## Available data input modes
* `local`    Input data from local files stored within the `\outfiles` subdirectory within the program folder. Individual `.out` files should be stored within a subfolder named `[molecule]outfiles` where `[molecule]` is the name of the molecule, e.g. `H2O`.
  
  The data input files should be named `[molecule].r[r]theta[theta].out` where `[molecule]` is the name of the molecule, `[r]` is the bond length (in Angstroms) and `[theta]` is the bond angle (in degrees). For example, `H2O.r0.70theta70.0.out`.

* `web`     Retrieve data from URL. The URL entered should be for the directory containing the individual `.out` files. For example, `https://gitlab.developers.cam.ac.uk/ch/thom/part2programming/-/raw/master/Ex2/H2Ooutfiles`. 

  The data input files should be named `[molecule].r[r]theta[theta].out` where `[molecule]` is the name of the molecule, `[r]` is the bond length (in Angstroms) and `[theta]` is the bond angle (in degrees). For example, `H2O.r0.70theta70.0.out`.]

## config.json
The parameters for this program can be configured by editing the `config.json` file.
* `r_min`       Start value of `r` to retrieve data input file for.
* `r_max`       End value of `r` to retrieve data input file for.
* `r_step`      Increment in which `r` increases between data input files.
* `theta_min`   Start value of `theta` to retrieve data input file for.
* `theta_max`   End value of `theta` to retrieve data input file for.
* `theta_step`  Increment in which `theta` increases between data input files.
* `e_min`       Lower limit of z-axis (energy) for 3D plot
* `e_max`       Upper limit of z-axis (energy) for 3D plot
* `r_fit_range` Number of data points either side of equillibrium `r` value to fit quadratic along potential energy curve with varying `r`
* `plor_r_fit`  If set to `true` displays a plot of the potential energy curve with varying `r` and the quadratic fit around the equillibrium value.
* `t_fit_range` Number of data points either side of equillibrium `theta` value to fit quadratic along potential energy curve with varying `theta`
* `plor_r_fit`  If set to `true` displays a plot of the potential energy curve with varying `theta` and the quadratic fit around the equillibrium value.