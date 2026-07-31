# Manifest schema

The manifest is the source of truth for pack readiness. Keep it small enough to review in a pull request and explicit enough to audit provenance.

```json
{
  "pack_id": "cozy-potion-shop",
  "pack_name": "Cozy Potion Shop",
  "version": "1.0.0",
  "status": "approved",
  "primary_format": "procedural-typescript",
  "assets": [
    {
      "id": "potion-bottle-01",
      "status": "approved",
      "reference": "assets/potion-bottle-01/reference.png",
      "model_source": "src/potion-bottle-01.ts",
      "preview": "previews/potion-bottle-01.png",
      "review": "assets/potion-bottle-01/review.md",
      "provenance": "assets/potion-bottle-01/provenance.md"
    }
  ],
  "provenance": [
    {
      "asset_id": "potion-bottle-01",
      "concept_tool": "GPT Image",
      "reconstruction_tool": "img2threejs",
      "human_edits": "material tuning and proportion adjustment",
      "third_party_dependencies": []
    }
  ]
}
```

Required pack fields are `pack_id`, `pack_name`, `version`, `status`, `assets`, and `provenance`. Every asset needs a unique `id`, a valid status, `reference`, `model_source`, and `review`. Approved assets also need `preview` and `provenance`.

Run `validate_pack.py PACK_DIR` while the pack is in progress. Run `validate_pack.py --release PACK_DIR` only when the pack status is `approved` and every asset is approved.
