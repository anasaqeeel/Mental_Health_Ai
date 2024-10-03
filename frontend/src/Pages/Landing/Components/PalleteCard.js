import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import "../Styles/card.styles.css"
import { Link } from 'react-router-dom';

export default function PalleteCard(props) {
  return (
    <div>
    <Card style={{ width: '24rem', margin:'2rem'}}>
      <Card.Img variant="top" src={props.img} />
      <Card.Body style={{display:"flex", flexDirection:"column",alignItems:"center"}}>
        <Card.Title>{props.title}</Card.Title>
        <Card.Text>
            {props.desc}
        </Card.Text>
        <Link to={props.url}><Button variant="primary">Get Started</Button></Link>
      </Card.Body>
    </Card>
    </div>
  )
}
