import React from 'react'
import Accordion from 'react-bootstrap/Accordion';
import "../Styles/faq.styles.css"
import plantImg from "../Assets/plant.png"

export default function Faq() {
  return (
    <div className="faq-bg">
      <div className="faq-grid">
        <div className="left">
          <div className="faq-content-flex">
            <div className="faq-heading">
                <h2>Any Questions ?</h2>
            </div>

            <div className="faq-desc">
                <p>Feel free to contact us in case of any further queries</p>
            </div>

            <div className="plant-img">
                <img src={plantImg} alt="Plant" />
            </div>
          </div>
        </div>

        <div className="accord">
            <Accordion>
              <Accordion.Item eventKey="0" style={{marginBottom:"1rem"}}>
                <Accordion.Header>Is online therapy effective?</Accordion.Header>
                <Accordion.Body>
                  Online therapy is proven to be as effective, if not more effective than face-to-face therapy. A study conducted by Talkspace & the Journal of Telemedicine and e-Health showed that text-based therapy through Talkspace was highly effective and comparable to traditional therapy.
                </Accordion.Body>
              </Accordion.Item>

              <Accordion.Item eventKey="1" style={{marginBottom:"1rem"}}>
                <Accordion.Header>What is the difference between therapy and psychiatry?</Accordion.Header>
                <Accordion.Body>
                  Therapy and psychiatry can both play an important role in your mental health treatment plan. In therapy, licensed therapists work with you to discuss personal challenges and devise a personalized plan, but they aren't able to prescribe medication.
                  
                  Psychiatry is a medical specialty that prescribes and monitors medication to treat mental health symptoms. Psychiatrists and psychiatric providers are licensed medical providers who specialize in mental health treatment and can provide psychiatric care services and personalized medication management.
                </Accordion.Body>
              </Accordion.Item>

              <Accordion.Item eventKey="2" style={{marginBottom:"1rem"}}>
                <Accordion.Header>How do I get matched with a therapist?</Accordion.Header>
                <Accordion.Body>
                  After you answer a few online questions about your symptoms and preferences you'll be matched with a therapist who is licensed in your state and who is likely to be a good fit for your needs.
                </Accordion.Body>
              </Accordion.Item>

              <Accordion.Item eventKey="3" style={{marginBottom:"1rem"}}>
                <Accordion.Header>Is there any additional costs involved ?</Accordion.Header>
                <Accordion.Body>
                  No, There are no costs for using the website's services.
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
        </div>
      </div>
    </div>
  )
}
