import React from "react";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
import Benefits from "../Assets/mental.png";
import "../style/pagestyle.css";
import { ReactTyped } from "react-typed";;
const Multipage = ({ test }) => {
    return (
        <>
            {/* <div className="container-fluid"> */}
                <div className="background">
                    {/* <img src={Benefits} className="backgroundimg"></img> */}
                    {test === 'PT' ? (
                        <ReactTyped
                            strings={['Welcome to Psychometric Testing']}
                            typeSpeed={40}
                            backSpeed={50}
                            loop
                        />) : <ReactTyped
                        strings={['Welcome to Self-Report Testing']}
                        typeSpeed={40}
                        backSpeed={50}
                        loop
                    />}
                </div>
                <div className="d-flex flex-column justify-content-center align-items-center mt-5 mb-5 ">
                    <div className="display-4 mb-5">Go through the Questionnaires for Prediction:</div>
                    {test === "PT" ? (<div className="d-flex flex-column justify-content-center align-items-center">
                        <Link to={"BFT"}><Button variant="primary" size="lg" className="bttn rounded-4"> Big Five Inventory</Button></Link>
                        <Link to={"MMPI"}><Button variant="primary" size="lg" className="bttn rounded-4"> MMPI-2</Button></Link>
                        <Link to={"IBT"}><Button variant="primary" size="lg" className="bttn rounded-4"> Rorschach Inkblot Test</Button></Link>
                        <Link to={"NPQ"}><Button variant="primary" size="lg" className="bttn rounded-4">Neurotic Personality Questionnaire KON-2006</Button></Link>
                        <Link to={"ENNEAGRAM"}><Button variant="primary" size="lg" className="bttn rounded-4"> Enneagram Test</Button></Link></div>) :
                        (<>
                            <Link to={"ADHD"}><Button variant="primary" size="lg" className="bttn rounded-4"> Adult ADHD Self-Report Scale (ASRS v1.1)</Button></Link>
                            <Link to={"BDI"}><Button variant="primary" size="lg" className="bttn rounded-4"> Beck Depression Inventory (BDI)</Button></Link>
                            <Link to={"OCIR"}><Button variant="primary" size="lg" className="bttn rounded-4"> Obsessive-Compulsive Inventory-Revised (OCI-R)</Button></Link>
                            <Link to={"MDQ"}><Button variant="primary" size="lg" className="bttn rounded-4"> Mood Disorder Questionnaire (MDQ)</Button></Link>
                            <Link to={"GAD"}><Button variant="primary" size="lg" className="bttn rounded-4">Generalized Anxiety Disorder-7 (GAD-7)</Button></Link>
                        </>)
                    }
                </div>

            {/* </div> */}
        </>
    )
}
export default Multipage;