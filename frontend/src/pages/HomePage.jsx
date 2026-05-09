import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Search, MapPin, Bed, Bath, Square } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function HomePage() {
  const [properties, setProperties] = useState([]);
  const [city, setCity] = useState('');
  const [propertyType, setPropertyType] = useState('buy');
  const [houseType, setHouseType] = useState('');
  const [budget, setBudget] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    setLoading(true);
    try {
      let params = new URLSearchParams();
      if (city) params.append('city', city);
      if (propertyType) params.append('property_type', propertyType);
      if (houseType) params.append('house_type', houseType);
      
      // Parse budget
      if (budget) {
        if (propertyType === 'buy') {
          if (budget === 'under50l') params.append('max_price', 5000000);
          else if (budget === '50l-1cr') {
            params.append('min_price', 5000000);
            params.append('max_price', 10000000);
          } else if (budget === 'above1cr') params.append('min_price', 10000000);
        } else {
          if (budget === 'under20k') params.append('max_price', 20000);
          else if (budget === '20k-50k') {
            params.append('min_price', 20000);
            params.append('max_price', 50000);
          } else if (budget === 'above50k') params.append('min_price', 50000);
        }
      }

      const response = await axios.get(`${API_URL}/properties?${params.toString()}`);
      setProperties(response.data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProperties();
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumSignificantDigits: 3
    }).format(price);
  };

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1 className="hero-title animate-fade-in">Find Your Dream Home</h1>
          <p className="hero-subtitle animate-fade-in" style={{ animationDelay: '0.1s' }}>
            Discover the best properties in Bangalore and Mumbai
          </p>
          
          <form className="search-container animate-fade-in" style={{ animationDelay: '0.2s' }} onSubmit={handleSearch}>
            <select 
              className="search-select" 
              value={propertyType} 
              onChange={(e) => {
                setPropertyType(e.target.value);
                setBudget(''); // Reset budget when type changes
              }}
            >
              <option value="buy">Buy</option>
              <option value="rent">Rent</option>
            </select>

            <select 
              className="search-select" 
              value={houseType} 
              onChange={(e) => setHouseType(e.target.value)}
            >
              <option value="">Any Type</option>
              <option value="flat">Flat</option>
              <option value="house">House</option>
            </select>
            
            <select 
              className="search-select" 
              value={city} 
              onChange={(e) => setCity(e.target.value)}
            >
              <option value="">All Cities</option>
              <option value="Bangalore">Bangalore</option>
              <option value="Mumbai">Mumbai</option>
            </select>
            
            <select 
              className="search-select" 
              value={budget} 
              onChange={(e) => setBudget(e.target.value)}
            >
              <option value="">Any Budget</option>
              {propertyType === 'buy' ? (
                <>
                  <option value="under50l">Under ₹50 Lac</option>
                  <option value="50l-1cr">₹50 Lac - ₹1 Cr</option>
                  <option value="above1cr">Above ₹1 Cr</option>
                </>
              ) : (
                <>
                  <option value="under20k">Under ₹20,000</option>
                  <option value="20k-50k">₹20,000 - ₹50,000</option>
                  <option value="above50k">Above ₹50,000</option>
                </>
              )}
            </select>
            
            <button type="submit" className="search-button">
              <Search size={20} />
              Search
            </button>
          </form>
        </div>
      </section>

      <main className="properties-section container">
        <h2 className="section-title">
          {loading ? 'Searching...' : `Found ${properties.length} Properties`}
        </h2>
        
        {!loading && properties.length === 0 && (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>
            No properties found matching your criteria. Try adjusting your search filters.
          </div>
        )}

        <div className="property-grid">
          {properties.map((property, index) => (
            <Link 
              to={`/property/${property.id}`}
              key={property.id} 
              className="property-card animate-fade-in" 
              style={{ animationDelay: `${index * 0.1}s`, textDecoration: 'none', color: 'inherit' }}
            >
              <div className="property-image-container">
                <span className="property-badge">For {property.property_type} • {property.house_type}</span>
                <img src={property.image_url} alt={property.title} className="property-image" />
              </div>
              <div className="property-content">
                <div className="property-price">{formatPrice(property.price)}</div>
                <h3 className="property-title">{property.title}</h3>
                <div className="property-location">
                  <MapPin size={16} />
                  {property.city}
                </div>
                <div className="property-features">
                  <div className="feature">
                    <Bed size={18} className="feature-icon" />
                    <span>{property.bedrooms} Beds</span>
                  </div>
                  <div className="feature">
                    <Bath size={18} className="feature-icon" />
                    <span>{property.bathrooms} Baths</span>
                  </div>
                  <div className="feature">
                    <Square size={18} className="feature-icon" />
                    <span>{property.area_sqft} sqft</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </>
  );
}

export default HomePage;
