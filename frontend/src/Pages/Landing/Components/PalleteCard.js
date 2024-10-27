import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../Styles/card.styles.css'



export default function PalleteCard({ title, desc, img, url }) {
  return (
    <>
      {/* <style>{cardStyle}</style> */}
      <Card className="custom-card">
        <Card.Img variant="top" src={img} className="custom-card-img" />
        <Card.Body className="custom-card-body">
          <Card.Title className="custom-card-title">{title}</Card.Title>
          <Card.Text className="custom-card-text">
            {desc}
          </Card.Text>
          <Link to={url}>
            <Button variant="primary" className="custom-card-button w-100">Get Started</Button>
          </Link>
        </Card.Body>
      </Card>
    </>
  );
}