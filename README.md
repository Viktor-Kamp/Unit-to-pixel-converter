# Unit to pixel converter
I created this Add-On to be able to quickly calculate the needed render resolution from different units (like inch, centimeter or millimeter) inside Blender while taking PPI/DPI (pixel density) into account.

Since Blender 4.5, it is possible to set a value for "Pixel Density" to be present in the meta-data of the rendered image. "Unit to pixel converter" also dynamically changes that information according to the number you choose for PPI.

## Features
- Different Units: You can choose between metric and imperial measurements
- Pixel density: Calculates with PPI (Pixel per Inch)
- Bleed: Just put in the bleed, you use with your print layout. I hate calculating manually. That's the reason, this feature exists.
- Presets: Choose between commonly used paper formats

## Usage
You can interact with the Add-On in: "Properties > Output > Unit to pixel converter"

<img width="289" height="237" alt="Screenshot 2026-04-22 150002" src="https://github.com/user-attachments/assets/e65f513c-467a-4af8-8e34-035f61bfa410" />
