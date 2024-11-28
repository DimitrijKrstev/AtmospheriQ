import { localInstance, pulseEco, setLocalAuthToken } from "../repository/Httpclient.js";

export default class MeasurementRepository {

	async get24hMeasurements() {
		try {
			const response = await pulseEco.get('data24h');
			return response;

		} catch (error) {
			console.warn(error);
		}
	}


	async getCurrentMeasurements() {
		try {
			const response = await pulseEco.get('current');
			return response;

		} catch (error) {
			console.warn(error);
		}
	}

}
