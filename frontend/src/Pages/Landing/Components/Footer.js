import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-dark text-white py-5">
      <div className="container">
        <div className="row">
          {/* Contact Us Section */}
          <div className="col-md-4">
            <h3 className="h5 mb-4">Contact Us</h3>
            <p className="mb-2"><strong>Email:</strong> info@example.com</p>
            <p className="mb-2"><strong>Phone:</strong> (123) 456-7890</p>
            <p><strong>Address:</strong> 123 Main St, City, Country</p>
          </div>

          {/* Quick Links Section */}
          <div className="col-md-4">
            <h3 className="h5 mb-4">Quick Links</h3>
            <ul className="list-unstyled">
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Home</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">About</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Services</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Contact</a></li>
            </ul>
          </div>

          {/* Newsletter Section */}
          <div className="col-md-4">
            <h3 className="h5 mb-4">Newsletter</h3>
            <p>Sign up for personalized emails and queries</p>
            <form className="d-flex">
              <input
                type="email"
                placeholder="Enter your email"
                className="form-control me-2 mb-2"
                style={{ backgroundColor: '#343a40', color: 'white' }}
              />
              <button
                type="submit"
                className="btn btn-primary mb-2"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>

        {/* Social Icons and Footer Text */}
        <div className="text-center mt-4">
          {/* <p className="mb-3" style={{ maxWidth: '600px', margin: '0 auto' }}>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt distinctio earum repellat quaerat
            voluptatibus placeat nam, commodi optio pariatur est quia magnam eum harum corrupti dicta, aliquam
            sequi voluptate quas.
          </p> */}
          <div className="mb-4">
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-facebook-f"></i>
            </a>
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-twitter"></i>
            </a>
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-google"></i>
            </a>
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-instagram"></i>
            </a>
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-linkedin-in"></i>
            </a>
            <a href="#!" className="btn btn-outline-light btn-floating m-1" role="button">
              <i className="fab fa-github"></i>
            </a>
          </div>
          {/* <p>&copy; 2023 Your Company. All rights reserved.</p>
          <p>Made with React and Django</p> */}
        </div>
      </div>
    </footer>
  );
}

export default Footer;
