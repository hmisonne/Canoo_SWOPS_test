
import './App.css';
import { api_getTemperature, api_setTemperature } from './api/temperature-api'
import { api_getLights, api_addLight, api_removeLight, api_toggleLight } from './api/light-api'
import { useEffect, useState } from 'react'
import EmojiObjectsIcon from '@material-ui/icons/EmojiObjects';
import AddIcon from '@material-ui/icons/Add';
import RemoveIcon from '@material-ui/icons/Remove';

function App() {
  const [temperature, setTemperature] = useState(0)
  const [lights, setLights] = useState<any[]>([])
  useEffect(() => {
    async function fetchData() {
      const temperature = await api_getTemperature()
      const lights = await api_getLights()
      lights !== undefined && setLights(lights)
      temperature !== undefined && setTemperature(temperature)
    }
    fetchData()
  }, []);


  async function handleAddLight(e: any) {
    e.preventDefault();
    const newLight = await api_addLight();
    newLight !== undefined && setLights(lights => [...lights, newLight])
  }

  async function handleDelete(e: any, id: string) {
    e.preventDefault();
    const response = await api_removeLight(id);
    response && setLights(lights.filter(i => i.id !== id))
  }

  async function handleToggleLight(e: any, id: string) {
    e.preventDefault();
    const response = await api_toggleLight(id);
    response && setLights(lights.map(light => light.id === id
      ? {
        ...light,
        turnedOn: !light.turnedOn
      }
      : light
    ))

  }

  async function onIncrement(e: any) {
    e.preventDefault();
    const response = await api_setTemperature(temperature+1)
    response && setTemperature(temperature+1)
  }
  async function onDecrement(e: any) {
    e.preventDefault();
    const response = await api_setTemperature(temperature-1)
    response && setTemperature(temperature-1)
  }

  return (

    <div className="App">
      <div className="container">
      <div className="row">
        <p style={{ fontSize:50,margin:20 }}>
           {temperature} °F
        </p>
          <button onClick={onIncrement}>
            <AddIcon/>
          </button>
          <button onClick={onDecrement}>
            <RemoveIcon/>
          </button>
        </div>
        <div>
        <button 
          style={{ margin: 20 }}
          onClick={handleAddLight}>
            Add light
        </button>
          {lights.map(light => {
            return (
              <div key={light.id}>
                <button
                  onClick={(e) => handleToggleLight(e, light.id)}
                  style={{ backgroundColor: "#282c34" }}
                  name='up'>
                  <EmojiObjectsIcon
                    style={{ color: light.turnedOn ? "#FFD700" : 'white' }}
                    fontSize="large"
                  />
                </button>
                <button onClick={(e) => handleDelete(e, light.id)}>
                  X
              </button>
              </div>

            )
          })}
        </div>
      </div>
    </div>
  );
}

export default App;
