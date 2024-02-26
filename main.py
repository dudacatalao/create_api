from fastapi import HTTPException, status, Path, FastAPI, Header, Depends
from modelo import Pokemon
from typing import Optional, Any, List
from time import sleep

def fake_db():
  try:
    print('Open database..')
    sleep(3)

  finally:
    print('Closing database..')
    sleep(1)

app = FastAPI(description='API para Estudos do FastAPI', title='API da aula de Web Dev', version='0.0.1', )
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

@app.get('/pokemon', description='Retorna uma lista de pokemons cadastrados ou uma lista vazia', response_model=List[Pokemon])
async def get_pokemons(db: Any = Depends(fake_db)):
  return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemon(pokemon_id: int = Path(...,title='Buscar pokeom pelo id', gt=0, lt=3, description='Selecionar pokemon por id, onde o id deve ser 1 ou 2')):
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
  
#metodo delete (deletar)
@app.delete('/pokemon/{pokemon_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(pokemon_id: int):
  if pokemon_id in pokemons:
    del pokemons[pokemon_id]
    return 

  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não existe um pokemon com esse ID')
  
#############################################
@app.get('/calculadora/soma')
async def calcular(n1:int, n2:int, n3:Optional[int] = None):
    if n3 == None:
      soma = n1 + n2 
      return {'Resultado:' : soma}
    else:
      soma = n1 + n2 + n3
      return {'Resultado:' : soma}
    
@app.get('/calculadora/subtracao')
async def calcular(n1:int, n2:int, n3:Optional[int] = None):
    if n3 == None:
      subtracao = n1 - n2 
      return {'Resultado:' : subtracao}
    else:
      subtracao = (n1 - n2) - n3
      return {'Resultado:' : subtracao}
    
@app.get('/calculadora/multiplicacao')
async def calcular(n1:int, n2:int, n3:Optional[int] = None):
    if n3 == None:
      multiplicacao = n1 - n2 
      return {'Resultado:' : multiplicacao}
    else:
      multiplicacao = n1 - n2 - n3
      return {'Resultado:' : multiplicacao}
    
@app.get('/headerEx')
async def headerEx(duda: str = Header(...)):
  return {'Duda': duda}
#############################################
  
  
if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', host="127.0.0.1", port=8000, log_level="info", reload=True)
  
  
  