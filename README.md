<img src="Asset Extractor Banner.png" width="100%">

### A lightweight **Minecraft mod data extractor** that scans mod **JAR files** and extracts useful asset IDs such as **items, blocks, biomes, structures, and entities**.
### These IDs can then be used directly in **Minecraft commands or mod development workflows**.

---

## ✨ Features

* 📦 Extract **item IDs** from mod JAR files
* 🧱 Extract **block IDs**
* 🌍 Extract **biome IDs**
* 🏛 Extract **structure IDs**
* 👾 Extract **entity IDs**
* 🖼 Extract **item textures (PNG files)**
* 📂 Automatically creates **numbered extraction folders** (`Extract_1`, `Extract_2`, etc.)

---

## 📄 Output Format

All IDs are exported using the standard Minecraft namespace format:

```
modid:item_name
```

### Example

```
mutantmonsters:creeper_shard
create:cogwheel
terralith:marble
```

---

## 🚀 Usage

1. Install **Python 3.x**
2. Run the extractor:

```
python minecraft_mod_extractor.py
```

3. Choose what you want to extract:

   * Items
   * Blocks
   * Biomes
   * Structures
   * Entities
   * Textures

4. Select your **mod JAR files**

5. Check the **`Extract` folder** for the generated files.

---

## 📁 Output Files

| File                   | Description                       |
| ---------------------- | --------------------------------- |
| `items.txt`            | All extracted item IDs            |
| `blocks.txt`           | All extracted block IDs           |
| `all_items_blocks.txt` | Combined list of items and blocks |
| `biomes.txt`           | All biome IDs                     |
| `structures.txt`       | All structure IDs                 |
| `entities.txt`         | All entity IDs                    |
| `Extracted_PNGs/`      | Extracted item textures           |

---

## 🎮 Example Minecraft Commands

```
/give @p mutantmonsters:creeper_shard
/locate biome terralith:volcanic_peaks
/locate structure terralith:ancient_ruins
/summon alexsmobs:bone_serpent
```

---

## ⚙️ Requirements

* **Python 3.x**
* **Tkinter** (included with most Python installations)

---

## 📜 License

This project is released under the **MIT License**.

---

## ⚠️ Disclaimer

```
This project is an independent fan-made creation and is not affiliated with,
endorsed by, or connected to Mojang Studios or Minecraft in any way.

Please do not report bugs, issues, or problems related to this project
to Mojang or the Minecraft support team.

Any feedback, bug reports, or questions should be directed only to the
developer of this project.
```

---

<h1 align="center">Made with 🖤 by <b>RK Studios</b></h1>
