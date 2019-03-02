const baseURL = process.env.NODE_ENV === 'production' ? 
    'https://api.swapdj.com/' : 'http://localhost:8000/'

const appURL = process.env.NODE_ENV === 'production' ? 
    'https://swapdj.com/' : 'http://localhost:8080/'

export default { baseURL, appURL }

