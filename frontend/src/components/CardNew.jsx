import React from 'react';
import './Card.css';

const Card = ({ title, description, image, onClick, meta = {} }) => {
  return (
    <div className="card" onClick={onClick}>
      {image && <img src={image} alt={title} className="card-image" />}
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <p className="card-description">{description}</p>
        {Object.entries(meta).map(([key, value]) => (
          <p key={key} className="card-meta">
            <span className="meta-label">{key}:</span> {value}
          </p>
        ))}
      </div>
    </div>
  );
};

export default Card;
