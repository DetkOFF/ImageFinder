# Image Search App (Desktop, Python)

A simple desktop application for searching through a local collection of images using text captions.  
Designed for personal image libraries, datasets, or any folder of pictures with associated text descriptions.

---

## Features

- Search images by text captions stored in a JSONL file.  
- Lightweight Tkinter GUI, works on Windows.
- Display search results in a scrollable grid layout.  
- Copy an image to the clipboard by clicking on it.  
- Paste text into the search bar with **Ctrl+V**.  
- Special Finder_lite.py version of default finder.py script for lightweight builds.
- Auto captions generator that uses OCR and Img_2_text models.

---

## How to use

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create captions for images using img_to_text model and OCR:
    ```bash
    python src\tagger\tagger.py
    ```

    or write your own tags manually

3. Generate the index (once):
    ```bash
    python src\tagger\index_generator.py
    ```

4. Launch the GUI:
    ```bash
    python src\img_finder\gui.py
    ```

## How to build
Use PyInstaller:

```bash
pyinstaller --name=ImgFinder --onefile --windowed src\img_finder\gui.py
```

It's recommended to use *finder_lite* in **gui.py** to reduce the size of application and change paths to image dataset (Img/ folder) and inv_index.pkl, to keep them next to gui.exe after.

If you dont use *finder_lite.py* but *finder.py*, include spaCy language models via --add-data and --hidden-import.
