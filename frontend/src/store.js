import { reactive, readonly } from "vue"

// configuration file
// import config from '/etc/frontend_config.json'

// development
import config from "../../frontend_config.json"

const authState = reactive({
	token: localStorage.getItem('token'),
	SERVER_ADDR: config.SERVER_ADDR,
	FRONTEND: config.FRONTEND,
	username: localStorage.getItem('username')
})

// --- Auth Actions Object ---
const authActions = {
    updateToken(token) {
        authState.token = token
        localStorage.setItem('token', token)
    },

    getAuthorizationHeader() {
        return { 'Authorization': `${config.AUTH_PREFIX} ${authState.token}` }
    },

    resetAuth() {
        authState.token = null
        localStorage.removeItem('token')
    }, 

    setUsername(name) {
    	authState.username = name
    	localStorage.setItem('username', name)
    }
}


export default {
	authState: readonly(authState),
	authActions
}