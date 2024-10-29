// frontend/src/Pages/Visualize/Visualization.jsx

import React, { useEffect, useState, useCallback } from 'react';
import { Bar } from 'react-chartjs-2';
import { Container, Spinner, Alert, Form } from 'react-bootstrap';
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

// Register Chart.js components
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
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);

    // List of available questionnaires
    const [questionnaires, setQuestionnaires] = useState([]);
    const [selectedQuestionnaire, setSelectedQuestionnaire] = useState('');

    // Initialize available questionnaires
    useEffect(() => {
        const availableQuestionnaires = [
            { name: 'MMPI2', displayName: 'MMPI2 Questionnaire' },
            { name: 'GAD', displayName: 'GAD Questionnaire' },
            // Add other questionnaires here as needed
        ];
        setQuestionnaires(availableQuestionnaires);
        if (availableQuestionnaires.length > 0) {
            setSelectedQuestionnaire(availableQuestionnaires[0].name); // Default selection
        }
    }, []);

    // Memoize fetchChartData to prevent ESLint warning
    const fetchChartData = useCallback(async (questionnaireType) => {
        setLoading(true);
        setError(false);
        let endpoint = '';
        switch (questionnaireType) {
            case 'MMPI2':
                endpoint = '/api/mmpi2-questionnaire/stats/';
                break;
            case 'GAD':
                endpoint = '/api/gad-questionnaire/stats/';
                break;
            // Add cases for other questionnaires here
            default:
                endpoint = '/api/mmpi2-questionnaire/stats/';
        }

        console.log(`Fetching data from endpoint: ${endpoint}`);

        try {
            const response = await axios.get(endpoint);
            console.log('API response:', response.data);
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
        } catch (error) {
            console.error(`Error fetching ${questionnaireType} stats:`, error);
            setError(true);
            setLoading(false);
        }
    }, []);

    // Fetch data when selectedQuestionnaire changes
    useEffect(() => {
        if (selectedQuestionnaire) {
            fetchChartData(selectedQuestionnaire);
        }
    }, [selectedQuestionnaire, fetchChartData]);

    // Helper function to format labels
    const formatLabel = (label) => {
        return label
            .replace(/([A-Z])/g, ' $1') // Add space before capital letters
            .replace(/^./, str => str.toUpperCase()); // Capitalize the first letter
    };

    // Handle dropdown change
    const handleQuestionnaireChange = (e) => {
        setSelectedQuestionnaire(e.target.value);
    };

    // Chart options
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: `${selectedQuestionnaire} Questionnaire Responses`,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0, // Ensure y-axis labels are integers
                },
            },
        },
    };

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">Questionnaire Responses Visualization</h2>

            <Form.Group controlId="questionnaireSelect" className="mb-4">
                <Form.Label>Select Questionnaire:</Form.Label>
                <Form.Control as="select" value={selectedQuestionnaire} onChange={handleQuestionnaireChange}>
                    {questionnaires.map(q => (
                        <option key={q.name} value={q.name}>{q.displayName}</option>
                    ))}
                </Form.Control>
            </Form.Group>

            {loading && (
                <div className="text-center">
                    <Spinner animation="border" role="status" />
                    <p>Loading data...</p>
                </div>
            )}

            {error && (
                <Alert variant="danger">
                    Failed to load questionnaire data. Please try again later.
                </Alert>
            )}

            {chartData && !loading && !error && (
                <Bar data={chartData} options={options} />
            )}
        </Container>
    );
};

export default Visualization;
