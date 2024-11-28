
import axios from "axios";

const localHttpInstance = axios.create({
	baseURL: process.env.LOCAL_BACKEND_BASE_URL ?? "http://localhost:8080/api",
	headers: {
		"Content-Type": "application/json",
		"Access-Control-Allow-Origin": "*",
	},
});

const pulseEcoInstance = axios.create({
	baseURL: "https://skopje.pulse.eco/rest",
	headers: {
		"Content-Type": "application/json",
	},
});

const encodeBase64 = (username, password) => {
	return btoa(`${username}:${password}`);
};

const setLocalAuthToken = (username, password) => {
	let localAuthToken = localStorage.getItem("localAuthToken");

	if (!localAuthToken && username && password) {
		localAuthToken = `Basic ${encodeBase64(username, password)}`;
		localStorage.setItem("localAuthToken", localAuthToken);
	}

	if (localAuthToken) {
		localHttpInstance.defaults.headers.common["Authorization"] = localAuthToken;
	} else {
		console.error("Username and password must be provided to generate the token.");
	}
};

const createRequestHandler = (httpInstance) => {
	const request = async (method, ...args) => {
		return await httpInstance[method](...args);
	};

	return {
		instance: httpInstance,
		get: (...args) => request("get", ...args),
		post: (...args) => request("post", ...args),
		put: (...args) => request("put", ...args),
		delete: (...args) => request("delete", ...args),
		patch: (...args) => request("patch", ...args),
		head: (...args) => request("head", ...args),
		options: (...args) => request("options", ...args),
	};
};

const localInstance = createRequestHandler(localHttpInstance);
const pulseEco = createRequestHandler(pulseEcoInstance);

export { localInstance, pulseEco, setLocalAuthToken };
