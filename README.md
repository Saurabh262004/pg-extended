# pg-extended
*A lightweight UI wrapper and window manager for pygame.*

> [!WARNING]
> - This library is in the early stages of development and may have many breaking changes in the future.  
> - Some of the features are still to be refined and added.

## Goal
- Provide a dynamic, customizable, and intuitive system for building UI and game elements in pygame.
- Handle repetitive UI / window management tasks for the user.
- Eventually evolve into a small, modular game engine.

---

## Installation
> [!IMPORTANT]
> pip install support will be added later on.

```
git clone https://github.com/Saurabh262004/pg-extended.git 
```

Copy the `pg_extended/` folder into the root directory of your project.  
Make sure that the folder name remains exactly `pg_extended/`.

---

# Example

A simple example of how to initialize an empty window with pg_extended.

```python
from pg_extended import Window

app = Window("Demo pgx window", (1280, 720))

app.openWindow()
```

> For more details, please checkout the [wiki page](../../wiki).
