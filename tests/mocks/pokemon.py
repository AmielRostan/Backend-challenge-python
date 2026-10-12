POKEMON_MOCKS = {
    1: {
        "id": 1,
        "name": "bulbasaur",
        "types": ["grass", "poison"],
    },
    25: {
        "id": 25,
        "name": "pikachu",
        "types": ["electric"],
    },
}


def fake_get_pokemon(self, pokemon_id: int) -> dict:
    return POKEMON_MOCKS[pokemon_id]
