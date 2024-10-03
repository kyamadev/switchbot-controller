import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/devices/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });
        setDevices(response.data);
      } catch (error) {
        console.error('Error fetching devices:', error);
      }
    };

    fetchDevices();
  }, []);

  return (
    <div>
      <h1>Device List</h1>
      <ul>
        {devices.map(device => (
          <li key={device.id}>
            {device.name} - Status: {device.status}
          </li>
        ))}
      </ul>
    </div>
  );
}