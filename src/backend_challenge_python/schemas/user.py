from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    pokemon_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "ash",
                    "email": "ash@example.com",
                    "password": "pikachu123",
                    "pokemon_ids": [1, 25, 6],
                }
            ]
        }
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    pokemon_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class PokemonResponse(BaseModel):
    id: int
    name: str
    types: list[str]


class UserWithPokemonsResponse(UserResponse):
    pokemons: list[PokemonResponse]


class UpdateUserRequest(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    pokemon_ids: list[int] | None = None
