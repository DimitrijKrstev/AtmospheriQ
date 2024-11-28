import { localInstance, pulseEco, setLocalAuthToken } from "../repository/Httpclient.js";
import { useEffect, useState } from "react"
import LineChartComponent from "../components/LineChartComponent.js"
import MeasurementRepository from "../repository/pulse-repository.js"

export default function Home() {
	const measurementRepository = new MeasurementRepository()
	const [measurements, setMeasurements] = useState([])

	useEffect(() => {
		setLocalAuthToken(process.env.USERNAME, process.env.PASSWORD)

		measurementRepository.get24hMeasurements().then((response) => {
			console.log("Localhost Data:", response.data);
			setMeasurements(response.data);
		}).catch(console.error);
	}, [])

	return (
		<>
			<div style={{
				display: 'flex', flexDirection: 'column', height: '90vh',
				alignItems: 'center', justifyContent: 'center'
			}}>
				<LineChartComponent sensorData={measurements}>

				</LineChartComponent>
			</div >
		</>
	)
}
