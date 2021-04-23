import { apiEndpoint } from '../config'

export async function api_getLights(): Promise<any> {
  try {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      };
      const result = await fetch(`${apiEndpoint}/lights`,requestOptions)
      const json = await result.json()
      return json.data
  } catch(err){
    console.log(err)
  }
}

export async function api_addLight(): Promise<any> {
    try {
      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        };
        const result = await fetch(`${apiEndpoint}/lights`,requestOptions)
        const json = await result.json()
        return json.data
    } catch(err){
      console.log(err)
    }
  }

export async function api_removeLight(light_id: string): Promise<any> {
    try {
        const requestOptions = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
        };
        const result = await fetch(`${apiEndpoint}/lights/${light_id}`,requestOptions)
        const data = await result.json()
        return data
    } catch(err){
        console.log(err)
    }
}

export async function api_toggleLight(light_id: string): Promise<any> {
    try {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
        };
        const result = await fetch(`${apiEndpoint}/lights/${light_id}`,requestOptions)
        const data = await result.json()
        return data
    } catch(err){
        console.log(err)
    }
}
