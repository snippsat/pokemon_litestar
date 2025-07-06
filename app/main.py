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
async def get_pokemon_list(offset: int = 0) -> Template:
    """Get 12 Pokemon from PokeAPI with pagination."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/pokemon?limit=12&offset={offset}")
        data = response.json()
        
        # Get detailed info for each Pokemon
        pokemon_list = []
        for pokemon in data["results"]:
            pokemon_response = await client.get(pokemon["url"])
            pokemon_data = pokemon_response.json()
            
            # Calculate total base stats (power)
            total_base_stats = sum(stat["base_stat"] for stat in pokemon_data["stats"])
            
            pokemon_info = {
                "id": pokemon_data["id"],
                "name": pokemon_data["name"].title(),
                "sprite": pokemon_data["sprites"]["front_default"],
                "types": [type_info["type"]["name"] for type_info in pokemon_data["types"]],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "power": total_base_stats
            }
            pokemon_list.append(pokemon_info)
            
        # Check if there are more Pokemon available
        has_more = data["next"] is not None
        next_offset = offset + 12
        
    return Template(
        template_name="pokemon_list.html", 
        context={                        
            "pokemon": pokemon_list, 
            "has_more": has_more, 
            "next_offset": next_offset,
            "current_offset": offset,
            "is_first_load": offset == 0,
            "total_count": data["count"],
            "total_loaded": offset + len(pokemon_list)
        }
    )


@get("/pokemon/{pokemon_id:int}", include_in_schema=False)
async def get_pokemon_detail(pokemon_id: int) -> Template:
    """Get detailed information about a specific Pokemon."""
    async with httpx.AsyncClient() as client:
        # Get Pokemon data
        pokemon_response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        pokemon_data = pokemon_response.json()
        
        # Get species data for additional info
        species_response = await client.get(pokemon_data["species"]["url"])
        species_data = species_response.json()
        
        # Get abilities with descriptions
        abilities = []
        for ability_info in pokemon_data["abilities"]:
            ability_response = await client.get(ability_info["ability"]["url"])
            ability_data = ability_response.json()
            
            # Get English description
            description = "No description available."
            for entry in ability_data["effect_entries"]:
                if entry["language"]["name"] == "en":
                    description = entry["short_effect"]
                    break
            
            abilities.append({
                "name": ability_info["ability"]["name"].replace("-", " ").title(),
                "description": description,
                "is_hidden": ability_info["is_hidden"]
            })
        
        # Get flavor text
        flavor_text = "A mysterious Pokemon."
        for entry in species_data["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                flavor_text = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                break
        
        # Get some learnable moves (first 8)
        moves = []
        for move_info in pokemon_data["moves"][:8]:
            moves.append({
                "name": move_info["move"]["name"].replace("-", " ").title(),
                "url": move_info["move"]["url"]
            })
        
        # Process stats
        stats = []
        for stat in pokemon_data["stats"]:
            stat_name = stat["stat"]["name"].replace("-", " ").title()
            # Convert some stat names to more readable format
            if stat_name == "Special Attack":
                stat_name = "Sp. Atk"
            elif stat_name == "Special Defense":
                stat_name = "Sp. Def"
            
            stats.append({
                "name": stat_name,
                "base_stat": stat["base_stat"],
                "percentage": min(stat["base_stat"] / 200 * 100, 100)  # Scale to 200 max for percentage
            })
        
        pokemon_detail = {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"].title(),
            "sprite": pokemon_data["sprites"]["front_default"],
            "sprite_shiny": pokemon_data["sprites"]["front_shiny"],
            "official_artwork": pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
            "types": [type_info["type"]["name"] for type_info in pokemon_data["types"]],
            "height": pokemon_data["height"] / 10,  # Convert to meters
            "weight": pokemon_data["weight"] / 10,  # Convert to kg
            "base_experience": pokemon_data["base_experience"],
            "abilities": abilities,
            "stats": stats,
            "total_stats": sum(stat["base_stat"] for stat in stats),
            "moves": moves,
            "flavor_text": flavor_text,
            "habitat": species_data["habitat"]["name"].title() if species_data["habitat"] else "Unknown",
            "generation": species_data["generation"]["name"].replace("-", " ").title()
        }
        
    return Template(
        template_name="pokemon_detail.html",
        context={"pokemon": pokemon_detail}
    )


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
        route_handlers=[home, get_pokemon_list, get_pokemon_detail, static_files_router],
        template_config=template_config,
    )
        
    return app 