## Unit to pixel converter
I created this Add-On to be able to quickly calculate the needed render resolution from different units (like inch, centimeter or millimeter) inside Blender while taking PPI/DPI (pixel density) into account.

Since Blender 4.5, it is possible to set a value for "Pixel Density" to be present in the meta-data of the rendered image. "Unit to pixel converter" also dynamically changes that information according to the number you choose for PPI.

### Features
- Different Units: You can choose between metric and imperial measurements
- Pixel density: Calculates with PPI (Pixel per Inch)
- Bleed: Just put in the bleed, you use with your print layout. I hate calculating manually. That's the reason, this feature exists.
- Presets: Choose between commonly used paper formats
- Compatibility: Compatible since Blender 4.2 until latest

### Usage
You can interact with the Add-On in: "Properties > Output > Unit to pixel converter"

<img width="1898" height="1068" alt="utp-Bild" src="https://github.com/user-attachments/assets/f2eeb369-6871-43f9-b348-0c6d5e8055c7" />
