import httpx

from backend_challenge_python.config import settings


class PokemonClient:
    def get_pokemon(self, pokemon_id: int) -> dict:
        response = httpx.get(
            f"{settings.pokemon_api_url}/pokemon/{pokemon_id}",
            timeout=5.0,
        )

        response.raise_for_status()
        data = response.json()

        return {
            "id": data["id"],
            "name": data["name"],
            "types": [item["type"]["name"] for item in data["types"]],
        }
