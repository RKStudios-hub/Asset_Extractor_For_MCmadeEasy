<img src="Asset Extractor Banner.png" width="100%">

<h1 align="center">🧩 Asset Extractor for MCmadeEasy</h1>

<p align="center">
A lightweight <b>Minecraft mod data extractor</b> that scans mod <b>JAR files</b> and extracts useful asset IDs such as <b>items, blocks, biomes, structures, and entities</b>.
</p>

<p align="center">
These IDs can be used directly in <b>Minecraft commands</b> or <b>mod development workflows</b>.
</p>

---

<p align="center">

<a href="https://github.com/RKStudios-hub/Asset_Extractor_For_MCmadeEasy/releases/tag/v1.0">
<img src="https://img.shields.io/badge/⬇ Download-Latest%20Release-brightgreen?style=for-the-badge">
</a>

<a href="https://github.com/RKStudios-hub/Asset_Extractor_For_MCmadeEasy">
<img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github">
</a>

</p>

---

# ✨ Features

| Icon | Feature                                               |
| ---- | ----------------------------------------------------- |
| 📦   | Extract **Item IDs** from mod JAR files               |
| 🧱   | Extract **Block IDs**                                 |
| 🌍   | Extract **Biome IDs**                                 |
| 🏛   | Extract **Structure IDs**                             |
| 👾   | Extract **Entity IDs**                                |
| 🖼   | Extract **Item Textures (PNG)**                       |
| 📂   | Automatically creates **numbered extraction folders** |

Example folders created:

```
Extract_1
Extract_2
Extract_3
```

---

# 📄 Output Format

All IDs are exported using the **standard Minecraft namespace format**.

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

# 🚀 How To Use

### 1️⃣ Install Python

Install **Python 3.x**

Download:
https://www.python.org/downloads/

---

### 2️⃣ Run the extractor

```
python minecraft_mod_extractor.py
```

---

### 3️⃣ Choose what to extract

* 📦 Items
* 🧱 Blocks
* 🌍 Biomes
* 🏛 Structures
* 👾 Entities
* 🖼 Textures

---

### 4️⃣ Select mod JAR files

Choose the **Minecraft mod `.jar` files** you want to scan.

---

### 5️⃣ Check the output folder

All results will appear inside the **`Extract` folder**.

---

# 📁 Output Files

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

# 🎮 Example Minecraft Commands

```
/give @p mutantmonsters:creeper_shard
/locate biome terralith:volcanic_peaks
/locate structure terralith:ancient_ruins
/summon alexsmobs:bone_serpent
```

---

# ⚙️ Requirements

| Requirement   | Notes                                   |
| ------------- | --------------------------------------- |
| 🐍 Python 3.x | Required to run the script              |
| 🖥 Tkinter    | Included with most Python installations |

---

# 📥 Download

Download the latest version from the **GitHub Releases page**:

➡ https://github.com/RKStudios-hub/Asset_Extractor_For_MCmadeEasy/releases/tag/v1.0

---

# 📜 License

This project is released under the **MIT License**.

---

# ⚠️ Disclaimer

```
This project is an independent fan-made creation and is not affiliated with,
endorsed by, or connected to Mojang Studios or Minecraft in any way.

Please do not report bugs, issues, or problems related to this project
to Mojang or the Minecraft support team.

Any feedback, bug reports, or questions should be directed only to the
developer of this project.
```

---

<h2 align="center">🖤 Made with love by <b>RK Studios</b></h2>
