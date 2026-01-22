# AGENTS.md - Starting Line Productions Shop Book

This document helps agents understand this codebase and work effectively with it.

## Project Overview

This is a **mdBook** project that creates the Starting Line Productions (STL) Shop Guide - a comprehensive manual for a fabrication lab rental business. The project documents tools, equipment, supplies, and procedures across different shop areas (Cleanfab, Dirtyfab, E3ds, Kitchen, HPCLab, RackRental).

## Essential Commands

### Building the Book
```bash
mdbook build                # Build the book to `book/` directory
mdbook serve               # Start live development server (usually on localhost:3000)
mdbook clean               # Clean build artifacts
```

### PDF Generation (Optional)
The `book.toml` contains commented PDF configuration. To generate PDF:
1. Uncomment the `[output.pdf]` section in book.toml
2. Ensure you have a Chromium-based browser installed
3. Run `mdbook build`

## Code Organization

```
├── src/                    # Source markdown files
│   ├── SUMMARY.md         # Book structure/table of contents
│   ├── welcome.md         # Introduction page
│   ├── version-history.md # Version tracking
│   └── [shop-area]-*.md   # Content files organized by shop area
├── book.toml              # mdBook configuration
└── SourceMaterialTomerge/ # Binary source files (ODT, PDF, etc.)
```

### Content Structure
The book is organized by shop areas:
- **Cleanfab**: Clean fabrication shop
- **Dirtyfab**: Dirty fabrication shop  
- **E3ds**: Electronics/3D printing area
- **Kitchen**: Kitchen facilities
- **HPCLab**: High Performance Computing Lab
- **RackRental**: Server rack rental operations

Each area has:
- `*-overview.md`: Area introduction
- `*-tools.md`: Available tools
- `*-equipment.md`: Equipment inventory
- `*-supplies.md`: Supplies list

## File Naming Conventions

- Use kebab-case for all filenames
- Shop area prefixes: `cleanfab-`, `dirtyfab-`, `e3ds-`, `kitchen-`, `hpclab-`, `rackrental-`
- Suffixes indicate content type: `-overview`, `-tools`, `-equipment`, `-supplies`
- Standard files: `welcome.md`, `version-history.md`, `SUMMARY.md`

## Content Patterns

### Markdown Structure
- Use ATX-style headers (`#`, `##`, etc.)
- Include links to vendor/product documentation
- Add equipment pictures when available (files stored in `SourceMaterialTomerge/`)

### SUMMARY.md Structure
- Must match actual files in `src/` directory
- Order: Welcome → Version History → Safety/Security → Area-specific content
- Use relative paths: `./filename.md`

## Important Gotchas

### Broken Links in SUMMARY.md
There's a known issue in SUMMARY.md line 2: `[Version History](./version-history.)` should point to `./version-history.md` (missing `.md` extension).

### File Extensions
Ensure all markdown files in SUMMARY.md have the `.md` extension - mdBook requires exact matches.

### SourceMaterialTomerge/
This directory contains binary files (ODT, PDF, etc.) that are referenced in the content but not directly processed by mdBook.

## Style Guidelines

- Write comprehensive, detailed descriptions
- Focus on reproducibility - aim for the lab to be fully reproducible by anyone
- Include vendor documentation links
- Add plenty of images to showcase the shop setup
- Maintain consistent structure across shop areas

## Testing

After making changes:
1. Run `mdbook build` to verify syntax is correct
2. Run `mdbook serve` to check the book renders properly
3. Check all internal links work in the generated book
4. Verify SUMMARY.md entries point to existing files

## External Resources

- Project issues: https://projects.knownelement.com/project/reachableceo-vptechnicaloperations/kanban
- Discussion: https://community.turnsys.com/g/STLProducrtions