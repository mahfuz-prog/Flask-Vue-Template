import { reactive, readonly } from "vue"

// configuration file
// import config from '/etc/config.json'

// test
import config from "../../config.json"

const state = reactive({
	token: localStorage.getItem('token'),
	SERVER_ADDR: config.SERVER_ADDR
})

const updateState = (token) => {
	state.token = token
	localStorage.setItem('token', token)
}

const getAuthorizationHeader = () => {
	return { 'Authorization': `${config.AUTH_PREFIX} ${state.token}` }
}

const resetState = () => {
	state.token = null
	localStorage.removeItem('token')
}

export default {
	state: readonly(state),
	resetState,
	updateState,
	getAuthorizationHeader
}