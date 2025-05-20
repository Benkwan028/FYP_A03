import React from 'react';
import './FeaturedProducts.css';

function FeaturedProducts() {
  const products = [
    { name: "Shoei GT-Air 2", price: "$563.00", rating: "1.00", image: "path-to-image" },
    { name: "AGV Sports Modular", price: "$3,214.00", rating: "4.00", image: "path-to-image" },
    { name: "Scorpion EXO-490", price: "$156.00", rating: "2.00", image: "path-to-image" },
  ];

  return (
    <section className="featured-products py-5">
      <div className="container">
        <h2 className="text-center mb-4">Hot Offers</h2>
        <div className="row">
          {products.map((product, index) => (
            <div className="col-md-4" key={index}>
              <div className="card">
                <img src={product.image} className="card-img-top" alt={product.name} />
                <div className="card-body">
                  <h5 className="card-title">{product.name}</h5>
                  <p className="card-text">Price: {product.price}</p>
                  <p className="card-text">Rating: {product.rating} out of 5</p>
                  <a href="/" className="btn btn-primary">Add to Cart</a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default FeaturedProducts;