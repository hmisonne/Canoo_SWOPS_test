import { apiEndpoint } from '../config'

export async function api_getTemperature(): Promise<any> {
  try {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      };
      const result = await fetch(`${apiEndpoint}/temperature`,requestOptions)
      const json = await result.json()
      return parseInt(json.data,10)
  } catch(err){
    console.log(err)
  }
}

export async function api_setTemperature(temperature: number): Promise<any> {
  try {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temperature })
      };
      const response = await fetch(`${apiEndpoint}/temperature`,requestOptions)
      return response
  } catch(err){
    console.log(err)
  }
}

