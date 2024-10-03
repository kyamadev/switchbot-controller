import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Devices() {
  const [devices, setDevices] = useState([]);

  const fetchDevices = async () => {
    const token = localStorage.getItem('token');  // JWTトークンを取得
    if (!token) {
      console.error('No token found');
      return;
    }

    try {
      const response = await axios.get('http://localhost:8000/api/devices/', {
        headers: {
          Authorization: `Bearer ${token}`  // トークンをヘッダーに設定
        }
      });
      setDevices(response.data.devices);
    } catch (error) {
      console.error('Error fetching devices:', error);
    }
  };

  useEffect(() => {
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