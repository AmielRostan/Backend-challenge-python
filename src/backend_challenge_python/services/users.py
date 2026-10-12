from fastapi import HTTPException

from backend_challenge_python.clients.pokemon import PokemonClient
from backend_challenge_python.models.user import User
from backend_challenge_python.repositories.users import UsersRepository
from backend_challenge_python.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserWithPokemonsResponse,
)
from backend_challenge_python.services.password import hash_password


class UsersService:
    def __init__(self, repository: UsersRepository, pokemon_client: PokemonClient):
        self.repository = repository
        self.pokemon_client = pokemon_client

    def create(self, data: CreateUserRequest) -> User:
        existing_user = self.repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
            pokemon_ids=data.pokemon_ids,
        )

        return self.repository.create(user)

    def get_all(self) -> list[User]:
        return self.repository.get_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return user

    def get_by_id_with_pokemons(self, user_id: int) -> UserWithPokemonsResponse:
        user = self.get_by_id(user_id)

        pokemons = [
            self.pokemon_client.get_pokemon(pokemon_id)
            for pokemon_id in user.pokemon_ids
        ]

        return UserWithPokemonsResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            pokemon_ids=user.pokemon_ids,
            pokemons=pokemons,
        )

    def update(self, user_id: int, data: UpdateUserRequest) -> User:
        user = self.get_by_id(user_id)

        changes = data.model_dump(exclude_unset=True)

        if "email" in changes:
            if changes["email"] is None:
                raise HTTPException(status_code=422, detail="Email cannot be null")

            existing_user = self.repository.get_by_email(changes["email"])

            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=422,
                    detail="Email is already registered",
                )

        if "password" in changes:
            if changes["password"] is None:
                raise HTTPException(status_code=422, detail="Password cannot be null")

            changes["password"] = hash_password(changes["password"])

        for field, value in changes.items():
            setattr(user, field, value)

        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repository.delete(user)
