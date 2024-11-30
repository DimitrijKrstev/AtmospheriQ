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

	async get12hRawMeasurements(sensorId, valueType) {
		try {
			/*const now = moment().toISOString();
			const from = moment().subtract(12, 'hours').toISOString();
*/
			let now = new Date();
			let from = new Date(now.getTime() - 12 * 60 * 60 * 1000); // 12 hours ago

			console.log(from);
			console.log(now);


			console.log(from.toISOString());
			console.log(now.toISOString());

			console.log(encodeURIComponent(from.toISOString()));
			console.log(encodeURIComponent(now.toISOString()));

			/*const formatDate = (date) => {
				return encodeURIComponent(
					date.toISOString().replace(/\.\d+Z$/, '%2b00:00')// Replacing 'Z' with timezone offset (+00:00)
				);
			};*/

			const formatDate = (date) =>
				`${date.toISOString().slice(0, 19)}%2b00:00`;

			from = formatDate(from);
			now = formatDate(now);

			console.log(from);
			console.log(now);

			// https://skopje.pulse.eco/rest/dataRaw?sensorId=1001&type=pm10&from=2017-03-15T02:00:00%2b01:00&to=2017-03-19T12:00:00%2b01:00 -
			const response = await pulseEco.get(`/dataRaw?sensorId=${sensorId}&
type=${valueType}&from=${from}&to=${now}`);
			return response.data; // Return just the data if the API provides a response object
		} catch (error) {
			console.warn("Failed to fetch 12-hour raw measurements:", error);
			throw error;
		}
	}

}
