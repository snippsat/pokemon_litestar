from litestar import Litestar, get, Request
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
import httpx
from pathlib import Path


@get("/", include_in_schema=False)
async def home() -> Template:
    """Home page with Pokemon list."""
    return Template(template_name="index.html")


@get("/pokemon", include_in_schema=False)
async def get_pokemon_list() -> Template:
    """Get first 20 Pokemon from PokeAPI."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=20")
        data = response.json()
        
        # Get detailed info for each Pokemon
        pokemon_list = []
        for pokemon in data["results"]:
            pokemon_response = await client.get(pokemon["url"])
            pokemon_data = pokemon_response.json()
            
            pokemon_info = {
                "id": pokemon_data["id"],
                "name": pokemon_data["name"].title(),
                "sprite": pokemon_data["sprites"]["front_default"],
                "types": [type_info["type"]["name"] for type_info in pokemon_data["types"]]
            }
            pokemon_list.append(pokemon_info)
    
    return Template(template_name="pokemon_list.html", context={"pokemon": pokemon_list})


def create_app() -> Litestar:
    """Create and configure the Litestar application."""
    # Create template configuration
    template_config = TemplateConfig(
        directory=Path("app/templates"),
        engine=JinjaTemplateEngine,
    )

    # Create static files router for CSS/JS
    static_files_router = create_static_files_router(
        path="/static", directories=["static"]
    )

    app = Litestar(
        route_handlers=[home, get_pokemon_list, static_files_router],
        template_config=template_config,
    )
    
    return app 