# RankForge Mermaid Diagrams — Part 2

This file contains the operational and system-level diagrams for RankForge, covering runtime processing, workspace structure, dashboards, and resilience patterns.

---

## 9. Plugin Queue Engine

Description: Shows the dual-queue design. SEO processing runs first via Ollama, then feeds into the image queue which generates and stores images.

```mermaid
flowchart TD
    A[Posts] --> B[SEO Queue]
    B --> C[Worker: Ollama]
    C --> D[SEO Meta Stored]
    D --> E[Image Queue]
    E --> F[Worker: Stable Diffusion]
    F --> G[Image Output Stored]
```

---

## 10. Production Queue Processing

Description: Describes how batches are safely processed. Locks prevent concurrency issues, items are processed individually, and success or failure is tracked before moving to the next item.

```mermaid
flowchart TD
    A[WP CLI / Cron Trigger] --> B[Acquire Lock]
    B --> C[Fetch Queue Batch]
    C --> D[Process Item]
    D -->|Success| E[Mark Complete]
    D -->|Fail| F[Mark Error + Retry]
    E --> G[Next Item]
    F --> G
    G --> H[Release Lock]
```

---

## 11. Full Working Pipeline

Description: End-to-end view of the system. SEO optimisation runs first, followed by image generation, then storage and attachment back into WordPress.

```mermaid
flowchart TD
    A[WP CLI / Trigger] --> B[SEO Queue]
    B --> C[Worker]
    C --> D[Ollama]
    D --> E[SEO Metadata Stored]
    E --> F[Image Queue]
    F --> G[Worker]
    G --> H[Stable Diffusion]
    H --> I[Base64 Image]
    I --> J[Image Handler]
    J --> K[Saved File + Attachment]
    K --> L[Featured Image Set]
```

---

## 12. Workspace Model

Description: Shows how RankForge is structured within the Forge repository. Plugin code, operations, and tests are separated but coordinated within a single workspace.

```mermaid
flowchart TD
    A[Workspace: RankForge] --> B[plugin/]
    A --> C[ops/]
    A --> D[tests/]
    B --> E[Queues + Workers]
    B --> F[AI Clients]
    B --> G[Image Handler]
    C --> H[CLI Commands]
    C --> I[Cron Automation]
    D --> J[Validation Checks]
    E --> K[Ollama]
    E --> L[Stable Diffusion]
```

---

## 13. Dashboard Control Surface

Description: Represents the admin UI layer. Users can view queue states and manually trigger processing from within WordPress.

```mermaid
flowchart TD
    A[WordPress Admin] --> B[RankForge Menu]
    B --> C[Dashboard]
    C --> D[SEO Queue Stats]
    C --> E[Image Queue Stats]
    C --> F[Manual Controls]
    F --> G[Trigger Workers]
```

---

## 14. Retry / Error Loop

Description: Shows the basic retry mechanism. Failed jobs are surfaced to the dashboard, retried manually, and re-enter the processing loop.

```mermaid
flowchart TD
    A[Queue Item] --> B[Processing]
    B -->|Success| C[Complete]
    B -->|Fail| D[Error State]
    D --> E[Error Dashboard]
    E --> F[Retry Button]
    F --> G[Back to Pending]
    G --> B
```

---

## 15. Intelligent Retry + Backoff

Description: Advanced resilience model. Errors are classified, retried with exponential delay if appropriate, or moved to a dead-letter queue if not recoverable.

```mermaid
flowchart TD
    A[Job] --> B[Process]
    B -->|Success| C[Complete]
    B -->|Fail| D[Classify Error]
    D -->|Transient| E[Backoff + Retry]
    D -->|Content| F[Dead Letter Queue]
    D -->|Config| F
    D -->|Max Attempts| F
    E --> A
```
