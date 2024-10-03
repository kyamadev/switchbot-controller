import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function DeviceDetail() {
  const [device, setDevice] = useState(null);
  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    if (id) {
      const fetchDevice = async () => {
        const token = localStorage.getItem('token');
        try {
          const response = await axios.get(`http://localhost:8000/api/devices/${id}/`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          setDevice(response.data);
        } catch (error) {
          console.error('Error fetching device details:', error);
        }
      };

      fetchDevice();
    }
  }, [id]);

  const handleToggle = async () => {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(`http://localhost:8000/api/devices/${id}/control/`, {
        command: device.status === 'on' ? 'turnOff' : 'turnOn'
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setDevice(prev => ({ ...prev, status: prev.status === 'on' ? 'off' : 'on' }));
    } catch (error) {
      console.error('Error controlling device:', error);
    }
  };

  if (!device) return <div>Loading...</div>;

  return (
    <div>
      <h1>{device.name}</h1>
      <p>Status: {device.status}</p>
      <button onClick={handleToggle}>
        {device.status === 'on' ? 'Turn Off' : 'Turn On'}
      </button>
    </div>
  );
}