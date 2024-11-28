import React, { useState, useEffect } from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { Button, Box, Typography } from "@mui/material";

const opshtini = [
	{ name: "Centar", sensorId: "0f10deea-03bc-4a47-ae87-85442140467c" },
	{ name: "Kisela Voda", sensorId: "sensor_dev_77790_464" },
	{ name: "Aerodrom", sensorId: "f9a91b1f-a6cf-4484-90e4-e5df7a128625" },
	{ name: "Madzari", sensorId: "5de2a490-05f1-4f33-927e-a7e6f5664b72" },
	{ name: "Karposh", sensorId: "fef6bc74-bf86-4874-9531-51b033580379" },
];

const types = ["pm10", "pm25", "humidity", "temperature"];

const LineChartComponent = ({ sensorData }) => {
	const [selectedType, setSelectedType] = useState("pm10");
	const [chartData, setChartData] = useState([]);
	const [selectedOpshtina, setSelectedOpshtina] = useState(opshtini[0]);

	useEffect(() => {
		if (sensorData && sensorData.length > 0) {
			const filteredData = sensorData.filter(
				(data) =>
					data.type === selectedType &&
					data.sensorId === selectedOpshtina?.sensorId
			);

			if (filteredData.length === 0) {
				setChartData([]);
				return;
			}

			const chartPoints = filteredData.map((data) => ({
				x: new Date(data.stamp).getHours(), // Extract hour from timestamp
				y: parseFloat(data.value), // Parse value as a number
			}));

			const fullHourRange = Array.from({ length: 24 }, (_, i) => i);

			const completeChartData = fullHourRange.map(hour => {
				const pointForHour = chartPoints.find(point => point.x === hour);
				return pointForHour || { x: hour, y: null };
			});

			setChartData(completeChartData);
		}
	}, [selectedType, selectedOpshtina, sensorData]);

	if (!sensorData || sensorData.length === 0) {
		return (
			<Typography variant="h6" color="error">
				No sensor data available
			</Typography>
		);
	}

	return (
		<Box sx={{ padding: 2 }}>
			{/* Buttons to select sensor type */}
			<Box sx={{ display: "flex", justifyContent: "center", gap: 1, marginBottom: 2 }}>
				{types.map((type) => (
					<Button
						key={type}
						variant={selectedType === type ? "contained" : "outlined"}
						onClick={() => setSelectedType(type)}
					>
						{type}
					</Button>
				))}
			</Box>

			{/* Buttons to select opshtina */}
			<Box sx={{ display: "flex", justifyContent: "center", gap: 1, marginBottom: 2 }}>
				{opshtini.map((opshtina) => (
					<Button
						key={opshtina.name}
						variant={
							selectedOpshtina?.name === opshtina.name ? "contained" : "outlined"
						}
						onClick={() => setSelectedOpshtina(opshtina)}
					>
						{opshtina.name}
					</Button>
				))}
			</Box>

			{/* Line chart */}
			{chartData.length > 0 ? (
				<Box sx={{ display: "flex", justifyContent: "center" }}>
					<LineChart
						width={1000}
						height={600}
						series={[
							{
								data: chartData.map(point => point.y),
								label: `Sensor Type: ${selectedType}`,
							},
						]}
						xAxis={[
							{
								data: chartData.map(point => point.x),
								label: "Hour of the Day",
							},
						]}
					/>
				</Box>
			) : (
				<Typography variant="h6" color="warning">
					No data available for selected sensor and type
				</Typography>
			)}
		</Box>
	);
};

export default LineChartComponent;  
