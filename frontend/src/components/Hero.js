import React from 'react';
import './Hero.css';

function Hero() {
  return (
    <section className="hero">
      <div className="container text-center py-5">
        <h1>Find the Best Motorbike Parts for Your Vehicle</h1>
        <p>Browse our range of Gore-Tex motorcycle clothing including Rukka, Dainese, Richa, Alpinestars, and more</p>
        <a href="/shop" className="btn btn-primary">Shop Now</a>
      </div>
    </section>
  );
}

export default Hero;