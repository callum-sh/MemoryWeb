import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Container, Row, Col, Modal } from 'react-bootstrap';

const PhotoGallery = () => {
  const [photos, setPhotos] = useState([]);
  const [currentImage, setCurrentImage] = useState(null);

  const handleImageClick = (photo) => {
    setCurrentImage(photo);
  }

  const handleClose = () => {
    setCurrentImage(null);
  }

  useEffect(() => {
    axios
      .get('http://localhost:8000/graphing/get-photos/')
      .then(response => {
        setPhotos(response.data);
      })
      .catch(error => {
        console.error('Error fetching photos:', error);
      });
  }, []);

  return (
    <Container>
      <Row>
        {photos.map(photo => (
          <Col md={4} key={photo.id}>
            <Card>
              <div 
                onClick={() => handleImageClick(photo)}
                style={{ 
                  width: '100px', 
                  height: '100px', 
                  borderRadius: '50%', 
                  overflow: 'hidden', 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center',
                }}
              >
                <img 
                  src={photo.baseUrl} 
                  alt=""
                  style={{
                    flexShrink: 0,
                    minWidth: '50%',
                    minHeight: '50%',
                  }} 
                />
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Modal show={currentImage !== null} onHide={handleClose}>
        <Modal.Body>
          {currentImage && <img src={currentImage.baseUrl} alt="" style={{width: '100%'}} />}
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default PhotoGallery;
