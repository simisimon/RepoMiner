# RepoMiner

RepoMiner is a web application for analyzing and visualizing the historical changes in software repositories. It uses Flask for the web interface and Dash/Plotly for interactive visualizations.

## Requirements
- Python 3.10, 3.11, 3.12, or 3.13 (recommended: 3.10+)
- [Poetry](https://python-poetry.org/) for dependency management
- Git (for repository analysis)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <this-repo-url>
   cd RepoMiner
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

   If you do not have Poetry, install it with:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **(Optional) Set Python version:**
   If you have multiple Python versions, you can set the Python version for Poetry:
   ```bash
   poetry env use 3.10
   ```
   Or use your preferred compatible version (3.10+).

## Running the App

1. **Start the server:**
   ```bash
   poetry run python main.py
   ```

2. **Open your browser:**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage Notes
- Enter a local path or GitHub repository URL to analyze a repository.
- The app will visualize method changes and other repository metrics.
- If you see errors about missing repositories, ensure the path or URL is correct and accessible.

## Python-Levenshtein Fallback
- The app previously used `python-Levenshtein` for string similarity. On Python 3.13+, this library is not available, so a pure Python fallback (`difflib.SequenceMatcher`) is used. This may be slower for large repositories but works on all Python versions.

## Troubleshooting
- If you encounter dependency issues, ensure you are using a supported Python version (3.10+).
- For repository analysis, make sure you have `git` installed and available in your PATH.

## License
MIT

