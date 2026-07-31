# Production profile

Complete this worksheet before production lock. It turns vague “ready” language into claims that can be tested and documented.

## Runtime and compatibility

```yaml
target_runtime: Three.js
supported_versions:
  - "pin or state a tested range"
browsers:
  - Chrome: "tested version"
  - Safari: "tested version"
devices:
  - desktop: "tested"
  - mobile: "tested or not supported"
```

If the pack targets Unity, Unreal, Blender, or another consumer, list the exact import path and version tested. Do not advertise compatibility with a platform that was not exercised.

## Performance budget

Choose budgets appropriate to the target scene and document the measurement method:

```yaml
max_draw_calls_in_demo: "measured target"
max_texture_memory_mb: "measured target"
max_scene_download_mb: "compressed target"
mobile_fps_target: "target and device"
```

The budgets are product requirements, not universal standards. If no budget is set, say so explicitly rather than implying optimization.

## Export guarantees

For every optional format, record:

- exporter and version;
- whether geometry, materials, transparency, animation, and pivots were checked;
- target importer and version;
- known differences from the procedural source.

“GLB included” means only that a file exists. “GLB tested” means it was imported into the named target and inspected.

## License and support profile

Define:

- whether buyers may use assets in commercial games, websites, SaaS, videos, and client work;
- whether redistribution, resale, or template inclusion is prohibited;
- what third-party materials require attribution;
- support channel and response target;
- compatibility/update window;
- refund or replacement policy;
- how license changes affect existing buyers.

Use a real license document for the final product. This worksheet is not legal advice and does not replace legal review.

## Known limitations

State whether the product includes or excludes:

- hidden-side fidelity;
- rigging and animation;
- collision meshes;
- UV editing;
- baked textures;
- mobile optimization;
- engine-native prefabs;
- commercial redistribution rights.
