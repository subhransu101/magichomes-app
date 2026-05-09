import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { MapPin, Bed, Bath, Square, ArrowLeft, Building, Phone } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function PropertyPage() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperty = async () => {
      try {
        const response = await axios.get(`${API_URL}/properties/${id}`);
        setProperty(response.data);
      } catch (error) {
        console.error('Error fetching property:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProperty();
  }, [id]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumSignificantDigits: 3
    }).format(price);
  };

  if (loading) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <h2>Loading property details...</h2>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <h2>Property not found.</h2>
        <Link to="/" className="search-button" style={{ display: 'inline-flex', marginTop: '20px', textDecoration: 'none' }}>
          Back to Search
        </Link>
      </div>
    );
  }

  return (
    <div className="property-page container">
      <Link to="/" className="back-link">
        <ArrowLeft size={20} />
        Back to Search Results
      </Link>

      <div className="property-details-container">
        <div className="property-gallery">
          <img src={property.image_url} alt={property.title} className="main-image" />
          <div className="property-tags">
            <span className="tag primary-tag">For {property.property_type}</span>
            <span className="tag secondary-tag">{property.house_type}</span>
          </div>
        </div>

        <div className="property-info-card">
          <div className="property-header">
            <h1 className="property-title-large">{property.title}</h1>
            <div className="property-location-large">
              <MapPin size={20} />
              <span>{property.city}</span>
            </div>
            <div className="property-price-large">{formatPrice(property.price)}</div>
          </div>

          <div className="property-specs-grid">
            <div className="spec-item">
              <Bed size={24} className="spec-icon" />
              <div className="spec-details">
                <span className="spec-value">{property.bedrooms}</span>
                <span className="spec-label">Bedrooms</span>
              </div>
            </div>
            <div className="spec-item">
              <Bath size={24} className="spec-icon" />
              <div className="spec-details">
                <span className="spec-value">{property.bathrooms}</span>
                <span className="spec-label">Bathrooms</span>
              </div>
            </div>
            <div className="spec-item">
              <Square size={24} className="spec-icon" />
              <div className="spec-details">
                <span className="spec-value">{property.area_sqft}</span>
                <span className="spec-label">Sq Ft</span>
              </div>
            </div>
            <div className="spec-item">
              <Building size={24} className="spec-icon" />
              <div className="spec-details">
                <span className="spec-value">{property.house_type}</span>
                <span className="spec-label">Type</span>
              </div>
            </div>
          </div>

          <div className="property-description">
            <h3>About this Property</h3>
            <p>
              This beautiful {property.house_type} located in the heart of {property.city} offers {property.bedrooms} bedrooms and {property.bathrooms} bathrooms. With a spacious area of {property.area_sqft} sq.ft, it is perfectly suited for those looking for a comfortable living space. Don't miss the opportunity to make this your new home.
            </p>
          </div>

          <div className="action-section">
            <button 
              className="enquire-button" 
              onClick={() => {
                const message = encodeURIComponent(`Hi, I'm interested in the property: ${property.title} in ${property.city}.`);
                const phone = '918260693896';
                window.open(`https://wa.me/${phone}?text=${message}`, '_blank');
              }}
            >
              <Phone size={20} />
              Enquire Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PropertyPage;
