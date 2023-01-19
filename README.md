# PhysMedGUI
This GUI was designed as a complementary tool for the teaching of an undergraduate level class of Medical Physics, as given at the Université de Montréal (Canada).

It consists of different modules, each available through a tab at the top of the GUI. 

This documentation is also available to read in the ReadMe tab at the top of the GUI.

A short description of each module will here be listed, in the order that they appear at the top of the GUI.

## Photon Beam Attenuation (PBA) Tab

This part shows the principle of photon beam attenuation. 

Three images are present:
- A distribution of the photon spectrum;
- A graphical distribution of the attenuation coefficients, as available on NIST's XCOM;
- A total attenuation, as a function of the penetrated depth, with the HVL and TVL depths indicated by dashed lines.

Many options are available to the user to change the views of the different graphs:

- Under the uppermost image is a slider that allows to change the depth penetrated by the beam. When modified, this will change the distribution of the beam and there will be an indicator in the lower right image, showing where the specific depth is located. For a value not encompassed by the slider, it can be manually added, in the small box to the right of the slider. The slider will not move, but the depth will be used. Note that if the value entered is greater than the "Max Depth" value, the bottom right image will not show the depth, as it will exceed the bounds;
- A selection box allows to choose the attenuating material. When changed, this will modify the bottom two graphs. The XCOM data will be updated;
- A selection box for the type of specter. This will modify the image of the spectrum and the depth of penetration graph. Note that the "Bump" spectrum is fixeds;
- The "Min.", "Max.", "In. Value", and "Factor" values change the form of the spectrum. The minimum value is the minimal energy for which the graph is defined. Similarly, the maximum value is the maximal value. For the "Peak" spectrum, only the minimal value is used. The initial value represents the value of the spectrum at the minimal energy value. The factor gives the shape of the curve, mainly for the exponential function. Note that the "Min." and "Max" values show dashed lines on the XCOM data, to indicate where the energy window is located;
- The "Max Depth" value gives the maximal depth available through the depth slider and seen on the depth-attenuation graph at the bottom right;
- The "Norm." button normalizes the spectrum and the total attenuation curve. This can be combined with the "Sup." and "Avg." buttons;
- The "Sup." button overlaps the original spectrum in the upper left image. This allows to easily see the principle of beam hardening. This can be combined with the "Norm." and "Avg." buttons;
- The "Avg." button shows graphically the average energy of the beam, at the top left image. This can be combined with the "Norm." and "Sup." buttons;
- The "Save" button allows to store a spectrum curve in memory;
- The "Clear" button clears the memory of spectra;
- The "Show" button shows the saved curves in the top left image. This allows to easily compare spectra of different types, material and energies in a single image. Normalization is considered if selected, but not "Sup." and "Avg." options.

## TBA

Future tabs

## ReadMe Tab
ReadMe documentation, i.e. this document.