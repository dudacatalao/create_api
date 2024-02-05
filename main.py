from fastapi import FastAPI
from fastapi import HTTPException, status
from modelo import Pokemon
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
  
@app.post('/pokemon')
async def post_pokemon(pokemon: Pokemon):
  if pokemon.id not in pokemons:
    pokemons[pokemon_id] = pokemon
    return pokemon
  else:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe')

if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="info", reload=True)
  