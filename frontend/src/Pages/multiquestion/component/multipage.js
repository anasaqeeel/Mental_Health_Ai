import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "../style/pagestyle.css";

const Multipage = ({ test }) => {
    const questionnaires = test === "PT"
        ? [
            { name: "Big Five Inventory", link: "BFT", color: "purple", icon: "📋" },
            { name: "MMPI-2", link: "MMPI", color: "blue", icon: "👥" },
            { name: "Rorschach Inkblot Test", link: "IBT", color: "green", icon: "🖼️" },
            { name: "Neurotic Personality Questionnaire KON-2006", link: "NPQ", color: "purple", icon: "🧠" },
            { name: "Enneagram Test", link: "ENNEAGRAM", color: "yellow", icon: "🔢" },
        ]
        : [
            { name: "Adult ADHD Self-Report Scale (ASRS v1.1)", link: "ADHD", color: "purple", icon: "🔍" },
            { name: "Beck Depression Inventory (BDI)", link: "BDI", color: "blue", icon: "😔" },
            { name: "Obsessive-Compulsive Inventory-Revised (OCI-R)", link: "OCIR", color: "green", icon: "🔁" },
            { name: "Mood Disorder Questionnaire (MDQ)", link: "MDQ", color: "purple", icon: "🎭" },
            { name: "Generalized Anxiety Disorder-7 (GAD-7)", link: "GAD", color: "yellow", icon: "😰" },
        ];

    return (
        <div className="container">
            <div className="pt-5 d-flex flex-column justify-content-center align-items-center ">
                <header className="text-center mb-4">
                    <h1 className="display-4">Choose Your Questionnaire</h1>
                    <p className="lead">Select a survey to share your valuable insights</p>
                </header>


                <div className="row ">
                    {questionnaires.map((item, index) => (
                        <div className="col-md-4 mb-4 d-flex justify-content-center" key={index}>
                            <Link to={item.link} className="text-decoration-none w-100">
                                <div className="card shadow-lg h-100">
                                    <div className="card-body text-center">
                                        <div className="mb-3" style={{ fontSize: '2rem' }}>{item.icon}</div>
                                        <h5 className="card-title">{item.name}</h5>
                                        <p className="card-text text-muted">Click to start the survey</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Multipage;
