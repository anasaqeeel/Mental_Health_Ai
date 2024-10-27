import React from 'react';
import { Carousel } from 'react-bootstrap';
import '../Styles/carousalStyle.css'


const CarouselComponent = () => {
    return (
        <>
            {/* <style>{carouselStyle}</style> */}
            <Carousel fade>
                <Carousel.Item>
                    <img className="d-block w-100" src="/Assets/mental.jpg" alt="Mental health support" />
                    <Carousel.Caption>
                        <h3>Empowering Your Mental Health Journey</h3>
                        <p>Discover personalized support and guidance for your well-being.</p>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item>
                    <img className="d-block w-100" src="/Assets/mental7.webp" alt="Group therapy session" />
                    <Carousel.Caption>
                        <h3>Connect and Heal Together</h3>
                        <p>Experience the power of group therapy and shared growth.</p>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item>
                    <img className="d-block w-100" src="/Assets/mental8.webp" alt="Individual counseling" />
                    <Carousel.Caption>
                        <h3>Your Path to Personal Growth</h3>
                        <p>Tailored counseling to help you overcome challenges and thrive.</p>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item>
                    <img className="d-block w-100" src="/Assets/mental9.png" alt="Mindfulness and relaxation" />
                    <Carousel.Caption>
                        <h3>Find Your Inner Peace</h3>
                        <p>Learn techniques for mindfulness and stress reduction.</p>
                    </Carousel.Caption>
                </Carousel.Item>
            </Carousel>
        </>
    );
};

export default CarouselComponent;