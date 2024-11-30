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

	const fullQuarterHourRange = Array.from({ length: 97 }, (_, i) => i / 4); // 96 quarter-hour points (0-23.75)

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

			const chartPoints = filteredData.map((data) => {
				const date = new Date(data.stamp);
				const hour = date.getHours();
				const minutes = date.getMinutes();
				const timePoint = hour + (Math.floor(minutes / 15) * 0.25); // 15-minute interval
				return {
					x: timePoint,
					y: parseFloat(data.value),
				};
			});

			const completeChartData = fullQuarterHourRange.map(timePoint => {
				const pointForTimePoint = chartPoints.find(point => point.x === timePoint);
				return pointForTimePoint || { x: timePoint, y: null };
			});

			setChartData(completeChartData.slice(0, 49).map(
				(point) => { return { x: point.x, y: point.y } })
				.concat(completeChartData.slice(49).map(
					(point) => { return { x: point.x, yprim: point.y } })));

		}
	}, [selectedType, selectedOpshtina, sensorData]);

	const xAxisTickFormatter = (value) => {
		const hours = Math.floor(value);
		const minutes = value % 1 === 0 ? '00' : value % 1 === 0.25 ? '15' : value % 1 === 0.5 ? '30' : '45';

		return `${hours.toString().padStart(2, '0')}:${minutes}`;
	};

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
						sx={{
							[`& .MuiLineElement-series-predicted`]: {
								strokeDasharray: '10 5',
								strokeWidth: 4,
							},
						}}
						series={
							[
								{
									id: 'realValue',
									dataKey: 'y',
									connectNulls: true,
									area: true,
									label: `pm10:`,
								},
								{
									id: 'predicted',
									dataKey: 'yprim',
									connectNulls: true,
									label: 'pm10 (predicted):'
								}
							]}
						xAxis={
							[
								{
									data: fullQuarterHourRange,
									label: "Time of Day",
									valueFormatter: xAxisTickFormatter,
								},
							]}
						dataset={chartData}
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
