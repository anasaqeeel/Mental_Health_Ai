import React from 'react';
import PalleteCard from './PalleteCard';
import { Container, Row, Col } from 'react-bootstrap';
import studentImg from "../Assets/student.jpg";
import teenImg from "../Assets/teens.jpg";
import personalImg from "../Assets/individual.jpg";
import '../Styles/selection.styles.css'



export default function SelectionPallete() {
    const cardData = [
        { title: "Personal Counseling", desc: "Individual Counseling for Adults", img: personalImg, url: "questionnaire" },
        { title: "Group Counseling", desc: "Counseling for Groups", img: teenImg, url: "questionnaire" },
        { title: "Student Counseling", desc: "Counseling for students", img: studentImg, url: "questionnaire" },
        { title: "Psychometric Testing", desc: "Psychology-based Counseling", img: studentImg, url: "PT" },
        { title: "Self-Report Testing", desc: "Counseling based on Self-Assessments", img: studentImg, url: "SRT" },
    ];

    return (
        <>
            {/* <style>{palleteStyle}</style> */}
            <div className="pallete-bg">
                <Container>
                    <div className="heading">
                        <h2>Therapy Is Healing</h2>
                    </div>
                    <div className="desc">
                        <h5>What counseling suits you the best?</h5>
                    </div>
                    <Row>
                        {cardData.map((card, index) => (
                            <Col key={index} lg={4} md={6} sm={12} className="mb-4">
                                <PalleteCard
                                    title={card.title}
                                    desc={card.desc}
                                    img={card.img}
                                    url={card.url}
                                />
                            </Col>
                        ))}
                    </Row>
                </Container>
            </div>
        </>
    );
}