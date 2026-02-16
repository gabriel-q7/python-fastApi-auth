# Main Differences Between Gunicorn and Uvicorn

## **Gunicorn (Green Unicorn)**
- **Type**: WSGI (Web Server Gateway Interface) server
- **Protocol**: Synchronous HTTP server
- **Use Case**: Traditional Python web frameworks (Flask, Django)
- **Workers**: Pre-fork worker model, spawns multiple worker processes
- **Async Support**: Limited (requires additional configuration)

## **Uvicorn**
- **Type**: ASGI (Asynchronous Server Gateway Interface) server
- **Protocol**: Asynchronous HTTP server
- **Use Case**: Modern async frameworks (FastAPI, Starlette)
- **Workers**: Single process by default, uses async/await
- **Async Support**: Native, built for async Python applications
- **Performance**: Generally faster for I/O-bound async operations

## **Common Pattern**
For production FastAPI applications, it's common to use **Gunicorn as a process manager** with **Uvicorn workers**:

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

This combines:
- **Gunicorn's** process management and stability
- **Uvicorn's** ASGI and async performance

For your FastAPI project, using Uvicorn directly for development and Gunicorn + Uvicorn workers for production is the recommended approach.

## **Python Version Compatibility Issue**

### **Problem**
When using Python 3.14, installation of dependencies fails with a build error:
```
ERROR: Failed building wheel for pydantic-core
error: could not compile `jiter` (lib) due to previous errors
PyO3 error: the configured Python interpreter version (3.14) is newer than PyO3's maximum supported version (3.13)
```

### **Root Cause**
- Python 3.14 is too new for current versions of `pydantic` and `pydantic-core`
- The `pydantic-core` package uses PyO3 Rust bindings which don't yet support Python 3.14
- Even with `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` flag, compilation fails due to missing Unicode API functions

### **Solution**
Use Python 3.13 or 3.12 instead:

**For Manjaro/Arch:**
```bash
sudo pacman -S python313
rm -rf .venv
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**For Ubuntu/Debian:**
```bash
sudo apt install python3.13 python3.13-venv
rm -rf .venv
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **Lesson Learned**
Always check Python version compatibility for dependencies, especially those with native extensions (Rust, C). Bleeding-edge Python versions may not be supported by popular libraries yet.
