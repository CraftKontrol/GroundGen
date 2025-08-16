# GGEN aka Gégène 
![GGEN System Overview](Assets/System/GGen_alpha.png)

## GGEN - Procedural Terrain Generator for TouchDesigner

**GGEN** aka (Gégène) is an MIT‑licensed, modular, node‑based procedural terrain and biome generation toolkit for TouchDesigner that lets you build and iterate on believable landscapes by chaining 3D and 2D operators (noise, shape, terraces, erosion, cavities, slope, snow, beaches, etc.), generate unlimited splatmaps stored as point attributes, tile and fill large 3D textures, and auto‑synthesize a powerful GLSL shader supporting height blending, and partial normal derivative for natural material transitions; it provides separate terrain and splatmap networks for geometry shaping and texture/biome distribution, encourages a fully procedural, GPU‑friendly, non‑destructive workflow, and ships as reusable components you can extend, with contributions welcomed under the MIT license.

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
| Noise | Add natural variation using Perlin/Simplex/etc. | Useful for fractal detail and turbulence. |
| Shape | Define base terrain forms (mountains, valleys, plains) | Uses profiles/curves for silhouette control. |
| Terrace | Apply stepped terraces | Simulates plateaus, rice fields, geological terraces. |
| Erosion | Simulate hydraulic/thermal erosion | Carves riverbeds, slopes, and sediment deposits. |
| Beach | Create coastline transitions | Blends sand and water edges at elevation ranges. |
| Snow | Add altitude/slope-based snow coverage | Controls accumulation by slope and height. |

### 2D Operators

| Operator | Purpose | Notes |
|---|---:|---|
| Cavity | Detect and enhance cavities/depressions | Neighborhood analysis to accentuate valleys/crevices. |
| HeightMap | Extract 2D heightmap from terrain flow | For export or downstream 2D processing. |
| Level | Normalize/adjust texture values | Fit height or texture within specified bounds. |
| Slope | Compute terrain slope | Drive slope-based texturing or visualizations. |
| Splatmap | Generate splatmaps from point attributes | Controls texture/biome distribution for shaders. |
---

### TO DO
| Operator | Purpose | Notes |
|---|---:|---|
| Blender | Attribute mixer for terrain and splatmap networks | Combine and blend point attributes. |
| Thermal Wither | Simulate wind erosion and weathering effects | Models thermal stress and wind-driven material loss. |


## Getting Started

1. **Clone the Repository:**
2. **Drag and drop the GGEN tox file into your TouchDesigner project.**

3. **See the instructions provided in the GGEN documentation for setting up your terrain and splatmap networks.**

---

## Credits

[Arnaud Cassone](https://www.artcraft-zone.com)

## Documentation

For detailed documentation on how to use GGEN, please refer to the [GGEN Documentation](docs/index.md).

## Contributing

Contributions are welcome! Please submit issues or pull requests to help improve GGEN.

---

## License

MIT License. See [LICENSE](LICENSE) for details.