from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend_challenge_python.clients.pokemon import PokemonClient
from backend_challenge_python.database import get_db
from backend_challenge_python.repositories.users import UsersRepository
from backend_challenge_python.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserWithPokemonsResponse,
)
from backend_challenge_python.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])

DbSession = Annotated[Session, Depends(get_db)]


def get_users_service(db: DbSession) -> UsersService:
    repository = UsersRepository(db)
    pokemon_client = PokemonClient()

    return UsersService(repository, pokemon_client)


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: CreateUserRequest, service: UsersServiceDep):
    return service.create(user)


@router.get("", response_model=list[UserResponse])
def get_users(service: UsersServiceDep):
    return service.get_all()


@router.get("/{user_id}", response_model=UserWithPokemonsResponse)
def get_user(user_id: int, service: UsersServiceDep):
    return service.get_by_id_with_pokemons(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UpdateUserRequest, service: UsersServiceDep):
    return service.update(user_id, data)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UsersServiceDep):
    return service.delete(user_id)
