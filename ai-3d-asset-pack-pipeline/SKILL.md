---
name: ai-3d-asset-pack-pipeline
description: Plan, produce, quality-gate, package, and launch coherent AI-native 3D asset packs using image concepts, img2threejs, and Three.js. Use when a user wants to turn generated 2D concepts into a sellable collection, build a repeatable asset factory, create marketplace-ready files, or design the automation and monetization around an AI 3D asset business.
---

# AI 3D Asset Pack Pipeline

## Overview

Treat an asset pack as a small product, not a folder of unrelated generated models. Start from a buyer and scene-building problem, define a style system, generate and filter concepts, reconstruct assets with img2threejs, review them visually, package source and compatibility exports, and launch with a usable demo.

## Operating principles

- Optimize for a coherent collection and a clear buyer, not maximum asset count.
- Prefer hard-surface props for the first pack; single-view procedural reconstruction is weakest on hidden sides, crowds, plants, animals, and complex characters.
- Keep the procedural TypeScript source as the primary product. Treat GLB/FBX/OBJ exports as an optional compatibility branch that may require Blender cleanup.
- Automate bookkeeping, validation, rendering, and packaging. Keep style, usefulness, and visual approval human-reviewed.
- Never imply that a generated asset is fully game-ready until scale, materials, topology/export behavior, documentation, and target-engine import have been checked.
- Track provenance for every reference, generated image, model, texture, and third-party dependency before commercial release.

## Workflow

### 1. Define the product brief

Write a short brief before generating anything:

```yaml
pack_name: Cozy Potion Shop
buyer: indie game and web developers
target_runtime: Three.js
style: warm low-poly fantasy
asset_count: 15
primary_format: procedural TypeScript
optional_formats: [glb]
price_tier: starter
```

Ask what scene the buyer can build with the pack. Reject themes that do not have a clear scene, repeated visual language, and at least 10 useful asset candidates.

### 2. Build the design bible

Specify palette, geometry, proportions, materials, lighting, camera, scale, naming, and forbidden traits. Include rules that are measurable at review time, such as “no thin unsupported parts,” “all props share a 1-unit tabletop scale,” and “silhouette remains readable at thumbnail size.”

### 3. Generate and filter concepts

Generate concept sheets in batches by category (for example: containers, furniture, decorations, tools). Filter before 3D reconstruction.

Use this funnel as a starting heuristic:

```text
100 concepts → 30 shortlisted → 18 reconstructed → 15 shipped
```

Keep the selected reference image and its prompt with the asset record. Do not use branded characters, logos, or unlicensed source art as pack identity.

### 4. Reconstruct with img2threejs

For each selected asset:

1. Provide one clean, isolated reference image with a readable silhouette.
2. State the intended style, scale, and whether the object is static or animated.
3. Let img2threejs produce the spec and procedural TypeScript.
4. Render the result beside the reference.
5. Revise only the failing parts; do not silently accept hidden-side guesses.

Record `reference`, `spec`, `model_source`, `render`, `review`, and `status` in the asset manifest. The method produces editable Three.js code; it is not automatically a production mesh pipeline.

### 5. Apply the quality gate

An asset is `approved` only when all of these are true:

- silhouette and identity match the selected reference;
- proportions, materials, and scale fit the pack bible;
- no floating, intersecting, missing, or accidental parts are visible;
- the source renders without console or import errors;
- the object is useful in the buyer's target scene;
- the asset has provenance and license notes;
- required previews and documentation exist.

Use these states only: `draft`, `needs_revision`, `approved`, `rejected`. A pack cannot be released with non-approved assets in its public manifest.

### 6. Package the release

Ship a predictable archive containing:

```text
pack/
  src/                  # procedural TypeScript
  exports/              # optional GLB/FBX/OBJ compatibility files
  demo/                 # runnable Three.js scene
  previews/             # thumbnails, hero image, comparison sheets
  manifest.json
  installation.md
  usage.md
  license.md
  changelog.md
```

Use `scripts/new_pack.py` to create a manifest and directory structure. Use `scripts/validate_pack.py` before every release. Do not ship a pack if validation reports missing files, invalid statuses, duplicate IDs, or a missing license/provenance record.

### 7. Launch and learn

Publish an interactive demo first, then list the pack on the marketplace that matches its format. Fab is a current digital asset marketplace; Sketchfab can be useful for interactive previews and portfolio credibility. Read current seller, technical, and license requirements before each submission because marketplace rules change. See [references/platforms-and-licensing.md](references/platforms-and-licensing.md).

Use a three-level funnel:

- free sampler: 3 assets;
- starter pack: 15–20 assets, procedural source, approximately $19–39;
- professional pack: source, compatibility exports, scenes, and commercial license, approximately $59–99.

Treat custom commissions as a discovery channel for future reusable packs. Measure demo visits, sampler downloads, paid conversions, support questions, refund reasons, and which asset categories are requested next.

## Automation boundary

Automate:

- pack and asset folder creation;
- manifest updates;
- filename and status checks;
- preview-sheet generation;
- render/export commands;
- archive creation;
- release checklists.

Keep human decisions for:

- theme and buyer selection;
- concept filtering;
- visual consistency;
- usefulness of the asset;
- final commercial and licensing review.

## Suggested first milestone

Build one hard-surface pack of 15 props for a single scene, with five hero assets, a working Three.js demo, a free three-asset sampler, and a complete provenance record. Do not scale to multiple themes until this pack can be generated, reviewed, documented, and repackaged repeatably.

## Resource routing

- Use [references/platforms-and-licensing.md](references/platforms-and-licensing.md) when deciding where to publish, checking marketplace expectations, or preparing commercial provenance records.
- Run `scripts/new_pack.py` when starting a pack.
- Run `scripts/validate_pack.py` when reviewing a pack or before creating a release archive.
