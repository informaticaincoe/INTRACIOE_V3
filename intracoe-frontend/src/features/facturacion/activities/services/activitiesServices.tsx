import axios from "axios"

// const apiKey = process.env.URL_BASE;

export const getAllActivities = async () => {
    try{
        const response = await axios.get(`http://127.0.0.1:8000/api/api/actividad/1`)
        console.log(response)

    }
    catch(error) {
        console.log(error)
    }
}