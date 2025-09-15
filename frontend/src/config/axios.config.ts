import axios from 'axios'

const http = axios.create()

http.interceptors.request.use((config) => {
    config.baseURL = 'http://localhost:8000/api'

    return config
})

export default http