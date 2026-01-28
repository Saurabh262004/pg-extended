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
```
pip install pg-extended
```

Inside your python project:

```python
import pg_extended
```

---

# Example

A simple example of how to initialize an empty window with pg_extended.

```python
from pg_extended import Window

# create a window with "Demo pgx window" as the title with 1280x720 resolution
app = Window("Demo pgx window", (1280, 720))

# all the UI / Game setup can be done here

# open the window
app.openWindow()
```

> For more details, please checkout the [wiki](https://github.com/Saurabh262004/pg-extended/wiki).

---

## [HVision](https://github.com/Saurabh262004/HVision)

### A project by me that uses pg-extended in an actual real environment.
