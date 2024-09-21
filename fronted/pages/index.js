// /pages/index.js
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    // Llamada a la API del backend desplegado
    axios.get('https://<your-backend-url>/attendance')
      .then(response => setAttendance(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>Lista de Asistencia</h1>
      <ul>
        {attendance.map((record, index) => (
          <li key={index}>{record.nombre} - {record.asistencia}</li>
        ))}
      </ul>
    </div>
  );
}
