import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Container, Row, Col } from 'react-bootstrap';

const PhotoGallery = () => {
  const [photos, setPhotos] = useState([]);

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
              <Card.Img variant="top" src={photo.baseUrl} />
              <Card.Body>
                <Card.Title>{photo.filename}</Card.Title>
                <Card.Text>{photo.productUrl}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default PhotoGallery;
