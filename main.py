from fastapi import FastAPI
from fastapi import HTTPException, status
from modelo import Pokemon
from typing import Optional
app = FastAPI()

pokemons = { 
  1: {
    'nome': 'Charmander',
    'elemento': 'fogo',
    'altura': 6
  },
  2: {
    'nome': 'Vaporeon',
    'elemento': 'água',
    'altura': 1
  }
}


#método get(visualizar)
@app.get("/")
async def raiz():
  return {'mensagem' : 'Funcionou'}

@app.get('/pokemon')
async def get_pokemons():
  return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemon(pokemon_id: int):
    if pokemon_id not in pokemons:
        raise HTTPException(status_code=404, detail="pokemon não encontrado")
    return pokemons[pokemon_id]

#método post (criar)
@app.post('/pokemon', status_code=status.HTTP_201_CREATED)
async def post_pokemon(pokemon: Optional[Pokemon] = None):
  if pokemon.id not in pokemon:
    next_id = len(pokemons) + 1
    pokemons[next_id] = pokemon
    del pokemon.id
    return pokemon
  else:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe')
  
#método put (atualizar)
@app.put('/pokemon/{pokemon_id}')
async def put_pokemon(pokemon_id: int, pokemon: Pokemon):
  if pokemon.id not in pokemon:
    pokemons[pokemon_id] = pokemon
    pokemon.id = pokemon_id
    del pokemon.id
    return pokemon
  
  else:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Não existe um pokemon com esse ID')
  
@app.delete('/pokemon/{pokemon_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_pokemon(pokemon_id: int, pokemon: Pokemon):
  if pokemon.id not in pokemon:
    del pokemons[pokemon_id]
    return 
  
  else:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Não existe um pokemon com esse ID')
  
  
if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="info", reload=True)
  