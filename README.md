# AI 3D Asset Pack Pipeline

Reusable Codex skill for turning generated concepts into coherent, reviewable, and commercially packageable 3D asset packs.

The workflow is designed around GPT Image concepts, [img2threejs](https://github.com/img2threejs/img2threejs), and Three.js. It treats the pack as a product: define a buyer, establish a visual system, reconstruct selected assets, review the result, record provenance, package the files, and launch with a working demo.

## What this repository contains

```text
SKILL.md                         # Codex operating instructions
agents/openai.yaml               # UI metadata and invocation prompt
references/
├── manifest-schema.md            # Manifest contract and example
└── platforms-and-licensing.md    # Publishing and provenance checklist
scripts/
├── new_pack.py                   # Create a pack workspace
└── validate_pack.py              # Validate draft or release readiness
```

## Install for Codex

Clone this repository and place the `ai-3d-asset-pack-pipeline` directory in your Codex skills directory:

```bash
git clone https://github.com/Playitcooool/ai-3d-asset-pack-pipeline.git \
  ~/.codex/skills/ai-3d-asset-pack-pipeline
```

Then invoke it explicitly:

```text
Use $ai-3d-asset-pack-pipeline to plan a Cozy Potion Shop prop pack for Three.js.
```

The skill can also be selected from the Codex skill picker when its metadata is available to the host.

## Quick start

Create a pack workspace:

```bash
python3 scripts/new_pack.py \
  "Cozy Potion Shop" --output ./packs
```

This creates a draft pack with `src`, `exports`, `demo`, `previews`, `assets`, a manifest, and documentation stubs.

Validate while developing:

```bash
python3 scripts/validate_pack.py \
  ./packs/cozy-potion-shop
```

Validate for public release:

```bash
python3 scripts/validate_pack.py \
  --release ./packs/cozy-potion-shop
```

Release mode requires an approved pack, at least one approved asset, provenance, and real files for every approved asset reference.

## Recommended first pack

Start with 15 hard-surface props for one scene—for example, a potion shop, roadside camp, or small workshop. This is a better first target than characters or organic environments because single-view procedural reconstruction is more reliable when the silhouette and visible components are clear.

Ship:

- 15 coherent props;
- five hero assets with comparison renders;
- a runnable Three.js demo;
- a free three-asset sampler;
- source TypeScript as the primary deliverable;
- optional GLB exports only after an actual import check;
- a complete provenance record.

## Product boundary

The pipeline produces editable procedural Three.js code. It does not, by itself, guarantee game-ready topology, UVs, animation rigs, collision meshes, or production-quality GLB/FBX exports. If a buyer needs engine-native meshes, add a separate Blender/export/engine-import stage and document what was tested.

## Quality and release gates

An asset is publishable only when its silhouette, proportions, materials, scale, render behavior, scene usefulness, provenance, and documentation have been reviewed. The release validator catches structural failures; it cannot judge visual quality. Keep final visual approval human-reviewed.

## Versioning policy

- Use semantic versions in `manifest.json`.
- Increment patch versions for metadata, documentation, or non-breaking fixes.
- Increment minor versions for additive assets or compatible improvements.
- Increment major versions when asset IDs, formats, behavior, or license scope change incompatibly.
- Keep a changelog with every public release.

## Limitations and licensing

The included platform guidance is operational, not legal advice. Re-check current marketplace terms and the licenses of all concepts, textures, fonts, code, and dependencies before selling. See [platforms-and-licensing.md](references/platforms-and-licensing.md).

## Development checks

Run the skill validator after editing the package:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

The repository is intentionally small. The skill body contains the operating sequence; references contain details that should be loaded only when the task needs them; scripts enforce repeatable invariants.
