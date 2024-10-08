import React from 'react'
import PalleteCard from './PalleteCard'
import "../Styles/selection.styles.css"
import studentImg from "../Assets/student.jpg"
import teenImg from "../Assets/teens.jpg"
import personalImg from "../Assets/individual.jpg"

export default function SelectionPallete() {
  return (
    <div>
        <div className="pallete-bg">

            <div className="heading">
                <h2>Therapy Is Healing</h2>
            </div>

            <div className="desc">
                <h5>What counseling suits you the best ?</h5>
            </div>
            
            <div className="card-grid">
                <PalleteCard title={"Personal Counseling"} desc={"Individual Counseling for Adults"} img={personalImg}/>
                <PalleteCard title={"Group Counseling"} desc={"Counseling for Groups"} img={teenImg}/>
                <PalleteCard title={"Student Counseling"} desc={"Counseling for students"} img={studentImg}/>
            </div>
        </div>
    </div>
  )
}
