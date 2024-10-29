import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title as ChartTitle,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './Visualization.css'; // Create this CSS file for styling

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTitle, Tooltip, Legend);

const Visualization = () => {
    const [selectedQuestionnaire, setSelectedQuestionnaire] = useState('ADHD');
    const [chartData, setChartData] = useState(null);

    const questionnaires = ['ADHD', 'GAD', 'BDI', 'OCIR', 'ENNEAGRAM'];

    // Response options for each questionnaire
    const questionnaireOptions = {
        ADHD: {
            options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Very Often'],
        },
        GAD: {
            options: ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
        },
        BDI: {
            optionsPerQuestion: true,
            questions: [
                'feelingsOfSadness',
                'thoughtsAboutFuture',
                'definitionOfSuccess',
                'abilityToExperiencePleasure',
                'negativeSelfStatements',
                'feelingsOfPunishment',
                'disappointmentsInSelf',
                'handlingSelfCriticism',
                'thoughtsOfSelfHarm',
                'frequencyOfCrying',
            ],
            options: {
                feelingsOfSadness: [
                    'I do not feel sad.',
                    'I feel sad',
                    "I am sad all the time and I can't snap out of it.",
                    "I am so sad and unhappy that I can't stand it.",
                ],
                thoughtsAboutFuture: [
                    'I am not particularly discouraged about the future.',
                    'I feel discouraged about the future.',
                    'I feel I have nothing to look forward to.',
                    'I feel the future is hopeless and that things cannot improve.',
                ],
                definitionOfSuccess: [
                    'I do not feel like a failure',
                    'I feel I have failed more than the average person.',
                    'As I look back on my life, all I can see is a lot of failures.',
                    'I feel I am a complete failure as a person.',
                ],
                abilityToExperiencePleasure: [
                    'I get as much satisfaction out of things as I used to.',
                    "I don't enjoy things the way I used to.",
                    "I don't get real satisfaction out of anything anymore.",
                    'I am dissatisfied or bored with everything.',
                ],
                negativeSelfStatements: [
                    "I don't feel particularly guilty",
                    'I feel guilty a good part of the time.',
                    'I feel quite guilty most of the time.',
                    'I feel guilty all of the time.',
                ],
                feelingsOfPunishment: [
                    "I don't feel I am being punished.",
                    'I feel I may be punished.',
                    'I expect to be punished.',
                    'I feel I am being punished.',
                ],
                disappointmentsInSelf: [
                    "I don't feel disappointed in myself.",
                    'I am disappointed in myself.',
                    'I am disgusted with myself.',
                    'I hate myself',
                ],
                handlingSelfCriticism: [
                    "I don't feel I am any worse than anybody else.",
                    'I am critical of myself for my weaknesses or mistakes.',
                    'I blame myself all the time for my faults.',
                    'I blame myself for everything bad that happens.',
                ],
                thoughtsOfSelfHarm: [
                    "I don't have any thoughts of killing myself.",
                    'I have thoughts of killing myself, but I would not carry them out.',
                    'I would like to kill myself.',
                    'I would kill myself if I had the chance.',
                ],
                frequencyOfCrying: [
                    "I don't cry any more than usual.",
                    'I cry more now than I used to.',
                    'I cry all the time now.',
                    "I used to be able to cry, but now I can't cry even though I want to.",
                ],
            },
        },
        OCIR: {
            options: [
                "Not at all",
                "A little",
                "Moderately",
                "A lot",
                "Extremely"
            ],
        },
        ENNEAGRAM: {
            options: [
                "Almost Never 1",
                "Rarely 2",
                "Sometimes 3",
                "Frequently 4",
                "Almost Always 5"
            ],
        },
    };

    useEffect(() => {
        fetchData();
    }, [selectedQuestionnaire]);

    const fetchData = async () => {
        try {
            const response = await axios.get(
                `http://127.0.0.1:8000/api/${selectedQuestionnaire.toLowerCase()}-questionnaire/stats/`
            );
            const data = response.data;

            const questionnaireData = questionnaireOptions[selectedQuestionnaire];

            if (questionnaireData.optionsPerQuestion) {
                // For BDI, where options vary per question, create multiple charts
                const chartsArray = [];
                const questions = questionnaireData.questions;

                questions.forEach((questionKey) => {
                    const questionData = data[questionKey];
                    const responseOptions = questionnaireData.options[questionKey];

                    // Ensure all response options are included, even if count is zero
                    const counts = responseOptions.map((option) => questionData[option] || 0);

                    const chartData = {
                        labels: responseOptions,
                        datasets: [
                            {
                                label: formatLabel(questionKey),
                                data: counts,
                                backgroundColor: getColors(responseOptions.length),
                            },
                        ],
                    };

                    chartsArray.push({ questionKey, chartData });
                });

                setChartData({ multipleCharts: true, charts: chartsArray });
            } else {
                // For questionnaires where all questions share the same options
                const labels = Object.keys(data).map((q) => formatLabel(q));
                const responseOptions = questionnaireData.options;

                const datasets = labels.map((label, index) => {
                    const questionKey = Object.keys(data)[index];
                    const dataPoints = responseOptions.map((option) => data[questionKey][option] || 0);

                    return {
                        label: label,
                        data: dataPoints,
                        backgroundColor: getColor(index),
                    };
                });

                setChartData({
                    multipleCharts: false,
                    data: {
                        labels: responseOptions,
                        datasets: datasets,
                    },
                });
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const formatLabel = (label) => {
        // Format the label by inserting spaces before capital letters
        return label.replace(/([a-z])([A-Z])/g, '$1 $2');
    };

    const getColors = (numColors) => {
        const colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
            'rgba(199, 199, 199, 0.6)',
            'rgba(83, 102, 255, 0.6)',
            'rgba(255, 99, 132, 0.6)',
            // Add more colors if needed
        ];
        if (numColors <= colors.length) {
            return colors.slice(0, numColors);
        } else {
            // Generate additional colors if needed
            const extraColors = [];
            for (let i = 0; i < numColors - colors.length; i++) {
                const r = Math.floor(Math.random() * 256);
                const g = Math.floor(Math.random() * 256);
                const b = Math.floor(Math.random() * 256);
                extraColors.push(`rgba(${r}, ${g}, ${b}, 0.6)`);
            }
            return colors.concat(extraColors);
        }
    };

    const getColor = (index) => {
        const colors = getColors(20); // Adjust the number as needed
        return colors[index % colors.length];
    };

    return (
        <div className="visualization-container">
            <h1 className="visualization-title">Questionnaire Data Visualization</h1>
            <div className="dropdown-container">
                <select
                    className="dropdown"
                    value={selectedQuestionnaire}
                    onChange={(e) => setSelectedQuestionnaire(e.target.value)}
                >
                    {questionnaires.map((q) => (
                        <option key={q} value={q}>
                            {q}
                        </option>
                    ))}
                </select>
            </div>

            {chartData && (
                <div className="chart-container">
                    {chartData.multipleCharts ? (
                        chartData.charts.map(({ questionKey, chartData }, index) => (
                            <div key={index} className="chart-item">
                                <h3>{formatLabel(questionKey)}</h3>
                                <Bar
                                    data={chartData}
                                    options={{
                                        responsive: true,
                                        plugins: {
                                            title: {
                                                display: true,
                                                text: `${formatLabel(questionKey)}`,
                                                font: {
                                                    size: 16,
                                                },
                                            },
                                            legend: {
                                                display: false,
                                            },
                                        },
                                        scales: {
                                            x: {
                                                ticks: {
                                                    autoSkip: false,
                                                    maxRotation: 90,
                                                    minRotation: 0,
                                                },
                                            },
                                        },
                                    }}
                                />
                            </div>
                        ))
                    ) : (
                        <Bar
                            data={chartData.data}
                            options={{
                                responsive: true,
                                plugins: {
                                    title: {
                                        display: true,
                                        text: `${selectedQuestionnaire} Questionnaire Results`,
                                        font: {
                                            size: 20,
                                        },
                                    },
                                    legend: {
                                        display: true,
                                        position: 'right',
                                    },
                                },
                                scales: {
                                    x: {
                                        ticks: {
                                            autoSkip: false,
                                        },
                                    },
                                },
                            }}
                        />
                    )}
                </div>
            )}
        </div>
    );
};

export default Visualization;
