# DisplayForge Product Definition

**Status:** Active Development  
**Path:** `products/displayforge/`  
**Type:** Standalone Product (sibling to RankForge)

## Placement

```
Forge/
├── products/
│   ├── rankforge/        # Processing & optimisation
│   └── displayforge/     # Presentation & visualisation ← THIS PRODUCT
├── standards/
│   └── naming.md
└── .github/
```

**DisplayForge is a sibling product to RankForge.**
- NOT nested inside RankForge
- NOT a subcomponent
- Independent workspace with own boundaries

## Purpose

DisplayForge handles all visual presentation concerns:
- Digital signage and kiosk displays
- Dashboard rendering and monitoring
- Real-time status visualisation
- Control surface interfaces

## Relationship to RankForge

| Product | Domain | Output |
|---------|--------|--------|
| RankForge | Processing, optimisation, scoring | Data, rankings, recommendations |
| DisplayForge | Visualisation, presentation, dashboards | Screens, widgets, rendered output |

**Integration Points:**
- RankForge produces processing data → DisplayForge visualises results
- DisplayForge consumes RankForge APIs for real-time status
- Shared standards from `standards/` but separate implementations

## Workspace Structure

```
products/displayforge/
├── README.md              # Product overview
├── PRODUCT.md             # This file - product definition
├── roadmap.md             # Development phases
├── architecture.md        # Technical architecture
├── openclaw-brief.md      # OpenClaw integration notes
├── openclaw/              # OpenClaw skills and prompts
├── skills/                # Agent skills for display management
├── ops/                   # Deployment and operations
├── tests/                 # Test suites
└── app/                   # Application code
```

## Boundaries

**DisplayForge owns:**
- Rendering pipelines
- Layout engines
- Template systems
- Output adapters
- Multi-screen coordination

**DisplayForge does NOT own:**
- Data processing logic (RankForge)
- Business rules (domain-specific)
- Storage persistence (shared infrastructure)

**Shared with RankForge:**
- Naming conventions (`standards/naming.md`)
- CI/CD patterns (`.github/`)
- Infrastructure modules (future: `shared/`)

## Naming

- Product: **DisplayForge** (PascalCase)
- Package: `displayforge` (lowercase)
- Prefix: `display-` for modules, `DisplayForge` for classes
- Skills: `display-forge-*` in OpenClaw

## Constraints

1. **Separation of concerns:** Presentation logic stays in DisplayForge
2. **No circular dependencies:** DisplayForge consumes RankForge APIs, never the reverse
3. **Independent release:** DisplayForge versions independently
4. **Workspace isolation:** Each product owns its `app/`, `tests/`, `ops/`

---

*This document defines product placement and should not be edited without updating the Forge product registry.*
