#!/usr/bin/env python3
"""Run the Pokemon Index application."""

import uvicorn
from app.main import create_app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"]
    ) 