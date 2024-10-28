// frontend/src/Pages/Visualize/Visualization.jsx

import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Container, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const Visualization = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        // Fetch data from the backend API
        axios.get('http://localhost:8000/api/mmpi2-questionnaire/stats/')
            .then(response => {
                const data = response.data;
                const labels = Object.keys(data);
                const trueCounts = labels.map(label => data[label]['True']);
                const falseCounts = labels.map(label => data[label]['False']);

                setChartData({
                    labels: labels.map(label => formatLabel(label)),
                    datasets: [
                        {
                            label: 'True',
                            data: trueCounts,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        },
                        {
                            label: 'False',
                            data: falseCounts,
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        },
                    ],
                });
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching questionnaire stats:', error);
                setError(true);
                setLoading(false);
            });
    }, []);

    // Helper function to format label names (e.g., from camelCase to Sentence Case)
    const formatLabel = (label) => {
        return label
            .replace(/([A-Z])/g, ' $1') // Add space before capital letters
            .replace(/^./, str => str.toUpperCase()); // Capitalize the first letter
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'MMPI2 Questionnaire Responses',
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0
                }
            }
        }
    };

    if (loading) {
        return (
            <Container className="text-center mt-5">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
                <p>Loading data...</p>
            </Container>
        );
    }

    if (error) {
        return (
            <Container className="mt-5">
                <Alert variant="danger">
                    Failed to load questionnaire data. Please try again later.
                </Alert>
            </Container>
        );
    }

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">MMPI2 Questionnaire Responses</h2>
            <Bar data={chartData} options={options} />
        </Container>
    );
};

export default Visualization;
