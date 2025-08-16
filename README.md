# GGEN aka Gégène 
![GGEN System Overview](Assets/System/GGen_alpha.png)

## GGEN - Procedural Terrain Generator for TouchDesigner

**GGEN** aka (Gégène) is a modular node‑based procedural terrain and biome generation toolkit for TouchDesigner that lets you build and iterate on believable landscapes by chaining 3D and 2D operators (noise, shape, terraces, erosion, cavities, slope, snow, beaches, etc.), generate unlimited splatmaps stored as point attributes, tile and fill large 3D textures, and auto‑synthesize a powerful GLSL shader supporting height blending, and partial normal derivative for natural material transitions; it provides separate terrain and splatmap networks for geometry shaping and texture/biome distribution, encourages a fully procedural, GPU‑friendly, non‑destructive workflow, and ships as reusable components you can extend, with contributions welcomed under the MIT license.

---

### Features

- **Modular Node-Based Workflow:** Build complex terrains using a non destructive workflows with a variety of 3D and 2D operators.
- **Infinite Splatmaps:** Store splatmaps as point attributes as your grahic card can handle them.
- **3d Textures:** 3D texture filler system for managing large textures efficiently.
- **GLSL Shader Generation:** On-the-fly shader creation with blending parameters.
- **Advanced Blending:** Supports Partial Normal Derivatives and height blending for natural transitions.
- **Custom Nodes:** Includes pre-built TouchDesigner components to streamline your workflow.

---

## Managed Areas
These are network zones where terrain and splatmap networks are built. They are managed and monitored continuously to update parameters and the shader in real time.

### Terrain Network
The main area for constructing and manipulating the terrain's geometry. Nodes in this network define the shape, elevation, and features of your landscape.

### Splatmap Network
Handles the generation and blending of splatmaps, which control the texture distribution across your terrain.

---

## Node Operators

| Operator | Purpose | Notes |
|---|---:|---|
| Noise | Add Perlin noise | Useful for fractal detail and turbulence. |
| Shape | Define base terrain forms | Uses profiles/curves for silhouette control. |
| Terrace | Apply stepped terraces | Simulates plateaus, geological terraces. |
| Erosion | Simulate hydraulic/thermal erosion | Carves slopes and sediment deposits. |
| Beach | Create coastline transitions | Blends sand and water edges at elevation ranges. |
| Snow | Altitude/slope-based snow coverage | Controls accumulation by slope. |

### 2D Operators

| Operator | Purpose | Notes |
|---|---:|---|
| Cavity | Detect cavities/depressions | Neighborhood analysis. |
| HeightMap | Extract 2D heightmap from terrain flow | For export or downstream 2D processing. |
| Level | Normalize/adjust texture values | Fit height or texture within specified bounds. |
| Slope | Compute terrain slope | Drive slope-based texturing or visualizations. |
| Splatmap | Generate splatmaps from point attributes | Controls texture/biome distribution for shaders. |
---

### TO DO
| Operator | Purpose | Notes |
|---|---:|---|
| Blender | Attribute mixer for splatmap networks | Combine and blend point attributes. |
| Thermal Wither | Simulate weathering effects | Models wind-driven material loss. |

---

## Credits

Main dev : Arnaud Cassone aka [Artcraft](https://www.artcraft-zone.com)

---

## Getting Started

1. **Clone the Repository:**
2. **Drag and drop the GGEN tox file into your TouchDesigner project.**

3. **See the instructions provided in the GGEN documentation for setting up your terrain and splatmap networks.**

---



## Documentation

For detailed documentation on how to use GGEN, please refer to the [GGEN Documentation](docs/index.md).

## Contributing

Contributions are welcome! Please submit issues or pull requests to help improve GGEN.

---

## License

MIT License. See [LICENSE](LICENSE) for details.