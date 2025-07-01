# Pokemon Index - Litestar + HTMX + Tailwind

A simple Pokemon index application built with Litestar, HTMX, and Tailwind CSS.

## Features

- ✨ Modern web framework with Litestar
- 🚀 Dynamic content loading with HTMX
- 🎨 Beautiful styling with Tailwind CSS
- 📱 Responsive design
- 🔗 Integration with PokeAPI

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000
   ```

## How it works

- **Litestar**: Fast, modern Python web framework
- **HTMX**: Enables dynamic content loading without writing JavaScript
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **PokeAPI**: Free API for Pokemon data

## Usage

1. Visit the homepage
2. Click "Load Pokemon" button
3. Watch as the first 20 Pokemon load dynamically via HTMX
4. Enjoy the responsive Pokemon cards with type indicators

## Project Structure

```
pokemon/
├── app/
│   ├── __init__.py    # Package initialization
│   ├── main.py        # Main Litestar application
│   └── templates/
│       ├── base.html      # Base HTML template
│       ├── index.html     # Home page template
│       └── pokemon_list.html # Pokemon cards template
├── venv/              # Virtual environment
├── requirements.txt   # Python dependencies
├── run.py            # Application entry point
└── README.md         # This file
```

## Next Steps

- Add Pokemon detail pages
- Implement search functionality
- Add pagination for more Pokemon
- Create favorite Pokemon list
- Add more interactive features 