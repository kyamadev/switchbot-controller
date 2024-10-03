import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.get('http://localhost:8000/api/logs/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setLogs(response.data.logs);
      } catch (error) {
        console.error('Error fetching logs:', error);
      }
    };

    fetchLogs();
  }, []);

  return (
    <div>
      <h1>Operation Logs</h1>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>
            {log.timestamp} - {log.device} - {log.action}
          </li>
        ))}
      </ul>
    </div>
  );
}