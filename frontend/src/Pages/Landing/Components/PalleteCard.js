import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import "../Styles/card.styles.css";
import { Link } from 'react-router-dom';

export default function PalleteCard(props) {
  return (
    <div className="card-container">
      <Card style={{ width: '24rem', margin: '2rem', borderRadius: '15px', boxShadow: '0px 8px 15px rgba(0, 0, 0, 0.1)' }}>
        <Card.Img variant="top" src={props.img} style={{ borderTopLeftRadius: '15px', borderTopRightRadius: '15px' }} />
        <Card.Body style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Card.Title style={{ fontWeight: 'bold', color: '#2C3E50' }}>{props.title}</Card.Title>
          <Card.Text style={{ color: '#7F8C8D', marginBottom: '1.5rem' }}>
            {props.desc}
          </Card.Text>
          <Link to={props.url}>
            <Button variant="primary" style={{ backgroundColor: '#2980B9', borderColor: '#2980B9', width: '100%' }}>Get Started</Button>
          </Link>
        </Card.Body>
      </Card>
    </div>
  )
}
