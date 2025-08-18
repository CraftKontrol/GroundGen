#GGEN - POP Terrain Generator for TouchDesigner
#Version 1.005
![GGEN System Overview](Assets/System/GGen_alpha.png)

**GGEN** aka (Gégène) is a modular POP (point operator) based procedural terrain generation toolkit for TouchDesigner that lets you build and iterate on believable landscapes by chaining 3D and 2D operators (noise, shape, terraces, erosion, cavities, slope, snow, beaches, etc.).

It can generate unlimited splatmaps stored as point attributes, tile and fill large 3D textures, and auto‑synthesize a powerful GLSL shader supporting height blending, and partial normal derivative for natural material transitions.

It provides separate terrain and splatmap networks for geometry shaping and texture/biome distribution, encourages a fully procedural, GPU‑friendly, non‑destructive workflow, and ships as reusable components you can extend, with contributions welcomed under the MIT license.

---

### Features

- **Modular Workflow:** Build complex terrains using a non destructive POP workflows with 3D and 2D operators.
- **Infinite Splatmaps:** Store splatmaps as point attributes as your grahic card can handle them.
- **3d Textures:** 3D texture filler system for managing large textures efficiently.
- **GLSL Shader Generation:** On-the-fly shader creation with blending parameters.
- **Advanced Blending:** Supports Partial Normal Derivatives and height blending for natural transitions.
- **Custom Nodes:** Includes pre-built TouchDesigner components to streamline your workflow.

---

## [Common-Networks](https://github.com/CraftKontrol/GroundGen/wiki/Common-Networks)

These are network zones where terrain and splatmap networks are built. They are managed and monitored continuously to update parameters and the shader in real time.

| Network | Description |
|---|---|
| [Terrain Network](https://github.com/CraftKontrol/GroundGen/wiki/Terrain-Network) | Constructs and manipulates terrain geometry: shape, elevation, large-scale forms, and physical features. |
| [Splatmap Network](https://github.com/CraftKontrol/GroundGen/wiki/Splatmap-Network) | Generates and blends splatmaps controlling texture/biome distribution across the terrain. |

---

## Node Operators

Node operators are the building blocks of your terrain and splatmap networks. They define how data flows and is processed within the system. They can be used to create complex interactions and effects by combining multiple operators.

## 3D Operators

| Operator | Purpose | Notes |
|---|---:|---|
| [Noise](https://github.com/CraftKontrol/GroundGen/wiki/Noise) | Add Perlin noise | Useful for fractal detail and turbulence. |
| [Shape](https://github.com/CraftKontrol/GroundGen/wiki/Shape) | Define base terrain forms | Uses profiles/curves for silhouette control. |
| [Terrace](https://github.com/CraftKontrol/GroundGen/wiki/Terrace) | Apply stepped terraces | Simulates plateaus, geological terraces. |
| [Erosion](https://github.com/CraftKontrol/GroundGen/wiki/Erosion) | Simulate hydraulic/thermal erosion | Carves slopes and sediment deposits. |
| [Beach](https://github.com/CraftKontrol/GroundGen/wiki/Beach) | Create coastline transitions | Blends sand and water edges at elevation ranges. |
| [Snow](https://github.com/CraftKontrol/GroundGen/wiki/Snow) | Altitude/slope-based snow coverage | Controls accumulation by slope. |

### 2D Operators

| Operator | Purpose | Notes |
|---|---:|---|
| [Cavity](https://github.com/CraftKontrol/GroundGen/wiki/Cavity) | Detect cavities/depressions | Neighborhood analysis. |
| [HeightMap](https://github.com/CraftKontrol/GroundGen/wiki/HeightMap) | Extract 2D heightmap from terrain flow | For export or downstream 2D processing. |
| [Level](https://github.com/CraftKontrol/GroundGen/wiki/Level) | Normalize/adjust texture values | Fit height or texture within specified bounds. |
| [Slope](https://github.com/CraftKontrol/GroundGen/wiki/Slope) | Compute terrain slope | Drive slope-based texturing or visualizations. |
| [Splatmap](https://github.com/CraftKontrol/GroundGen/wiki/Splatmap) | Generate splatmaps from point attributes | Controls texture/biome distribution for shaders. |
---

### TO DO
| Operator | Purpose | Notes |
|---|---:|---|
| Blender | Attribute mixer for splatmap networks | Combine and blend point attributes. |
| Thermal Wither | Simulate weathering effects | Models wind-driven material loss. |

---


## Getting Started

1. **Clone the Repository:**

2. **Drag and drop the GGEN tox file into your TouchDesigner project.**

3. **See the instructions provided in the GGEN.toe example file.**

---


## Documentation

For detailed documentation on how to use GGEN, please refer to the [wiki](https://github.com/CraftKontrol/GroundGen/wiki).

## Contributing

Contributions are welcome! Please submit issues or pull requests to help improve GGEN.

---

## Credits

##### Main & lone dev : Arnaud Cassone aka [Artcraft](https://www.artcraft-zone.com)
##### Thanks to derivative [TouchDesigner](https://derivative.ca/)

---

## License

MIT License. See [LICENSE](LICENSE) for details.