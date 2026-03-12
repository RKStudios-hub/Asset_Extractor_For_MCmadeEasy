# Asset Extractor For MC

A Minecraft mod data extractor tool - extracts items, blocks, biomes, structures, and entities from mod JAR files for use in Minecraft commands.

## Features

- Extract item IDs from mod JARs
- Extract block IDs
- Extract biome IDs  
- Extract structure IDs
- Extract entity IDs
- Extract item textures (PNGs)
- Numbered extraction folders (Extract_1, Extract_2, etc.)

## Output Format

```
modid:item_name
```

Example:
```
mutantmonsters:creeper_shard
create:cogwheel
terralith:marble
```

## Usage

1. Install Python 3.x
2. Run the extractor:
   ```
   python minecraft_mod_extractor.py
   ```
3. Select what to extract (Items, Entities, Biomes, Structures, Textures)
4. Select your mod JAR files
5. Check the `Extract` folder for results

## Output Files

- `items.txt` - All item IDs
- `blocks.txt` - All block IDs  
- `all_items_blocks.txt` - Combined items and blocks
- `biomes.txt` - Biome IDs
- `structures.txt` - Structure IDs
- `entities.txt` - Entity IDs
- `Extracted_PNGs/` - Item textures

## Example Commands

```bash
/give @p mutantmonsters:creeper_shard
/locate biome terralith:volcanic_peaks
/locate structure terralith:ancient_ruins
/summon alexsmobs:bone_serpent
```

## Requirements

- Python 3.x
- Tkinter (included with Python)

## License

MIT
