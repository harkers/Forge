# DisplayForge Mermaid Diagrams

## Standalone Display with Source Connectors

```mermaid
flowchart TD
    A[RSS Sources] --> D[Source Connector Layer]
    B[Calendar Sources] --> D
    C[API Sources] --> D
    D --> E[Normalisation Layer]
    E --> F[Display Components]
    F --> G[55-inch Fullscreen Display]
```

## Source Isolation Model

```mermaid
flowchart TB
    subgraph Sources
        R1[RSS Feed 1]
        R2[RSS Feed 2]
        C1[Calendar 1]
        C2[Calendar 2]
        A1[API Source 1]
    end
    
    subgraph Connectors
        RC[RSS Connector]
        CC[Calendar Connector]
        AC[API Connector]
    end
    
    subgraph Core
        N[Normaliser]
        S[State Manager]
        C[Cache Layer]
    end
    
    subgraph Display
        W[Widgets]
        L[Layouts]
        R[Renderer]
    end
    
    R1 --> RC
    R2 --> RC
    C1 --> CC
    C2 --> CC
    A1 --> AC
    
    RC --> N
    CC --> N
    AC --> N
    
    N --> S
    S --> C
    C --> W
    W --> L
    L --> R
```

## Normalisation Flow

```mermaid
sequenceDiagram
    participant Source
    participant Connector
    participant Normaliser
    participant Cache
    participant Display
    
    Source->>Connector: Fetch data
    Connector->>Normaliser: Raw items
    Normaliser->>Normaliser: Transform to DisplayItem
    Normaliser->>Cache: Store normalised
    Cache->>Display: Emit update
    Display->>Display: Re-render
```

## Failure Isolation

```mermaid
flowchart TD
    subgraph Healthy
        H1[RSS Feed 1] --> H2[Display: Fresh]
    end
    
    subgraph Degraded
        D1[RSS Feed 2] --> D2[Cache: Stale]
        D2 --> D3[Display: Dimmed + Stale Badge]
    end
    
    subgraph Failed
        F1[RSS Feed 3] --> F2[No Cache]
        F2 --> F3[Display: Error Placeholder]
    end
```

## Screen Layout Example

```mermaid
graph TB
    subgraph "55-inch Display"
        subgraph Top
            T[Header: Time + Status]
        end
        
        subgraph Left
            L1[Calendar: Today]
            L2[Calendar: Upcoming]
        end
        
        subgraph Center
            C1[Main Panel: Dashboard]
            C2[Status: KPIs]
        end
        
        subgraph Right
            R1[RSS Ticker]
            R2[Alerts]
        end
    end
```

## Refresh Cycle

```mermaid
stateDiagram-v2
    [*] --> Initialising
    Initialising --> Fetching: Start
    Fetching --> Parsing: Response received
    Parsing --> Normalising: Items extracted
    Normalising --> Caching: DisplayItems ready
    Caching --> Displaying: Emit to widgets
    Displaying --> Fetching: Refresh interval
    
    Fetching --> Error: Timeout/failure
    Error --> Cached: Use stale data
    Cached --> Displaying: Show with warning
    Displaying --> Fetching: Retry interval
```